# TipiVariable.py
#
# ElectricLab
# Class to support "Network Variables"
#
#

import struct
import fcntl
import os
import errno
import re
import sys
import socket
import logging
from Oled import oled

logger = logging.getLogger(__name__)

runtime_dir = '/home/tipi/.tipivars/'

class TipiVariable(object):

    def __init__(self, tipi_io):
        self.tipi_io = tipi_io
        
    
    def processRequest(self, message):
        logger.debug("request: %s", message)
     
        # Fields:
        # caller_guid        Program's GUID
        # action             'R', 'W', 'T'   read, write, transmit
        # var_key            Key
        # var_val            Value
        # queue              Allow values to queue for these variables. (only locally for now)
        # remote_var_key     The name of the remote variable, if we're transmitting this var/val.
        # remote_id          Remote ID to present, if we're transmitting this var/val. We're going to use session_id for the remote_id

        
        # Messages look like: (Tab-delimited)
        #
        # CHATTI     R   REMOTE_HOST     NULL        0   NULL        NULL
        # CHATTI     W   REMOTE_PORT     9900        0   NULL        NULL
        # CHATTI     W   MESSAGE         [myPasswd]  0   AUTHPASS    NULL
        # CHATTI     W   MESSAGE         TESTING123  0   MESSAGE     [session_id]


        # Now that we have message, let's parse it:
        ti_message = message.split("\t")

        caller_guid    = ti_message[0] if len(ti_message) >= 1 else ''  # Program's GUID
        action         = ti_message[1] if len(ti_message) >= 2 else ''  # 'R', 'W', 'U', 'T'   read, write, transmit via UDP, transmit via TCP
        var_key        = ti_message[2] if len(ti_message) >= 3 else ''  # Key
        var_val        = ti_message[3] if len(ti_message) >= 4 else ''
        queue          = ti_message[4] if len(ti_message) >= 5 else ''  # Allow values to queue for these variables. (only locally for now)
        remote_var_key = ti_message[5] if len(ti_message) >= 6 else ''  # The name of the remote variable, if we're transmitting this var/val.
        remote_id      = ti_message[6] if len(ti_message) >= 7 else ''  # Remote ID to present, if we're transmitting this var/val. We're going to use session_id for the remote_id

        oled.info("VAR:%s/%s %s", caller_guid, action, var_key)

        # Our response will be stored in "remote_var_key.RESP"
        response = str(remote_var_key) + '.RESP' if (len(remote_var_key)) else ''

        # Load our existing variables into a dict:
        self.ti_vars = {}
        
        guid_file = runtime_dir + caller_guid
        
        if os.path.isfile(str(guid_file)):
            with open(str(guid_file), "r") as f:
                for line in f:
                    line = line.rstrip("\n\r")   # Strip newlines, but not whitespace (which is what rstrip() alone will do)
                    data = line.split("\t")
                    
                    if len(data) > 1:
                        self.ti_vars[data[0]] = data[1]

            f.close

        if action == 'W' or action == 'U' or action == 'T':   # Write!
            self.ti_vars[response] = ''  # Blank out our old response
        
            var_val = var_val.rstrip()

            self.ti_vars[str(var_key)] = str(var_val)
                
            self.store(caller_guid)   # Write our vars to our local file


        if action == 'U':    #   TX via UDP    NOT COMPLETE! FIX!!!
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            server_address = (self.ti_vars['REMOTE_HOST'], int(self.ti_vars['REMOTE_PORT']))

            sock.close()

            self.store(caller_guid)   # Write our vars to our local file


        elif action == 'T':    #   TX via TCP
            if 'REMOTE_HOST' not in self.ti_vars or 'REMOTE_PORT' not in self.ti_vars:
                return bytearray("!ERROR!")

            self.ti_vars[response] = ''  # Blank out our old response

            message = str(remote_id) + "\t" + str(remote_var_key) + "\t" + str(var_val)

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            try:
                server_address = (self.ti_vars['REMOTE_HOST'], int(self.ti_vars['REMOTE_PORT']))
            except:
                pass

            try:
                sock.connect(server_address)

                # Send data
                sock.sendall(message + "\n")
            
                data = sock.recv(1024)

            except:
                self.ti_vars[response] = '_FAIL_'

                self.store(caller_guid)
                return bytearray("!ERROR!")
                
                
            finally:
                sock.close()
                
                self.ti_vars[response] = data

            self.store(caller_guid)   # Write our vars to our local file

            return bytearray(self.ti_vars[response])

        elif action == 'R':   # Read!
            if str(var_key) in self.ti_vars and len(str(self.ti_vars[str(var_key)])):  # str() is necessary because var_key is an unhashable bytearray. If not forced to string: "TypeError: unhashable type: 'bytearray'"
                
                # Need to check to see if variable is queued, uses ASCII 30 (Record Separator) to delimit.
                # If so, we want to pop off the first one and return it.

                if chr(0x1e) in str(self.ti_vars[str(var_key)]):
                    items = str(self.ti_vars[str(var_key)]).split(chr(0x1e))
                    
                    first_item = items.pop(0)
                    
                    self.ti_vars[str(var_key)] = chr(0x1e).join(items)

                    self.store(caller_guid)
                    
                    return bytearray(first_item)
                    
                else:                    
                    response = self.ti_vars[str(var_key)]
                    
                    if '.RESP' in str(var_key):
                        self.ti_vars[str(var_key)] = ''
                    
                    self.store(caller_guid)
    
                    return bytearray(response)

            else:
                return bytearray("!ERROR!")
            
        return bytearray()
                

    def store(self, caller_guid):

        # Create runtime directory if it doesn't exist:
        if not os.path.exists(runtime_dir):
            try:
                os.makedirs(runtime_dir)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise

        # Write out the variables file

        f = open(runtime_dir + str(caller_guid), "w")
        
        for key, val in self.ti_vars.items():
            f.write(key + "\t" + str(val) + "\n")
            
        f.close()        
        

    def handle(self, bytes):
        # Handle all tipi_io here, so main logic is just dealing with bytes in and out
        message = self.tipi_io.receive()
        self.tipi_io.send(self.processRequest(message))

        return True


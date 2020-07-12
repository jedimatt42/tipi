# TipiVariable.py
#
# ElectricLab
# Class to support "Network Variables"
#

import struct
import fcntl
import os
import errno
import re
import sys
import socket
import logging

logger = logging.getLogger(__name__)

runtime_dir = "/home/tipi/.tipivars/"


class TipiVariable(object):
    def __init__(self, tipi_io):
        self.tipi_io = tipi_io

    def processRequest(self, message):
        logger.info(f'request: {message}')
        # Now that we have message, let's parse it:
        ti_message = str(message, 'latin1').split(chr(0x1E))

        caller_guid = ti_message[0] if len(ti_message) >= 1 else ""  # Program's GUID
        context = (
            ti_message[1] if len(ti_message) >= 2 else ""
        )  # optional context, used when storing on myti99.com. Does Not Apply locally.
        action = (
            ti_message[2] if len(ti_message) >= 3 else ""
        )  # 'R', 'RS', 'W', 'U', 'T'   read, read-simple, write, transmit via UDP, transmit via TCP
        queue = (
            ti_message[3] if len(ti_message) >= 4 else ""
        )  # Allow values to queue for these variables. (only locally for now)
        results_var = (
            ti_message[4] if len(ti_message) >= 5 else ""
        )  # results_var (optional)
        var_key1 = ti_message[5] if len(ti_message) >= 6 else ""  # var key
        var_val1 = ti_message[6] if len(ti_message) >= 7 else ""  # var val
        var_key2 = ti_message[7] if len(ti_message) >= 8 else ""  # var key
        var_val2 = ti_message[8] if len(ti_message) >= 9 else ""  # var val
        var_key3 = ti_message[9] if len(ti_message) >= 10 else ""  # var key
        var_val3 = ti_message[10] if len(ti_message) >= 11 else ""  # var val
        var_key4 = ti_message[11] if len(ti_message) >= 12 else ""  # var key
        var_val4 = ti_message[12] if len(ti_message) >= 13 else ""  # var val
        var_key5 = ti_message[13] if len(ti_message) >= 14 else ""  # var key
        var_val5 = ti_message[14] if len(ti_message) >= 15 else ""  # var val
        var_key6 = ti_message[15] if len(ti_message) >= 16 else ""  # var key
        var_val6 = ti_message[16] if len(ti_message) >= 17 else ""  # var val

        response = results_var if len(results_var) else ""

        # Load our existing variables into a dict:
        self.ti_vars = {}
        self.ti_global = {}

        guid_file = runtime_dir + caller_guid
        global_file = runtime_dir + "GLOBAL"

        if os.path.isfile(str(guid_file)):
            with open(str(guid_file), "r") as f:
                for line in f:
                    line = line.rstrip(
                        "\n\r"
                    )  # Strip newlines, but not whitespace (which is what rstrip() alone will do)
                    data = line.split(chr(0x1D))

                    if len(data) > 1:
                        self.ti_vars[data[0]] = data[1]

            f.close

        if os.path.isfile(global_file):
            with open(global_file, "r") as f:
                for line in f:
                    line = line.rstrip(
                        "\n\r"
                    )  # Strip newlines, but not whitespace (which is what rstrip() alone will do)

                    data = line.split(chr(0x1D))

                    if len(data) > 1:
                        self.ti_global[data[0]] = data[1]

            f.close

        if action == "W" or action == "U" or action == "T":  # Write!
            self.ti_vars[response] = ""  # Blank out our old response

            var_val1 = var_val1.rstrip()
            self.ti_vars[str(var_key1)] = str(var_val1)

            var_val2 = var_val2.rstrip()
            self.ti_vars[str(var_key2)] = str(var_val2)

            var_val3 = var_val3.rstrip()
            self.ti_vars[str(var_key3)] = str(var_val3)

            var_val4 = var_val4.rstrip()
            self.ti_vars[str(var_key4)] = str(var_val4)

            var_val5 = var_val5.rstrip()
            self.ti_vars[str(var_key5)] = str(var_val5)

            var_val6 = var_val6.rstrip()
            self.ti_vars[str(var_key6)] = str(var_val6)

            self.store(caller_guid)  # Write our vars to our local file

        if action == "U":  #   TX via UDP    NOT COMPLETE!
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            server_address = (
                self.ti_vars["REMOTE_HOST"],
                int(self.ti_vars["REMOTE_PORT"]),
            )

            sock.close()

            self.store(caller_guid)  # Write our vars to our local file

        elif action == "T":  #   TX via TCP
            if (
                "REMOTE_HOST" not in self.ti_global
                or "REMOTE_PORT" not in self.ti_global
            ):
                logger.error("REMOTE HOST NOT SET")
                return bytearray("0" + chr(0x1E) + "ERROR", 'latin1')

            self.ti_vars[response] = ""  # Blank out our old response

            # Listener on 9918 expects:
            # prog_guid
            # session_id
            # app_id
            # context (Optional)
            # action
            # var
            # val
            #

            tmp = []

            try:
                session_id = self.ti_global["SESSION_ID"]
            except:
                session_id = ""

            tmp = [str(caller_guid), str(session_id), str(context), str(action)]

            if var_key1:
                tmp.append(str(var_key1))
                tmp.append(str(var_val1))
            if var_key2:
                tmp.append(str(var_key2))
                tmp.append(str(var_val2))
            if len(var_key3):
                tmp.append(str(var_key3))
                tmp.append(str(var_val3))
            if len(var_key4):
                tmp.append(str(var_key4))
                tmp.append(str(var_val4))
            if len(var_key5):
                tmp.append(str(var_key5))
                tmp.append(str(var_val5))
            if len(var_key5):
                tmp.append(str(var_key6))
                tmp.append(str(var_val6))

            message = chr(0x1E).join(tmp)

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            try:
                server_address = (
                    self.ti_global["REMOTE_HOST"],
                    int(self.ti_global["REMOTE_PORT"]),
                )
            except:
                pass

            try:
                sock.connect(server_address)

                # Send data
                sock.sendall(bytearray(message + "\n", 'latin1'))

                data = sock.recv(1024)
                data = str(data, 'latin1')

                if (
                    'File "' in data or "Traceback" in data
                ):  # BAD! Usually means compilation error on far end, esp when running via inetd.
                    return bytearray("0" + chr(0x1E) + "ERROR", 'latin1')

            except:
                logger.exception('server error')
                self.ti_vars[response] = "ERROR"

                self.store(caller_guid)
                return bytearray("0" + chr(0x1E) + "ERROR", 'latin1')

            finally:
                sock.close()

                self.ti_vars[response] = data

            self.store(caller_guid)  # Write our vars to our local file

            return bytearray("1" + chr(0x1E) + self.ti_vars[response], 'latin1')

        elif (
            action == "R" or action == "RS"
        ):  # Read!   'RS' is "READ SIMPLE" which will just return the value, not preceeded by return code. Better for BASIC!
            if str(var_key1) in self.ti_vars and len(
                str(self.ti_vars[str(var_key1)])
            ):  # str() is necessary because var_key is an unhashable bytearray. If not forced to string: "TypeError: unhashable type: 'bytearray'"
                # Need to check to see if variable is queued, uses ASCII 31 (Unit Separator) to delimit.
                # If so, we want to pop off the first one and return it.
                if chr(0x1E) in str(self.ti_vars[str(var_key1)]):
                    items = self.ti_vars[str(var_key1)].split(chr(0x1E))

                    first_item = items.pop(0)

                    self.ti_vars[str(var_key1)] = chr(0x1E).join(items)

                    self.store(caller_guid)

                    if action == "R":
                        return bytearray("1" + chr(0x1E) + first_item, 'latin1')
                    else:
                        return bytearray(first_item, 'latin1')

                else:
                    response = self.ti_vars[str(var_key1)]

                    if ".RESP" in str(var_key1):
                        self.ti_vars[str(var_key1)] = ""

                    self.store(caller_guid)

                    if action == "R":
                        return bytearray("1" + chr(0x1E) + response, 'latin1')
                    else:
                        return bytearray(response, 'latin1')

            else:
                if action == "R":
                    return bytearray("0" + chr(0x1E) + "ERROR", 'latin1')
                else:
                    return bytearray("ERROR", 'latin1')

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
            if len(key) and len(val):
                f.write(key + chr(0x1D) + str(val) + "\n")

        f.close()

    def handle(self, bytes):
        # Handle all tipi_io here, so main logic is just dealing with bytes in and out
        message = self.tipi_io.receive()
        response = self.processRequest(message)
        self.tipi_io.send(response)

        return True

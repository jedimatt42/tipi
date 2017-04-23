# route.py
#
# TIPI web administration
#
# Corey J. Anderson ElectricLab.com 2017
#

from __future__ import print_function
from flask import *
from functools import wraps
from flask import Markup
from ti_files import ti_files
from tinames import tinames
import sys
import Cookie
import datetime
import socket
import os.path
import glob
import fnmatch
import os, time
import ntpath
import traceback

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)



app = Flask(__name__)

webpage_object = {}       # Object we'll be passing to render_template

@app.route('/images/<path:path>')
def staticImages(path):
    return send_from_directory('images', path)

@app.route('/fonts/<path:path>')
def staticFonts(path):
    return send_from_directory('fonts', path)

@app.route('/css/<path:path>')
def staticCss(path):
    return send_from_directory('css', path)

@app.route('/js/<path:path>')
def staticJs(path):
    return send_from_directory('js', path)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def home(path):

    tipi_files = []

    tipi_root = "/home/tipi/tipi_files/"
    basepath = "{}{}".format(tipi_root,path)

    # Produce the TI PATH string (TIPI.DIR1.DIR2.ETC)
    current_path = "TIPI.{}".format('.'.join(path.split('/')))
    tmpurl = "/"
    steps = [ { 'name' : "TIPI", 'url' : tmpurl } ]
    for d in list(filter(lambda x : len(x) > 0, path.split('/'))):
        tmpurl = "{}{}/".format(tmpurl, d)
        steps += [ { 'name' : d, 'url' : tmpurl } ]
    webpage_object['steps'] = steps

    # fetch and sort just the directories and the TIFILES
    files = sorted(list(filter(lambda x : os.path.isdir(os.path.join(basepath,x)), os.listdir(basepath))))
    files += sorted(list(filter(lambda x : ti_files.isTiFile(str(os.path.join(basepath,x))), os.listdir(basepath))))

    for file_name in files:

        fullpath = os.path.join(basepath, file_name)
        bytes = None
        if not os.path.isdir(fullpath):
            try: 
                fh = open(fullpath, 'rb')
                bytes = bytearray(fh.read())
                fh.close() 
            except:
                traceback.print_exc()
                pass
        
        # create the root based url path for directory links
        webpath = "{}/{}".format(path, file_name)
        if not webpath.startswith("/"):
            webpath = "/{}".format(webpath)

        reclen = "" if bytes == None or ti_files.isProgram(bytes) else ti_files.recordLength(bytes)
        type = "directory" if bytes == None else ti_files.flagsToString(bytes)
        if type != "PROGRAM" and type != "directory":
            type = "{} {}".format(type, reclen)

        tipi_files.append( { 'name'      : tinames.asTiShortName(file_name), 
                             'webpath'   : webpath,
                             'type'      : type,
                             'size'      : 2 if bytes == None else ti_files.byteLength(bytes),
                             'date'      : time.ctime(os.path.getmtime(fullpath)),
                             'full_path' : fullpath,
                           }
                        )

    webpage_object['tipi_files'] = tipi_files
    webpage_object['total_files'] = len(tipi_files) 
    webpage_object['current_path'] = current_path

    return render_template('home.html', webpage_object=webpage_object, tipi_files=tipi_files)


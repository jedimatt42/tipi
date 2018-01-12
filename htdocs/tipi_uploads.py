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
import os, time, errno
import socket
import glob
import fnmatch
import ntpath
import traceback
import tempfile
import uuid
from subprocess import call
import re

tipi_disk_base = '/home/tipi/tipi_disk' 

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
    
    # Should instead use this since it will work with python 3 too: sys.stderr.write("error!\n"); 



app = Flask(__name__)

webpage_object = {}       # Object we'll be passing to render_template


@app.route('/images/<path:path>')
def send_image(path):
    return send_from_directory('images', path)
    

@app.route('/twbs/<path:path>')   # What does twbs stand for??????
def staticFonts(path):
    return send_from_directory('twbs', path)


@app.route('/')
def home():
    return render_template('home.html', webpage_object=webpage_object)


@app.route('/uploadFile', methods=['POST'])
def upload_file():
    file = request.files['upload_file']
    file_name = file.filename
    
    rp = request.form.get('rp')
    path = request.form.get('path')
    
    file.save(tipi_disk_base + '/' + path + '/' + file_name)

    return redirect(rp)


@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)


@app.route('/files', defaults = {'path': ''}, methods=['GET', 'POST'])
@app.route('/files/<path:path>')
def files(path):
    tipi_subdirs = []
    tipi_files = []

    if request.args.get('newDir'):
        eprint("newDir", request.args.get('newDir'))
        eprint("filePath", request.args.get('filePath'))
        
        # Need to sanitize these !!!
        newDir = request.args.get('newDir')
        filePath = request.args.get('filePath')
    
        try:
            os.makedirs(tipi_disk_base + filePath + '/' + newDir)  # Danger! Danger!
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

    if request.args.get('action') == 'download':
        eprint("wants to download!")
        
        eprint("path ", path)
        
        file_path = tipi_disk_base + '/' + path
        
        eprint("file_path: ", file_path)
        
        return send_from_directory(directory = os.path.dirname(file_path), filename = os.path.basename(file_path))

    #
    # Add a link to go back up a directory:
    #
    if len(path):
        rel_path = path
    
        p = rel_path.split('/')
        
        p = p[:-1]
        
        new_path = '/'.join(p)
    
        if len(new_path):
            new_path = '/' + new_path
    
        tipi_subdirs.append( { 'icon' : '<div class="tooltip"><a href="/files%s"><img src="/images/dots.png" width=16 border=0 alt="Go to parent directory"></a> &nbsp; <span class="tooltiptext">Return to parent directory</span></div>' % new_path,
                             }
                           )
   
    full_path = tipi_disk_base
    
    if len(path):
        full_path += '/' + path
    
    for item in sorted(os.listdir(full_path)):
        item_path = os.path.join(full_path, item)
        
        if os.path.isdir(item_path):
            item_display_path = item
            
            if len(path):
                item = path + '/' + item

            item = '/' + item
        
            tipi_subdirs.append( { 'name'      : item_display_path,
                                   #'type'      : 'subdir',
                                   'icon'   : '<a href="/files%s"><img src="/images/folder_icon.png" width=22 border=0></a>' %item,
                                 }
                               )

        else:
            # Determine file type:
            #
            icon = ''
            type = ''
            edit_link = ''
            dl_link = ''
            
            if ti_files.isTIBasicPrg(item_path):
                icon = '<img src="/images/BASIC.png" width=36>'
                type = 'TI'
                edit_link = '<a href="/edit_basic_file?file_name=' + path + '/' + item + '&rp=/files/' + path + '">Edit</a>'
                dl_link = '<a href="/files/' + path + '/' + item + '?action=download">Download</a>'
            
            elif ti_files.isTiFile(item_path):
                icon = '<img src="/images/ti_logo_icon.jpg" width=22>'
                type = 'TI'
                
            else:
                icon = '<img src="/images/clearpixel.gif" width=30>'
                type = ' '
            
            
            if item_path.endswith('.b99'):
                edit_link = '<a href="/edit_b99_file?file_name=' + path + '/' + item + '&rp=/files/' + path + '">Edit</a>'
        
            tipi_files.append( { 'name'      : item,
                                 'size'      : os.stat(item_path).st_size,
                                 # 'date'      : time.ctime(os.path.getmtime(item_path)),
                                 'date'      : time.strftime("%b %d %Y %H:%M:%S", time.gmtime(os.path.getmtime(item_path))),
                                 'icon'      : icon,
                                 'edit_link' : edit_link,
                                 'dl_link'   : dl_link,
                                 
                                 'type'      : type,
                               #  'full_path' : os.path.join(root, file_name),
                               }
                             )

    tipi_dir_listing = tipi_subdirs
    tipi_dir_listing.extend(tipi_files)

    return render_template('files.html', tipi_dir_listing=tipi_dir_listing, total_files = len(tipi_files), display_path = '/' + path, rp = '/files/' + path, path = path)


@app.route('/edit_b99_file', methods=['GET', 'POST'])
def edit_b99_file():

    status_message = ''

    edit_file_path = tipi_disk_base + '/' + request.args.get('file')
    rp = request.args.get('rp')
    
    if request.form.get('action') == 'save_b99_file' or request.args.get('action') == 'save_b99_file':
        file_contents = request.form.get('file_contents')

        file_name = request.form.get('file_name')  # Yeah, need to sanitize this, esp if this stuff runs as root!
 
        file = open(tipi_disk_base + '/' + file_name, 'w') 
        file.write(file_contents)
        file.close()
    
        status_message = '/' + file_name + ' Saved, ' + str(os.stat(tipi_disk_base + '/' + file_name).st_size) + ' bytes written'
        
        # Attempt to convert to TI's binary format:  (Needs validation)
        #
        binary_file_name = os.path.splitext(file_name)[0]
        

    with open(tipi_disk_base + '/' + request.args.get('file'), 'r') as content_file:
        file_contents = content_file.read()

    return render_template('edit_b99_file.html', file_contents=file_contents, file_name = request.args.get('file'), rp = rp, status_message = status_message )
    


@app.route('/edit_basic_file', methods=['GET', 'POST'])
def edit_basic_file():

    status_message = ''

    if request.args.get('rp'):
        rp = request.args.get('rp')
    elif request.form.get('rp'):
        rp = request.form.get('rp')

    if request.form.get('file_name'):
        edit_file_path = tipi_disk_base + '/' + request.form.get('file_name')
    elif request.args.get('file_name'):
        edit_file_path = tipi_disk_base + '/' + request.args.get('file_name')

    
    
    if request.form.get('action') == 'save_basic_file' or request.args.get('action') == 'save_basic_file':
        eprint("action is save_basic_file")
        file_contents = request.form.get('file_contents')
        
        file_name = request.form.get('file_name')  # Need to sanitize this and other user-supplied fields.
        
        eprint("file_name: ", file_name)
 
        bas_tmp_file = '/tmp/' + str(uuid.uuid4()) + '.tmp'
        prg_tmp_file = '/tmp/' + str(uuid.uuid4()) + '.tmp'
 
        file = open(bas_tmp_file, 'w') 
        file.write(file_contents)
        file.close()
                
        # Encode ASCII file to TI's binary BASIC format:
        #
        call(['xbas99.py', '-c', bas_tmp_file, '-o', prg_tmp_file])

        # Now convert to TIFILES format:
        #
        call(['xdm99.py', '-T', prg_tmp_file, '-o', tipi_disk_base + '/' + file_name])

        status_message = '/' + file_name + ' Saved, ' + str(os.stat(tipi_disk_base + '/' + file_name).st_size) + ' bytes written'
        
        if re.match(r"^\/files", rp) is None:  # Still necessary?
            rp = '/files' + rp

        if (request.form.get('saveAndExit')):
            return redirect(rp)

            
    if request.form.get('action') == 'create_new_basic_file' or request.args.get('action') == 'create_new_basic_file':
        eprint("action is create_new_basic_file")
        eprint("create new BASIC file!!!")
        
        file_name = request.form.get('path') + '/' + request.form.get('file')
        
        status_message = 'New BASIC File'
        file_contents = ''

        
    else:  # We're editing an existing file
        # First try decoding the file (non-FIAD format):
        #
        
        if request.args.get('file_name'):
            file_name = request.args.get('file_name')
        elif request.form.get('file_name'):     
            file_name = request.form.get('file_name')

        bas_tmp_file = '/tmp/' + str(uuid.uuid4()) + '.tmp'
    
        call(['xbas99.py', '-d', edit_file_path, '-o', bas_tmp_file])
        
        with open(bas_tmp_file, 'r') as f:
            line = f.readline()
        
        if re.match(r"^\d+\s\w+", line) is not None:
            with open(bas_tmp_file, 'r') as content_file:
                file_contents = content_file.read()
    
        else:
            # Extract the the BASIC program from the TIFILES format into a temp file:
            #
            prg_tmp_file = '/tmp/' + str(uuid.uuid4()) + '.tmp'
            bas_tmp_file = '/tmp/' + str(uuid.uuid4()) + '.tmp'
            
            call(['xdm99.py', '-P', edit_file_path, '-o', prg_tmp_file])   # print contents of file in FIAD format
        
            # Decode the file:
            #
            call(['xbas99.py', '-d', prg_tmp_file, '-o', bas_tmp_file])
            
            with open(bas_tmp_file, 'r') as content_file:
                file_contents = content_file.read()
            
    return render_template('edit_basic_file.html', file_contents=file_contents, file_name = file_name, rp = rp, status_message = status_message )
    





@app.route('/about', methods=['GET', 'POST'])
def about():

    return render_template('about.html', webpage_object=webpage_object, )


@app.route('/rebootnow', methods=['GET'])
def rebootnow():

    with open("/tmp/tipireboot", 'w') as reboot_trigger:
        reboot_trigger.write("tipi")

    return render_template('reboot.html', webpage_object=webpage_object )

@app.route('/shutdownnow', methods=['GET'])
def shutdownnow():

    with open("/tmp/tipihalt", 'w') as reboot_trigger:
        reboot_trigger.write("tipi")

    return render_template('shutdown.html', webpage_object=webpage_object )







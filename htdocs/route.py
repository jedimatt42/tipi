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
import os, time
import socket
# import os.path
import glob
import fnmatch
import ntpath
import traceback
import tempfile
import uuid
from subprocess import call
import re

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)



app = Flask(__name__)

webpage_object = {}       # Object we'll be passing to render_template


@app.route('/images/<path:path>')
def send_image(path):
    return send_from_directory('images', path)
    
    
    
    
    



@app.route('/twbs/<path:path>')   # What does twbs stand for??????
def staticFonts(path):
    return send_from_directory('twbs', path)

#@app.route('/', defaults={'path': ''})


@app.route('/')
def home():

    return render_template('home.html', webpage_object=webpage_object)




@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)

@app.route('/files', defaults = {'path': ''})
@app.route('/files/<path:path>')
def files(path):
    tipi_subdirs = []
    tipi_files = []

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
    
    
        tipi_subdirs.append( { 'icon' : '<div class="tooltip"><a href="/files%s"><img src="/images/dots.png" width=20 border=0 alt="Go to parent directory"></a> &nbsp; <span class="tooltiptext">Return to parent directory</span></div>' % new_path,
                             }
                           )
   
    full_path = '/tipi_disk' 
    
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
            
            if ti_files.isTIBasicPrg(item_path):
                icon = '<img src="/images/BASIC.png" width=36>'
                type = 'TI'
                edit_link = '<a href="/edit_basic_file?file=' + path + '/' + item + '&rp=/files/' + path + '">Edit</a>'            
            
            elif ti_files.isTiFile(item_path):
                icon = '<img src="/images/ti_logo_icon.jpg" width=22>'
                type = 'TI'
                
            else:
                icon = '<img src="/images/clearpixel.gif" width=30>'
                type = ' '
            
            
            if item_path.endswith('.b99'):
                edit_link = '<a href="/edit_b99_file?file=' + path + '/' + item + '&rp=/files/' + path + '">Edit</a>'
        
            tipi_files.append( { 'name'      : item,
                                 'size'      : os.stat(item_path).st_size,
                                 # 'date'      : time.ctime(os.path.getmtime(item_path)),
                                 'date'      : time.strftime("%b %d %Y %H:%M:%S", time.gmtime(os.path.getmtime(item_path))),
                                 'icon'      : icon,
                                 'edit_link' : edit_link,
                                 
                                 'type'      : type,
                               #  'full_path' : os.path.join(root, file_name),
                               }
                             )

    tipi_dir_listing = tipi_subdirs
    tipi_dir_listing.extend(tipi_files)

    return render_template('files.html', tipi_dir_listing=tipi_dir_listing, total_files = len(tipi_files), display_path = '/' + path, rp = '/' + path)


@app.route('/edit_b99_file', methods=['GET', 'POST'])
def edit_b99_file():

    status_message = ''

    edit_file_path = '/tipi_disk/' + request.args.get('file')
    rp = request.args.get('rp')
    
    if request.form.get('action') == 'save_b99_file' or request.args.get('action') == 'save_b99_file':
        file_contents = request.form.get('file_contents')

        file_name = request.form.get('file_name')  # Yeah, need to sanitize this, esp if this stuff runs as root!
 
        file = open('/tipi_disk/' + file_name, 'w') 
        file.write(file_contents)
        file.close()
    
        status_message = '/' + file_name + ' Saved, ' + str(os.stat('/tipi_disk/' + file_name).st_size) + ' bytes written'
        
        # Attempt to convert to TI's binary format:  (Needs validation)
        #
        binary_file_name = os.path.splitext(file_name)[0]
        

    with open('/tipi_disk/' + request.args.get('file'), 'r') as content_file:
        file_contents = content_file.read()

    return render_template('edit_b99_file.html', file_contents=file_contents, file_name = request.args.get('file'), rp = rp, status_message = status_message )
    


@app.route('/edit_basic_file', methods=['GET', 'POST'])
def edit_basic_file():

    status_message = ''

    edit_file_path = '/tipi_disk/' + request.args.get('file')
    rp = request.args.get('rp')
    
    if request.form.get('action') == 'save_basic_file' or request.args.get('action') == 'save_basic_file':
        file_contents = request.form.get('file_contents')
        
        file_name = request.form.get('file_name')  # Yeah, need to sanitize this, esp if this stuff runs as root!
 
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
        call(['xdm99.py', '-T', prg_tmp_file, '-o', '/tipi_disk/' + file_name])

        status_message = '/' + file_name + ' Saved, ' + str(os.stat('/tipi_disk/' + file_name).st_size) + ' bytes written'

    # First try decoding the file (non-FIAD format):
    #
    bas_tmp_file = '/tmp/' + str(uuid.uuid4()) + '.tmp'

    call(['xbas99.py', '-d', edit_file_path, '-o', bas_tmp_file])
    
    with open(bas_tmp_file, 'r') as f:
        line = f.readline()
    
    if re.match(r"^\d+\s\w+", line) is not None:

        with open(bas_tmp_file, 'r') as content_file:
            file_contents = content_file.read()

        return render_template('edit_basic_file.html', file_contents=file_contents, file_name = request.args.get('file'), rp = rp, status_message = status_message )

    

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

    return render_template('edit_basic_file.html', file_contents=file_contents, file_name = request.args.get('file'), rp = rp, status_message = status_message )
    



















@app.route('/about', methods=['GET', 'POST'])
def about():

    return render_template('about.html', webpage_object=webpage_object, )









# tipi_editor
#
# TIPI web administration
#
# Corey J. Anderson ElectricLab.com 2017
# et al.

import os
import logging
import uuid
from ti_files import ti_files
from subprocess import call

logger = logging.getLogger(__name__)

tipi_disk_base = '/home/tipi/tipi_disk' 

def load(file_name):
    edit_file_path = os.path.join(tipi_disk_base, file_name)
    file_contents = basicContents(edit_file_path)

    editor_data = { 'file_contents': file_contents, 
                    'file_name': file_name,
                    'status_message': '' }
    return editor_data

def whatever():

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


def basicContents(filename):
    logger.debug("fetching BASIC PROGRAM as ascii in %s", filename)
    # We are assuming the test for FIAD isTiFile has already passed.

    prg_tmp_file = '/tmp/' + str(uuid.uuid4()) + '.tmp'
    bas_tmp_file = '/tmp/' + str(uuid.uuid4()) + '.tmp'

    try:
        # strip the FIAD header off to get the raw file xbas99 needs.
        with open(filename, "rb") as tifile:
            with open(prg_tmp_file, "wb") as program:
                bytes = bytearray(tifile.read())
                if not ti_files.isProgram(bytes):
                    return False
                program.write(bytes[128:])

        call(['/home/tipi/xdt99/xbas99.py', '-d', prg_tmp_file, '-o', bas_tmp_file]) 

        if ti_files.isTiBasicAscii(bas_tmp_file):
            with open(bas_tmp_file, 'rb') as content_file:
                return content_file.read()

    finally:
        if os.path.exists(prg_tmp_file):
            os.unlink(prg_tmp_file)
        if os.path.exists(bas_tmp_file):
            os.unlink(bas_tmp_file)

    return False



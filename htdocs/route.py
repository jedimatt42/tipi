# route.py
#
# TIPI web administration
#
# Corey J. Anderson ElectricLab.com 2017
# et al.

import logging
import tipi_admin
import tipi_editor
import tipi_files
import tipi_uploads

from flask import *

app = Flask(__name__)

#
# Static resources
#

@app.route('/images/<path:path>')
def send_image(path):
    return send_from_directory('images', path)
    
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)

#
# File management
#

@app.route('/files', defaults = {'path': ''}, methods=['GET'])
@app.route('/files/<path:path>')
def files(path):
    catalog = tipi_files.catalog(path)
    return render_template('files.html', **catalog)

@app.route('/uploadFile', methods=['POST'])
def upload_file():
    rp = request.form.get('rp')
    uploads.save(request.form.get('path'), request.files['upload_file'])
    return redirect(rp)

#
# Text editor
#

@app.route('/edit_basic_file', methods=['GET'])
def edit_basic_file():
    file_data = editor.load(request.form.get('path'))
    return render_template('edit_basic_file.html', file_data)

@app.route('/save_basic_file', methods=['POST'])
def save_basic_file():
    # probably wrong... files is attachements, and the big text box is problably
    # just a form field....
    rp = editor.save(request.form.get('path'), request.files['upload_file'])
    return redirect(rp)

#
# Tipi Admin
#

@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')

@app.route('/rebootnow', methods=['GET'])
def rebootnow():
    tipi_admin.reboot()
    return render_template('reboot.html')

@app.route('/shutdownnow', methods=['GET'])
def shutdownnow():
    tipi_admin.shutdown()
    return render_template('shutdown.html')


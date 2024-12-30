# route.py
#
# TIPI web administration
#
# Corey J. Anderson ElectricLab.com 2017
# Matthew Splett jedimatt42.com

from ConfigLogging import configure_logging

import string
import tipi_admin
import tipi_backup
import tipi_editor
import tipi_emulation
import tipi_files
import tipi_uploads
import tipi_map
import pi_config
import os
from flask_socketio import SocketIO

from flask import *
import logging

configure_logging()

logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["TESTING"] = False
app.config["ENV"] = "development"
socketio = SocketIO(app)

#
# sqlite3 concession
#
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


#
# Static resources
#


@app.route("/images/<path:path>")
def send_image(path):
    return send_from_directory("images", path)


@app.route("/")
def home():
    rp = createFileUrl("/")
    return redirect(rp)


@app.route("/css/<path:path>")
def send_css(path):
    return send_from_directory("css", path)


@app.route("/mdb/<path:path>")
def send_mdb5(path):
    return send_from_directory("mdb5s", path)


#
# File management
#


@app.route("/<path:path>", methods=["GET"])
def download(path):
    localpath = tipi_files.download(path)
    resp = make_response(
        send_from_directory(localpath["directory"], localpath["filename"])
    )
    resp.cache_control.no_store = True
    resp.cache_control.public = False
    resp.cache_control.max_age = None
    del(resp.headers['Content-Encoding'])
    return resp


@app.route("/files", defaults={"path": ""}, methods=["GET"])
@app.route("/files/<path:path>", methods=["GET"])
def files(path):
    catalog = tipi_files.catalog(path)
    return render_template("files.html", **catalog)


@app.route("/uploadFile", methods=["POST"])
def upload_file():
    path = request.form.get("path")
    tipi_uploads.save(path, request.files.getlist("upload_file"))
    rp = createFileUrl(path)
    return redirect(rp)


@app.route("/newdir", methods=["POST"])
def newdir():
    path = request.form.get("path")
    newdir = request.form.get("newdir")
    tipi_files.newdir(path, newdir)
    rp = createFileUrl(path)
    return redirect(rp)


@app.route("/delete", methods=["POST"])
def deleteSelected():
    path = request.form.get("path")
    files = request.form.getlist("selected")
    tipi_files.deleteAll(path, files)
    rp = createFileUrl(path)
    return redirect(rp)


@app.route("/tifiles", methods=["POST"])
def convert():
    path = request.form.get("path")
    files = request.form.getlist("selected")
    tipi_files.convert(path, files)
    rp = createFileUrl(path)
    return redirect(rp)


@app.route("/mapdsk1", methods=["POST"])
def mapdsk1():
    path = request.form.get("path")
    files = request.form.getlist("selected")
    tipi_map.mapdrive("DSK1_DIR", path, files)
    rp = createFileUrl(path)
    return redirect(rp)


@app.route("/mapdsk2", methods=["POST"])
def mapdsk2():
    path = request.form.get("path")
    files = request.form.getlist("selected")
    tipi_map.mapdrive("DSK2_DIR", path, files)
    rp = createFileUrl(path)
    return redirect(rp)


@app.route("/mapdsk3", methods=["POST"])
def mapdsk3():
    path = request.form.get("path")
    files = request.form.getlist("selected")
    tipi_map.mapdrive("DSK3_DIR", path, files)
    rp = createFileUrl(path)
    return redirect(rp)


@app.route("/mapdsk4", methods=["POST"])
def mapdsk4():
    path = request.form.get("path")
    files = request.form.getlist("selected")
    tipi_map.mapdrive("DSK4_DIR", path, files)
    rp = createFileUrl(path)
    return redirect(rp)


@app.route("/mapdsk5", methods=["POST"])
def mapdsk5():
    path = request.form.get("path")
    files = request.form.getlist("selected")
    tipi_map.mapdrive("DSK5_DIR", path, files)
    rp = createFileUrl(path)
    return redirect(rp)


@app.route("/mapdsk6", methods=["POST"])
def mapdsk6():
    path = request.form.get("path")
    files = request.form.getlist("selected")
    tipi_map.mapdrive("DSK6_DIR", path, files)
    rp = createFileUrl(path)
    return redirect(rp)


@app.route("/mapdsk7", methods=["POST"])
def mapdsk7():
    path = request.form.get("path")
    files = request.form.getlist("selected")
    tipi_map.mapdrive("DSK7_DIR", path, files)
    rp = createFileUrl(path)
    return redirect(rp)


@app.route("/mapdsk8", methods=["POST"])
def mapdsk8():
    path = request.form.get("path")
    files = request.form.getlist("selected")
    tipi_map.mapdrive("DSK8_DIR", path, files)
    rp = createFileUrl(path)
    return redirect(rp)


@app.route("/mapdsk9", methods=["POST"])
def mapdsk9():
    path = request.form.get("path")
    files = request.form.getlist("selected")
    tipi_map.mapdrive("DSK9_DIR", path, files)
    rp = createFileUrl(path)
    return redirect(rp)


@app.route("/unmapdsk1", methods=["POST"])
def unmapdsk1():
    path = request.form.get("path")
    tipi_map.unmapdrive("DSK1_DIR")
    rp = createFileUrl(path)
    return redirect(rp)


@app.route("/unmapdsk2", methods=["POST"])
def unmapdsk2():
    path = request.form.get("path")
    tipi_map.unmapdrive("DSK2_DIR")
    rp = createFileUrl(path)
    return redirect(rp)


@app.route("/unmapdsk3", methods=["POST"])
def unmapdsk3():
    path = request.form.get("path")
    tipi_map.unmapdrive("DSK3_DIR")
    rp = createFileUrl(path)
    return redirect(rp)


@app.route("/unmapdsk4", methods=["POST"])
def unmapdsk4():
    path = request.form.get("path")
    tipi_map.unmapdrive("DSK4_DIR")
    rp = createFileUrl(path)
    return redirect(rp)


@app.route("/unmapdsk5", methods=["POST"])
def unmapdsk5():
    path = request.form.get("path")
    tipi_map.unmapdrive("DSK5_DIR")
    rp = createFileUrl(path)
    return redirect(rp)


@app.route("/unmapdsk6", methods=["POST"])
def unmapdsk6():
    path = request.form.get("path")
    tipi_map.unmapdrive("DSK6_DIR")
    rp = createFileUrl(path)
    return redirect(rp)


@app.route("/unmapdsk7", methods=["POST"])
def unmapdsk7():
    path = request.form.get("path")
    tipi_map.unmapdrive("DSK7_DIR")
    rp = createFileUrl(path)
    return redirect(rp)


@app.route("/unmapdsk8", methods=["POST"])
def unmapdsk8():
    path = request.form.get("path")
    tipi_map.unmapdrive("DSK8_DIR")
    rp = createFileUrl(path)
    return redirect(rp)


@app.route("/unmapdsk9", methods=["POST"])
def unmapdsk9():
    path = request.form.get("path")
    tipi_map.unmapdrive("DSK9_DIR")
    rp = createFileUrl(path)
    return redirect(rp)


@app.route("/unmapcs1", methods=["POST"])
def unmapcs1():
    path = request.form.get("path")
    tipi_map.unmapdrive("CS1_FILE")
    rp = createFileUrl(path)
    return redirect(rp)


@app.route("/mapcs1", methods=["POST"])
def mapcs1():
    path = request.form.get("path")
    cs1_input = request.form.get("cs1_input")
    files = request.form.getlist("selected")
    if cs1_input and not cs1_input.isspace():
        tipi_map.mapfile("CS1_FILE", cs1_input)
    else:
        tipi_map.mapfile("CS1_FILE", files[0], path=path)
    rp = createFileUrl(path)
    return redirect(rp)


#
# Text editor
#


@app.route("/edit_basic_file", methods=["GET"])
def edit_basic_file():
    file_data = tipi_editor.load(request.args.get("file_name"))
    file_data["rp"] = createFileUrl(request.args.get("path"))
    return render_template("edit_basic_file.html", **file_data)


@app.route("/save_basic_file", methods=["POST"])
def save_basic_file():
    file_data = tipi_editor.save(
        request.form.get("file_name"), request.form.get("file_contents")
    )
    rp = request.form.get("rp")
    if request.form.get("saveAndExit"):
        return redirect(rp)
    else:
        file_data["rp"] = rp
        return render_template("edit_basic_file.html", **file_data)


@app.route("/new_basic_file", methods=["POST"])
def new_basic_file():
    path = request.form.get("path")
    filename = request.form.get("file")
    file_data = tipi_editor.new(path + "/" + filename)
    file_data["rp"] = createFileUrl(path)
    return render_template("edit_basic_file.html", **file_data)


#
# Tipi Admin
#


@app.route("/about", methods=["GET", "POST"])
def about():
    version = tipi_admin.version()
    return render_template("about.html", **version)


@app.route("/logs", methods=["GET"])
def logs():
    logdata = tipi_admin.logdata()
    return render_template("log.html", **logdata)


@app.route("/oslogs", methods=["GET"])
def oslogs():
    logdata = tipi_admin.oslogdata()
    return render_template("oslog.html", **logdata)


@app.route("/rebootnow", methods=["GET"])
def rebootnow():
    tipi_admin.reboot()
    return render_template("reboot.html")


@app.route("/shutdownnow", methods=["GET"])
def shutdownnow():
    tipi_admin.shutdown()
    return render_template("shutdown.html")


# Tipi Backup


@app.route("/restorenow", methods=["POST"])
def restore_now():
    backup_file = request.form.get("backup_file")
    tipi_backup.restore_now(backup_file)
    return redirect("/backup")


@app.route("/backup", methods=["GET"])
def backup():
    backup = tipi_backup.status()
    return render_template("backup.html", **backup)


@app.route("/backupnow", methods=["POST"])
def backup_now():
    tipi_backup.backup_now()
    return redirect("/backup")


@app.route("/backupdl/<path:path>", methods=["GET"])
def backupdl(path):
    resp = make_response(
        send_from_directory("/home/tipi", os.path.basename(path))
    )
    resp.cache_control.no_store = True
    resp.cache_control.public = False
    resp.cache_control.max_age = None
    del(resp.headers['Content-Encoding'])
    return resp


@app.route("/backupul", methods=["POST"])
def backupul():
    tipi_backup.upload(request.files.getlist("upload_file"))
    return redirect("/backup")


@app.route("/delete-backup", methods=["POST"])
def delete_backup():
    backup_file = request.form.get("backup_file")
    tipi_backup.delete(backup_file)
    return redirect("/backup")


@app.route("/emulation", methods=["GET"])
def emulation():
    status = tipi_emulation.status()
    return render_template("emulation.html", **status)


@app.route("/emulation-update", methods=["POST"])
def emulation_update():
    emulation_state = { }
    emulation_state['enabled'] = request.form.get("enabled") == 'true'
    emulation_state['pdf'] = request.form.get("pdf") == "pdf"
    emulation_state['nfs'] = request.form.get("nfs") == "nfs"
    tipi_emulation.update(emulation_state)
    return redirect("/emulation")


@app.route("/piconfig", methods=["GET"])
def piconfig():
    data = pi_config.data()
    return render_template("pi_config.html", **data)


@app.route("/piconfig-update", methods=["POST"])
def piconfig_update():
    updated_config = request.form.to_dict()
    pi_config.update(updated_config)
    return render_template("pi_config_saved.html")


@app.route("/search", methods=["GET"])
def searchQuery():
    criteria = { }
    criteria['globpat'] = request.args.get("globpat")
    criteria['matchpaths'] = request.args.get("matchpaths")
    criteria['type_program'] = request.args.get("type_program")
    criteria['type_dv80'] = request.args.get("type_dv80")
    criteria['type_df80'] = request.args.get("type_df80")
    criteria['type_df128'] = request.args.get("type_df128")
    results = tipi_files.search(criteria)
    return render_template("search_result.html", **results)
    

## Utility


def createFileUrl(path):
    if path == "/" or path == "":
        return "/files"
    else:
        return f"/files/{path}".replace("//", "/")


## Launch app

if __name__ == "__main__":
    socketio.run(app, "0.0.0.0", 9900,  allow_unsafe_werkzeug=True)

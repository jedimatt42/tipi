# route.py
#
# TIPI web administration
#
# Corey J. Anderson ElectricLab.com 2017
# et al.

import string
import tipi_admin
import tipi_editor
import tipi_files
import tipi_uploads
from flask_socketio import SocketIO

from flask import *

app = Flask(__name__)
app.config["DEBUG"] = False
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


@app.route("/daemonlogs", methods=["GET"])
def daemonlogs():
    logdata = tipi_admin.daemonlogdata()
    return render_template("daemonlog.html", **logdata)


@app.route("/rebootnow", methods=["GET"])
def rebootnow():
    tipi_admin.reboot()
    return render_template("reboot.html")


@app.route("/shutdownnow", methods=["GET"])
def shutdownnow():
    tipi_admin.shutdown()
    return render_template("shutdown.html")


## Utility


def createFileUrl(path):
    if path == "/" or path == "":
        return "/files"
    else:
        return f"/files/{path}".replace("//", "/")


## Launch app

if __name__ == "__main__":
    socketio.run(app, "0.0.0.0", 9900)

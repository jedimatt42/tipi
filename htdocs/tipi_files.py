# TIPI web administration
#
# Corey J. Anderson ElectricLab.com 2017
# et al.

from ti_files import ti_files
from ti_files import v9t9_files
from tinames import tinames
from TipiConfig import TipiConfig
import os
import shutil
import time
import errno
import logging
import tipi_cache

tipi_config = TipiConfig.instance()

logger = logging.getLogger(__name__)

tipi_disk_base = "/home/tipi/tipi_disk"

icons = {
    "basic": '<img src="/images/basic_icon.png" width=22 title="BASIC PROGRAM">',
    "tifile": '<img src="/images/ti_logo_icon.jpg" width=22 title="TIFILES">',
    "native": '<img src="/images/native_icon.png" width=22 title="OS Native File">',
    "floppy": '<img src="/images/floppy.png" width=22 title="Sector Dump">',
}

download_template = '<a href="%s"><img src="/images/download_icon.png" width=32 title="Download File"/></a>'

editlink_template = '<a href="/edit_basic_file?file_name=%s&path=%s"><img src="/images/edit_icon.png" width=22 title="Edit File"/></a>'

dirlink_template = '<a href="/files%s">TIPI.%s</a>'

# this should be a form.
convlink_template = (
    '<img src="/images/convert_icon.png" width=32 title="Convert to TIFILES"/>'
)


def newdir(path, newdir):
    logger.debug("creating directory %s/%s", path, newdir)
    if "." in newdir:
        raise
    try:
        os.makedirs(tipi_disk_base + path + "/" + newdir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


def download(path):
    logger.debug("download request for %s", path)

    file_path = tipi_disk_base + "/" + path
    return {
        "directory": os.path.dirname(file_path),
        "filename": os.path.basename(file_path),
    }


def deleteAll(path, files):
    logger.debug("deleting %s from %s", files, path)

    base_path = os.path.abspath(tipi_disk_base + "/" + path)
    for f in files:
        try:
            fname = tinames.findpath(base_path, f)
            file_path = base_path + "/" + fname
            if os.path.isfile(file_path):
                os.remove(file_path)
            else:
                shutil.rmtree(file_path)
            logger.debug("Deleted %s", file_path)
        except Exception as e:
            logger.warn("Failed to delete: %s/%s", base_path, f, exc_info=1)


def convert(path, files):
    logger.debug("converting v9t9 to tifiles %s from %s", files, path)

    base_path = os.path.abspath(tipi_disk_base + "/" + path)
    for f in files:
        try:
            fname = tinames.findpath(base_path, f)
            file_path = base_path + "/" + fname
            if v9t9_files.convert(file_path):
                logger.debug("Converted %s", file_path)
            else:
                logger.debug("Did not convert %s", file_path)
        except Exception as e:
            logger.warn("Failed to convert: %s/%s", base_path, f, exc_info=1)


def mappedUrl(tipath):
    return "/files/" + tipath.replace('.', '/')


def catalog(path):
    logger.debug("generating catalog for: %s", path)
    tipi_subdirs = []
    tipi_files = []

    #
    # Add a link to go back up a directory:
    #
    if len(path):
        rel_path = path

        p = rel_path.split("/")

        p = p[:-1]

        new_path = "/".join(p)

        if len(new_path):
            new_path = "/" + new_path

    full_path = tipi_disk_base

    if len(path):
        full_path += "/" + path

    for item in sorted(os.listdir(full_path)):
        item_path = os.path.join(full_path, item)

        if os.path.isdir(item_path):
            item_display_path = item

            if len(path):
                item = path + "/" + item

            item = "/" + item

            mapping_path = item[1:].replace('/', '.')

            tipi_subdirs.append(
                {
                    "name": item_display_path,
                    "type": "DIR",
                    "icon": '<a href="/files%s"><img src="/images/folder_icon.png" width=22 border=0></a>'
                    % item,
                    "longname": None,
                    "mapname": mapping_path,
                }
            )

        else:
            fileInfo = tipi_cache.lookupFileInfo(item_path)
            tipi_files.append(fileDisplayData(fileInfo))

    tipi_dir_listing = tipi_subdirs
    tipi_dir_listing.extend(tipi_files)
    tipi_path = ("TIPI." + path.replace('/', '.') + '.') if path else "TIPI."

    return {
        "tipi_dir_listing": tipi_dir_listing,
        "total_files": len(tipi_files),
        "display_path": "/" + path,
        "tipi_path": makeBreadcrumbs(tipi_path),
        "rp": "/files/" + path,
        "path": path,
        "config": {
            "DSK1_DIR": tipi_config.get("DSK1_DIR"),
            "DSK2_DIR": tipi_config.get("DSK2_DIR"),
            "DSK3_DIR": tipi_config.get("DSK3_DIR"),
            "DSK4_DIR": tipi_config.get("DSK4_DIR"),
            "DSK1_URL": mappedUrl(tipi_config.get("DSK1_DIR")),
            "DSK2_URL": mappedUrl(tipi_config.get("DSK2_DIR")),
            "DSK3_URL": mappedUrl(tipi_config.get("DSK3_DIR")),
            "DSK4_URL": mappedUrl(tipi_config.get("DSK4_DIR")),
        },
        "mapped": { 
            tipi_config.get("DSK1_DIR"): "DSK1",
            tipi_config.get("DSK2_DIR"): "DSK2",
            tipi_config.get("DSK3_DIR"): "DSK3",
            tipi_config.get("DSK4_DIR"): "DSK4",
        },
    }


def makeBreadcrumbs(path):
    # take a string like TIPI.GAMES.EA5
    # and return a list of maps each with a link and label field
    paths = []
    link = "/files"
    for step in path.split('.')[:-1]:
        link += ("/" + step) if step != "TIPI" else ""
        paths.append({
            "label": step,
            "link": link
        })
    return paths


def fileDisplayData(fileInfo):
    item_path = fileInfo["name"]
    item = item_path.split('/')[-1]
    path = "/".join(item_path.split('/')[:-1])

    if item_path.endswith('.sectors'):
        icon = icons['floppy']
    else:
        icon = icons[fileInfo["icon"]]
    file_type = fileInfo["type"]
    tiname = fileInfo["tiname"]
    size = fileInfo["size"]
    edit_link = ""
    conv_link = ""
    date = time.strftime(
        "%b %d %Y %H:%M:%S", time.gmtime(os.path.getmtime(item_path))
    )

    dlpath = item_path.replace(tipi_disk_base, "")
    dl_link = download_template % (dlpath)
    if fileInfo["icon"] == "basic":
        edit_link = editlink_template % (dlpath, "/".join(dlpath.split("/")[:-1]))

    if fileInfo["icon"] == "native":
        conv_link = convlink_template

    if tiname != item:
        longname = item
    else:
        longname = None

    dirpath = ".".join(path.split("/")[4:])

    if dirpath:
        dir_link = dirlink_template % ('/' + dirpath.replace('.','/'), dirpath)
    else:
        dir_link = dirlink_template % ('', '')

    return {
        "icon": icon,
        "name": tiname,
        "size": size,
        "date": date,
        "edit_link": edit_link,
        "dl_link": dl_link,
        "conv_link": conv_link,
        "type": file_type,
        "longname": longname,
        "dir_link": dir_link,
    }


def search(criteria):
    logger.info("generating search for: %s", criteria)
    matching_files = tipi_cache.searchFileInfo(criteria) if criteria['globpat'] else []
    tipi_files = []
    for match in matching_files:
        tipi_files.append(fileDisplayData(match))

    return { 
        "criteria": criteria,
        "tipi_files": tipi_files,
        "total_files": len(tipi_files),
        "config": {
            "DSK1_DIR": tipi_config.get("DSK1_DIR"),
            "DSK2_DIR": tipi_config.get("DSK2_DIR"),
            "DSK3_DIR": tipi_config.get("DSK3_DIR"),
            "DSK4_DIR": tipi_config.get("DSK4_DIR"),
            "DSK1_URL": mappedUrl(tipi_config.get("DSK1_DIR")),
            "DSK2_URL": mappedUrl(tipi_config.get("DSK2_DIR")),
            "DSK3_URL": mappedUrl(tipi_config.get("DSK3_DIR")),
            "DSK4_URL": mappedUrl(tipi_config.get("DSK4_DIR")),
        },
        "mapped": { 
            tipi_config.get("DSK1_DIR"): "DSK1",
            tipi_config.get("DSK2_DIR"): "DSK2",
            tipi_config.get("DSK3_DIR"): "DSK3",
            tipi_config.get("DSK4_DIR"): "DSK4",
        },
    }


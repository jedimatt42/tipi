import os
import logging
import sqlite3
import ConfigLogging
from flask import g
from ti_files import ti_files
from tinames import tinames

#
# DOA-ish methods for cache of tipi_disk file meta-data. 
#

logger = logging.getLogger(__name__)
tipi_disk = '/home/tipi/tipi_disk'

global_conn = None
db_name = '/home/tipi/.tipiweb.db'

def get_context_conn():
    """
    Flask needs a database connection per request context, and that
    is registered to close in route.py
    """
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(db_name)
    return db

def get_mon_conn():
    """
    If not under the flask process, such as TipiMonitor.py, we can
    act in a single-threaded model, and use a global connection
    """
    global global_conn
    if not global_conn:
        global_conn = sqlite3.connect(db_name)
    return global_conn

def get_conn():
    try:
        return get_context_conn()
    except RuntimeError:
        return get_mon_conn()

def setupSchema():
    logger.info("Checking for schema")
    sql = get_conn().cursor()
    sql.execute('CREATE TABLE IF NOT EXISTS fileheader (name TEXT PRIMARY KEY, icon TEXT, type TEXT, tiname TEXT, size INTEGER, protected INTEGER)')
    get_conn().commit()
    sql.close()

def deleteAll():
    logger.info("clearing tipi_disk meta-data")
    setupSchema()
    sql = get_conn().cursor()
    sql.execute('DELETE FROM fileheader')
    get_conn().commit()
    sql.execute('VACUUM')
    get_conn().commit()
    sql.close()
    logger.debug("previous meta-data deleted.")

def addAll():
    for root, subdirs, files in os.walk(tipi_disk):
        for filename in files:
            name = os.path.join(root.decode('utf-8'), filename.decode('utf-8'))
            updateFileInfo(name)

def deleteMissing():
    cachedFiles = []
    logger.debug("finding all cached files")
    sql = get_conn().cursor()
    for row in sql.execute('SELECT name FROM fileheader'):
        cachedFiles.append(row[0])
    
    get_conn().commit()
    sql.close()

    for name in cachedFiles:
        if not os.path.exists(os.path.join(tipi_disk, name)):
            deleteFileInfo(name)

def deleteFileInfo(name):
    logger.info("Deleting cache for %s", name)
    sql = get_conn().cursor()
    try: 
        sql = get_conn().cursor()
        sqlargs = (name,)
        sql.execute('DELETE FROM fileheader WHERE name == ?', sqlargs)
        get_conn().commit()
    except Exception as e:
        logger.error("failed to delete %s", name)
    finally:
        sql.close()
        

def lookupFileInfo(name):
    sql = get_conn().cursor()
    sqlargs = (name,)
    sql.execute('SELECT * FROM fileheader WHERE name == ?', sqlargs)
    fileInfo = sql.fetchone()
    sql.close()
    if fileInfo == None:
        fileInfo = updateFileInfo(name)
    return rowToMap(fileInfo)

def rowToMap(fileInfo):
    # fileInfo is currently a positional 'tuple' which sucks... so let's make a
    # map
    return { "name": fileInfo[0],
             "icon": fileInfo[1],
             "type": fileInfo[2],
             "tiname": fileInfo[3],
             "size": fileInfo[4],
             "protected": fileInfo[5]
    }

def updateFileInfo(name):
    if os.path.isdir(name):
        return
    sqlargs = _getFileInfo(name)
    sql = get_conn().cursor()
    try:
        sql.execute('REPLACE INTO fileheader VALUES (?, ?, ?, ?, ?, ?)', sqlargs)
        get_conn().commit()
    except Exception as e:
        logger.error("could not update info for %s", name)
    finally:
        sql.close()
    return sqlargs

def searchFileInfo(globpat):
    sql = get_conn().cursor()
    sqlargs = (f"*{globpat}*",)
    sql.execute('SELECT * FROM fileheader WHERE tiname GLOB ?', sqlargs)
    allrows = sql.fetchall()
    logger.info(f"allrows: {allrows}")
    files = []
    for row in allrows:
        files.append(rowToMap(row))
    return files

def _getFileInfo(name):
    dv80suffixes = (".txt", ".a99", ".b99", ".bas", ".xb", ".tb")
    basicSuffixes = (".b99", ".bas", ".xb", ".tb")
        
    header = None
    
    with open(name,"rb") as fdata:
        header = bytearray(fdata.read())[:128]

    valid = ti_files.isValid(header)

    isprotected = 0
    icon = "native"
    type = "DIS/FIX 128"
    tiname = tinames.asTiShortName(name)
    size = os.stat(name).st_size

    if valid:
        type = ti_files.flagsToString(header) 
        if type != 'PROGRAM':
            type = type + " " + str(ti_files.recordLength(header))
        isprotected = ti_files.isProtected(header)
        icon = 'tifile'
    elif name.lower().endswith(dv80suffixes):
        type = "DIS/VAR 80"
        if name.lower().endswith(basicSuffixes):
            icon = 'basic'

    if type == 'PROGRAM' and ti_files.isTiBasicPrg(name):
        icon = 'basic'
    if type == 'INT/VAR 254' and ti_files.isTiBasicPrg(name):
        icon = 'basic'

    return (name, icon, type, tiname, size, isprotected)
    
if __name__ == '__main__':
    deleteAll()


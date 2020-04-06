import os
import logging
import sqlite3
import ConfigLogging
from ti_files import ti_files
from tinames import tinames

#
# DOA-ish methods for cache of tipi_disk file meta-data. 
#

logger = logging.getLogger(__name__)
conn = sqlite3.connect('/home/tipi/.tipiweb.db')
tipi_disk = '/home/tipi/tipi_disk'

def setupSchema():
    logger.info("Checking for schema")
    sql = conn.cursor()
    sql.execute('CREATE TABLE IF NOT EXISTS fileheader (name TEXT PRIMARY KEY, icon TEXT, type TEXT, tiname TEXT, size INTEGER, protected INTEGER)')
    conn.commit()
    sql.close()

def deleteAll():
    logger.info("clearing tipi_disk meta-data")
    setupSchema()
    sql = conn.cursor()
    sql.execute('DELETE FROM fileheader')
    conn.commit()
    sql.execute('VACUUM')
    conn.commit()
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
    sql = conn.cursor()
    for row in sql.execute('SELECT name FROM fileheader'):
        cachedFiles.append(row[0])
    
    conn.commit()
    sql.close()

    for name in cachedFiles:
        if not os.path.exists(os.path.join(tipi_disk, name)):
            deleteFileInfo(name)

def deleteFileInfo(name):
    logger.info("Deleting cache for %s", name)
    sql = conn.cursor()
    try: 
        sql = conn.cursor()
        sqlargs = (name,)
        sql.execute('DELETE FROM fileheader WHERE name == ?', sqlargs)
        conn.commit()
    except Exception as e:
        logger.error("failed to delete %s", name)
    finally:
        sql.close()
        

def lookupFileInfo(name):
    logger.debug("looking up file info for %s", name)
    sql = conn.cursor()
    sqlargs = (name,)
    sql.execute('SELECT * FROM fileheader WHERE name == ?', sqlargs)
    fileInfo = sql.fetchone()
    sql.close()
    if fileInfo == None:
        fileInfo = updateFileInfo(name)

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
    logger.info("Updating %s", name)
    if os.path.isdir(name):
        logger.debug("skipping directory")
        return
    sqlargs = _getFileInfo(name)
    sql = conn.cursor()
    try:
        sql.execute('REPLACE INTO fileheader VALUES (?, ?, ?, ?, ?, ?)', sqlargs)
        conn.commit()
    except Exception as e:
        logger.error("could not update info for %s", name)
    finally:
        sql.close()
    return sqlargs

def _getFileInfo(name):
    logger.info("Looking at %s", name)

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

    logger.info("%s is of type %s, icon %s", name, type, icon)
        
    return (name, icon, type, tiname, size, isprotected)
    
if __name__ == '__main__':
    deleteAll()


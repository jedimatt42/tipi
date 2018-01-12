# file_manager.py
#
# TIPI web administration
#
# Corey J. Anderson ElectricLab.com 2017
# et al.

from ti_files import ti_files
import os
import time
import errno
import logging

logger = logging.getLogger(__name__)

tipi_disk_base = '/home/tipi/tipi_disk' 

def newDir(path,dir):
    logger.debug("creating directory %s/%s", path, dir)
    if dir.contains("."):
        raise
    try:
        os.makedirs(tipi_disk_base + filePath + '/' + newDir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

def download(path):
    logger.debug("download request for %s", path)

    file_path = tipi_disk_base + '/' + path
    return { directory: os.path.dirname(file_path), 
             filename: os.path.basename(file_path) }


def catalog(path):
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
            dl_link = '<a href="/files/' + path + '/' + item + '?action=download">Download</a>'
            
            if ti_files.isTiFile(item_path):
                icon = '<img src="/images/ti_logo_icon.jpg" width=22>'
                type = 'TI'
                if ti_files.isTIBasicPrg(item_path):
                    icon = '<img src="/images/BASIC.png" width=36>'
                    edit_link = '<a href="/edit_basic_file?file_name=' + path + '/' + item + '&rp=/files/' + path + '">Edit</a>'
                
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

    return { 'tipi_dir_listing': tipi_dir_listing, 
             'total_files': len(tipi_files), 
             'display_path': '/' + path, 
             'rp': '/files/' + path, 
             'path': path }



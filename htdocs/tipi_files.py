# TIPI web administration
#
# Corey J. Anderson ElectricLab.com 2017
# et al.

from ti_files import ti_files
import os
import time
import errno
import logging
import tipi_cache

logger = logging.getLogger(__name__)

tipi_disk_base = '/home/tipi/tipi_disk' 

icons = { 'basic': '<img src="/images/basic_icon.png" width=22 title="BASIC PROGRAM">',
          'tifile': '<img src="/images/ti_logo_icon.jpg" width=22 title="TIFILES">',
          'native': '<img src="/images/native_icon.png" width=22 title="OS Native File">'
}

download_template = '<a href="%s"><img src="/images/download_icon.png" width=32 title="Download File"/></a>'

editlink_template = '<a href="/edit_basic_file?file_name=%s/%s&path=%s"><img src="/images/edit_icon.png" width=22 title="Edit File"/></a>'

# this should be a form.
convlink_template = '<img src="/images/convert_icon.png" width=32 title="Convert to TIFILES"/>'

def newdir(path,newdir):
    logger.debug("creating directory %s/%s", path, newdir)
    if '.' in newdir:
        raise
    try:
        os.makedirs(tipi_disk_base + path + '/' + newdir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

def download(path):
    logger.debug("download request for %s", path)

    file_path = tipi_disk_base + '/' + path
    return { 'directory': os.path.dirname(file_path), 
             'filename': os.path.basename(file_path) }


def catalog(path):
    logger.debug("generating catalog for: %s", path)
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
                               'name' : '&lt;parent&gt;',
                               'longname' : None,
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
        
            tipi_subdirs.append( { 'name': item_display_path,
                                   'type': 'DIR',
                                   'icon': '<a href="/files%s"><img src="/images/folder_icon.png" width=22 border=0></a>' %item,
                                   'longname': None,
                                 }
                               )

        else:
            # Determine file type:
            #
            fileInfo = tipi_cache.lookupFileInfo(item_path)
            icon = icons[fileInfo['icon']]
            type = fileInfo['type']
            tiname = fileInfo['tiname']
            size = fileInfo['size']
            edit_link = ''
            conv_link = ''
            date = time.strftime("%b %d %Y %H:%M:%S", time.gmtime(os.path.getmtime(item_path)))

            dlpath = item_path.replace(tipi_disk_base,'')
            dl_link = download_template % (dlpath)
            if fileInfo['icon'] == 'basic':
                edit_link = editlink_template % (path, item, path)

            if fileInfo['icon'] == 'native':
                conv_link = convlink_template 
                # % (path, item)
          

            if tiname != item:
                longname = item
            else:
                longname = None
        
            tipi_files.append( { 'icon'      : icon,
                                 'name'      : tiname,
                                 'size'      : size,
                                 'date'      : date,
                                 'edit_link' : edit_link,
                                 'dl_link'   : dl_link,
                                 'conv_link' : conv_link,
                                 'type'      : type,
                                 'longname'  : longname,
                               } )

    tipi_dir_listing = tipi_subdirs
    tipi_dir_listing.extend(tipi_files)

    return { 'tipi_dir_listing': tipi_dir_listing, 
             'total_files': len(tipi_files), 
             'display_path': '/' + path, 
             'rp': '/files/' + path, 
             'path': path }



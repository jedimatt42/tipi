# tipi_uploads
#
# TIPI web administration
#
# Corey J. Anderson ElectricLab.com 2017
# et al.

import os
import logging
from ti_files import ti_files

logger = logging.getLogger(__name__)

tipi_disk_base = '/home/tipi/tipi_disk' 

def save(path, filedata):
    localfilename = os.path.join(tipi_disk_base + path, filedata.filename)
    logger.debug("saving upload to: %s", localfilename)
    filedata.save(localfilename)
    


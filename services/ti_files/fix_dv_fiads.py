import logging
from ConfigLogging import configure_logging
from . import ti_files
from pathlib import Path

"""
Scan the TIPI filesystem for FIADs that have an incorrect EOF_OFFSET header
and repair them.
"""


configure_logging()

logger = logging.getLogger(__name__)

def is_broken(data):
    eof_offset = ti_files.eofOffset(data)
    try:
        if eof_offset:
            ridx = ((ti_files.getSectors(data) - 1) * 256) + 128 + eof_offset
            return data[ridx-1] == 0xff and data[ridx] == 0x00
    except:
        # if files are empty the calculated eof index will be out of range
        pass
    return False

def fix_eof(file_path, data):
    eof_offset = ti_files.eofOffset(data)
    ti_files.setEofOffset(data, eof_offset - 1)
    with open(file_path, 'wb') as f:
        f.write(data)


if __name__ == "__main__":
    for path in Path('/home/tipi/tipi_disk').rglob('*'):
        if path.is_file():
            posix_path = path.as_posix()

            with open(posix_path, 'rb') as f:
                data = bytearray(f.read())

            if len(data) > 128 and ti_files.isValid(data) and ti_files.isVariable(data):
                if is_broken(data):
                    logger.info(f'file: {posix_path}')
                    fix_eof(posix_path, data)


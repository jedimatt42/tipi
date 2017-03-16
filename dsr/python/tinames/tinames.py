import sys

# Transform a name supplied by the 4A into our storage path
def devnameToLocal(devname):
    parts = devname.split('.')
    path = ""
    if parts[0] == "TIPI":
        path = "/tipi_disk"
    elif parts[0] == "DSK1":
        path = "/tipi_disk/DSK1"
    elif parts[0] == "DSK":
        path = "/tipi_disk"

    for part in parts[1:]:
        if part != "":
            path += "/" + findpath(path, part)

    return path

# Use the context of actual files to transform TI file names to possibly long TI names
def findpath(path, part):
    # TBD
    return part


# print devnameToLocal(sys.argv[1])


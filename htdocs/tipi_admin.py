# TIPI web administration
#
# Corey J. Anderson ElectricLab.com 2017
# et al.

def version():
    version = { }
    with open("/home/tipi/tipi/version.txt") as vt:
        for line in vt.readlines():
            parts = line.split('=')
            version[str(parts[0].strip().lower())] = str(parts[1].strip())
    return version

def logdata():
    with open('/var/log/tipi/tipi.log', 'r') as f:
        return { 'logdata': f.read() }

def reboot():
    with open("/tmp/tipireboot", 'w') as trigger:
        trigger.write("tipi")

def shutdown():
    with open("/tmp/tipihalt", 'w') as trigger:
        trigger.write("tipi")

def upgrade():
    with open("/tmp/tipiupgrade", 'w') as trigger:
        trigger.write("tipi")


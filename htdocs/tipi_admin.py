# route.py
#
# TIPI web administration
#
# Corey J. Anderson ElectricLab.com 2017
# et al.


def reboot():
    with open("/tmp/tipireboot", 'w') as trigger:
        trigger.write("tipi")

def shutdown():
    with open("/tmp/tipihalt", 'w') as trigger:
        trigger.write("tipi")

def upgrade():
    with open("/tmp/tipiupgrade", 'w') as trigger:
        trigger.write("tipi")


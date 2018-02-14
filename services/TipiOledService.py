#!/usr/bin/env python2

import os
import sys
import errno
import time
import Adafruit_SSD1306
import re
import logging
import ConfigLogging

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from pygtail import Pygtail

ConfigLogging.configure_logging()
logger = logging.getLogger(__name__)

pat = re.compile(r"^.*oled.*: INFO     (.*)$")

fontpath = "/home/tipi/tipi/services/TI99Basic.ttf"

oled = None

try:
    # 128x32 oledlay with hardware I2C:
    oled = Adafruit_SSD1306.SSD1306_128_32(rst=None)

    # Initialize library.
    oled.begin()
    logger.info("TIPI Attached to I2C Oled Display")
except Exception as e:
    logger.exception("No I2C Oled Display attached")
    sys.exit(1)

# Clear oledlay.
oled.clear()
oled.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = oled.width
height = oled.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Load TI Basic short caps font.
font = ImageFont.truetype(fontpath, 32)
fontsmall = ImageFont.truetype(fontpath, 24)


def displayLine(line):
    lineparts = line.split('/')
    line1 = lineparts[0]
    if len(lineparts) == 2:
        line2 = lineparts[1]
    else:
        line2 = line[min(len(line),10):]

    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    draw.text((0, 0), line1, font=font, fill=255)
    draw.text((0, 16), line2, font=fontsmall, fill=255)

    # Display image.
    oled.image(image)
    oled.display()


displayLine("   TIPI   Waiting...")

logpath = "/home/tipi/log"
try:
    os.makedirs(logpath)
except OSError as exc:
    if exc.errno == errno.EEXIST and os.path.isdir(logpath):
        pass
    else:
        raise

logfile = "{}/tipi.log".format(logpath)
with open(logfile, 'a'):
    os.utime(logfile, None)

pygtail = Pygtail(logfile)
oldlines = filter(lambda x: "oled" in x, pygtail.readlines())

if len(oldlines) > 0:
    line = oldlines[len(oldlines) - 1]
else:
    line = ""


idleCounter = 0
while True:
    for line in pygtail:
        if "oled" in line:
            m = pat.match(line)
            msg = m.group(1)
            displayLine(msg)
    time.sleep(0.100)
    idleCounter += 1
    if idleCounter > 200:
        displayLine("TIPI IP:/192.168.1.48")
        idleConter = 0

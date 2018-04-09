import os
import sys
import errno
import time
import Adafruit_SSD1306
import logging

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from TipiConfig import TipiConfig

logger = logging.getLogger(__name__)

tipi_config = TipiConfig.instance()

fontpath = "/home/tipi/tipi/services/TI99Basic.ttf"

class Oled(object):

    def __init__(self):
        self.device = None
        try:
            # 128x32 devicelay with hardware I2C:
            self.device = Adafruit_SSD1306.SSD1306_128_32(rst=None)

            # Initialize library.
            self.device.begin()
            print "TIPI Attached to I2C Oled Display"

            # Clear display.
            self.device.clear()
            self.device.display()

            # Create blank image for drawing.
            # Make sure to create image with mode '1' for 1-bit color.
            self.width = self.device.width
            self.height = self.device.height
            self.image = Image.new('1', (self.width, self.height))

            # Get drawing object to draw on image.
            self.draw = ImageDraw.Draw(self.image)

            # Load TI Basic short caps font.
            self.font = ImageFont.truetype(fontpath, 32)
            self.fontsmall = ImageFont.truetype(fontpath, 24)

            self.rotate = int(tipi_config.get("OLED_ROTATE", "0"))

        except Exception as e:
            self.device = None
            print "No I2C Oled Display attached"

    def displayLine(self, line):
        lineparts = line.split('/')
        line1 = lineparts[0]
        if len(lineparts) == 2:
            line2 = lineparts[1]
        else:
            line2 = line[min(len(line),10):]

        # Draw a black filled box to clear the image.
        self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)

        self.draw.text((0, 0), line1, font=self.font, fill=255)
        self.draw.text((1, 16), line2, font=self.fontsmall, fill=255)

        # Display image.
        self.device.image(self.image.rotate(self.rotate))
        self.device.display()

    def info(self, format, *args):
        if not self.device is None:
            self.displayLine(format % args)

oled = Oled()

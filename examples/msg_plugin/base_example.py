import logging

logger = logging.getLogger(__name__)



# When installed in /home/tipi/tipi_disk/PLUGINS as '60.py', this plugin will respond to 
# TIPI message requests for message type 0x60. 

class ExamplePlugin(object):
    """ The class name doesn't matter. It doesn't even have to be unique. """

    def __init__(self):
        logger.info('created plugin instance')

    def handle(self, bytes):
    """
    'bytes' will be a byte array of the message sent to the plugin
    'bytes' includes the message type byte at index 0. 
    """
        # process the message and send a message back
        # processing should catch any exceptions and return an error code or empty message back to the 4A

        try:
            logger.info('handled plugin message')

            # return a message containing the letter 'A'
            return [0x41]
        except:
            logger.error('something went wrong')

            # Always return something, even 0 length array of bytes, or the 4A/client side will hang
            return []


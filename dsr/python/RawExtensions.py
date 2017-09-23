from Mouse import Mouse


class RawExtensions(object):

    def __init__(self, tipi_io):
        # Extend this list to register new special request handlers
        self.__reg = {0x20: Mouse(tipi_io)}

    def handle(self, bytes):
        if not bytes[0] in self.__reg:
            return False
        handler = self.__reg[bytes[0]]
        return handler.handle(bytes)

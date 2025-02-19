import os
import importlib.util

PLUGIN_DIR = "/home/tipi/plugins"

class CustomExtensions(object):
    def __init__(self, tipi_io):
        # Extend this list to register new special request handlers
        #
        self.__reg = self.load_plugins(tipi_io)

    def handle(self, bytes):
        if not bytes[0] in self.__reg:
            return False
        handler = self.__reg[bytes[0]]

        return handler.handle(bytes)

    def load_plugins(self, tipi_io):
        plugins = {}

        for filename in os.listdir(PLUGIN_DIR):
            if filename.endswith(".py") and len(filename) == 5:  # "XX.py" (2 hex + ".py")
                hex_part = filename[:2]

                try:
                    key = int(hex_part, 16)  # Convert hex part to integer
                except ValueError:
                    continue  # Skip non-hex named files

                if key < 0x60:
                    continue  # Skip message named less than 0x60, reserved for built in handlers
            
                module_path = os.path.join(PLUGIN_DIR, filename)
                module_name = f"plugin_{hex_part}"  # Unique module name
            
                spec = importlib.util.spec_from_file_location(module_name, module_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                # Find the first class defined in the module
                plugin_class = None
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if isinstance(attr, type) and attr.__module__ == module.__name__:
                        plugin_class = attr
                        break

                if plugin_class:
                    plugins[key] = plugin_class(tipi_io)

        return plugins


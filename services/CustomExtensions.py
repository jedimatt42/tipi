import os
import importlib.util
import logging
import time

PLUGIN_DIR = "/home/tipi/TIPI_DISK/PLUGINS"

plugins = {}  # Stores active plugin instances
logger = logging.getLogger(__name__)
last_load_time = 0  # Stores the last load time

class CustomExtensions(object):
    def __init__(self, tipi_io):
        # Extend this list to register new special request handlers
        #
        self.tipi_io = tipi_io

    def handle(self, bytes):
        reload_plugins()  # Reload plugins if modified
        if not bytes[0] in plugins:
            return False
        self.tipi_io.send(self.processRequest(bytes))
        return True

    def processRequest(self, bytes):
        try:
            plugin = plugins[bytes[0]]
            return plugin.handle(bytes)
        except KeyError as k:
            return [0xFF]


# -- load and monitor plugins for change

def load_plugin(filename):
    """Loads or reloads a single plugin from a file."""
    hex_part = filename[:2]

    try:
        key = int(hex_part, 16)  # Convert hex part to integer
    except ValueError:
        logger.warning(f"Skipping invalid hex filename: {filename}")
        return

    module_path = os.path.join(PLUGIN_DIR, filename)
    module_name = f"plugin_{hex_part}"  # Unique module name

    try:
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    except Exception as e:
        logger.error(f"Failed to load plugin {filename}: {e}")
        return

    # Find the first class defined in the module
    plugin_class = None
    for attr_name in dir(module):
        attr = getattr(module, attr_name)
        if isinstance(attr, type) and attr.__module__ == module.__name__:
            plugin_class = attr
            break

    if plugin_class:
        plugins[key] = plugin_class()  # Instantiate without tipi_io
        logger.info(f"Loaded plugin {hex(key).upper()} from {filename}")

def load_plugins():
    """Scans the directory and loads all plugins initially."""
    global last_load_time
    os.makedirs(PLUGIN_DIR, exist_ok=True)
 
    for filename in os.listdir(PLUGIN_DIR):
        if filename.endswith(".py") and len(filename) == 5:  # Must be 'XX.py'
            load_plugin(filename)
    
    last_load_time = time.time()  # Set the last load time

def reload_plugins():
    """Reloads plugins that have been modified since the last load time."""
    global last_load_time
    current_time = time.time()
    
    for filename in os.listdir(PLUGIN_DIR):
        if filename.endswith(".py") and len(filename) == 5:  # Must be 'XX.py'
            file_path = os.path.join(PLUGIN_DIR, filename)
            if os.path.getmtime(file_path) > last_load_time:
                load_plugin(filename)
    
    last_load_time = current_time  # Update the last load time

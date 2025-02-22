import os
import importlib.util
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

PLUGIN_DIR = "/home/tipi/TIPI_DISK/PLUGINS"


plugins = {}  # Stores active plugin instances
logger = logging.getLogger(__name__)

class CustomExtensions(object):
    def __init__(self, tipi_io):
        # Extend this list to register new special request handlers
        #
        self.tipi_io = tipi_io

    def handle(self, bytes):
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
    os.makedirs(PLUGIN_DIR, exist_ok=True)
 
    for filename in os.listdir(PLUGIN_DIR):
        if filename.endswith(".py") and len(filename) == 5:  # Must be 'XX.py'
            load_plugin(filename)

class PluginWatcher(FileSystemEventHandler):
    """Watches the plugin directory for changes and reloads plugins."""

    def on_modified(self, event):
        """Handles file modifications (reload plugin)."""
        if event.is_directory or not event.src_path.endswith(".py"):
            return

        filename = os.path.basename(event.src_path)
        logger.info(f"Detected change in {filename}, reloading...")
        load_plugin(filename)

    def on_created(self, event):
        """Handles new files (load new plugin)."""
        if event.is_directory or not event.src_path.endswith(".py"):
            return

        filename = os.path.basename(event.src_path)
        logger.info(f"New plugin detected: {filename}, loading...")
        load_plugin(filename)

    def on_deleted(self, event):
        """Handles plugin deletions (remove from dictionary)."""
        if event.is_directory or not event.src_path.endswith(".py"):
            return

        filename = os.path.basename(event.src_path)
        hex_part = filename[:2]

        try:
            key = int(hex_part, 16)
            if key in plugins:
                del plugins[key]
                logger.info(f"Plugin {hex(key).upper()} removed")
        except ValueError:
            pass  # Ignore invalid filenames

def start_watcher():
    """Starts the file watcher."""
    event_handler = PluginWatcher()
    observer = Observer()
    observer.schedule(event_handler, PLUGIN_DIR, recursive=False)
    observer.start()
    return observer




import logging
import evdev
import threading
import queue

logger = logging.getLogger(__name__)


class KeyboardPlugin(object):
    def __init__(self):
        logger.info('created plugin instance')
        self.device = None
        self.queue = queue.Queue()
        self.thread = None
        self.grabbed = False

    def grab_keyboard(self):
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
        for device in devices:
            logger.info(f'examining device: {device.name}')
            if 'keyboard' in device.name.lower():
                self.device = device
                self.device.grab()
                logger.info(f'grabbed keyboard: {device.name}')
                break

    def read_keyboard(self):
        for event in self.device.read_loop():
            if event.type == evdev.ecodes.EV_KEY and event.value == 1:  # Key press event
                self.queue.put(event.code)
                logger.info(f'key pressed: {evdev.ecodes.KEY[event.code]}')

    def handle(self, bytes):
        try:
            if not self.grabbed:
                self.grab_keyboard()
                self.thread = threading.Thread(target=self.read_keyboard, daemon=True)
                self.thread.start()
                self.grabbed = True

            if not self.queue.empty():
                key_code = self.queue.get()
                logger.info(f'handled plugin message, key code: {key_code}')
                return [key_code]
            else:
                return []

        except Exception as e:
            logger.error(f'something went wrong: {e}')
            return []


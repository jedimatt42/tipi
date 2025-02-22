import logging
import evdev
import threading
import queue

logger = logging.getLogger(__name__)

# Mapping of evdev keycodes to ASCII terminal VT100 type codes
KEYCODE_TO_ASCII = {
    evdev.ecodes.KEY_A: ord('a'),
    evdev.ecodes.KEY_B: ord('b'),
    evdev.ecodes.KEY_C: ord('c'),
    evdev.ecodes.KEY_D: ord('d'),
    evdev.ecodes.KEY_E: ord('e'),
    evdev.ecodes.KEY_F: ord('f'),
    evdev.ecodes.KEY_G: ord('g'),
    evdev.ecodes.KEY_H: ord('h'),
    evdev.ecodes.KEY_I: ord('i'),
    evdev.ecodes.KEY_J: ord('j'),
    evdev.ecodes.KEY_K: ord('k'),
    evdev.ecodes.KEY_L: ord('l'),
    evdev.ecodes.KEY_M: ord('m'),
    evdev.ecodes.KEY_N: ord('n'),
    evdev.ecodes.KEY_O: ord('o'),
    evdev.ecodes.KEY_P: ord('p'),
    evdev.ecodes.KEY_Q: ord('q'),
    evdev.ecodes.KEY_R: ord('r'),
    evdev.ecodes.KEY_S: ord('s'),
    evdev.ecodes.KEY_T: ord('t'),
    evdev.ecodes.KEY_U: ord('u'),
    evdev.ecodes.KEY_V: ord('v'),
    evdev.ecodes.KEY_W: ord('w'),
    evdev.ecodes.KEY_X: ord('x'),
    evdev.ecodes.KEY_Y: ord('y'),
    evdev.ecodes.KEY_Z: ord('z'),
    evdev.ecodes.KEY_1: ord('1'),
    evdev.ecodes.KEY_2: ord('2'),
    evdev.ecodes.KEY_3: ord('3'),
    evdev.ecodes.KEY_4: ord('4'),
    evdev.ecodes.KEY_5: ord('5'),
    evdev.ecodes.KEY_6: ord('6'),
    evdev.ecodes.KEY_7: ord('7'),
    evdev.ecodes.KEY_8: ord('8'),
    evdev.ecodes.KEY_9: ord('9'),
    evdev.ecodes.KEY_0: ord('0'),
    evdev.ecodes.KEY_ENTER: ord('\n'),
    evdev.ecodes.KEY_SPACE: ord(' '),
    evdev.ecodes.KEY_BACKSPACE: ord('\b'),
    evdev.ecodes.KEY_TAB: ord('\t'),
    evdev.ecodes.KEY_ESC: ord('\x1b'),
    evdev.ecodes.KEY_MINUS: ord('-'),
    evdev.ecodes.KEY_EQUAL: ord('='),
    evdev.ecodes.KEY_LEFTBRACE: ord('['),
    evdev.ecodes.KEY_RIGHTBRACE: ord(']'),
    evdev.ecodes.KEY_BACKSLASH: ord('\\'),
    evdev.ecodes.KEY_SEMICOLON: ord(';'),
    evdev.ecodes.KEY_APOSTROPHE: ord('\''),
    evdev.ecodes.KEY_GRAVE: ord('`'),
    evdev.ecodes.KEY_COMMA: ord(','),
    evdev.ecodes.KEY_DOT: ord('.'),
    evdev.ecodes.KEY_SLASH: ord('/'),
    # Add more mappings as needed
}

SHIFT_KEYCODES = {evdev.ecodes.KEY_LEFTSHIFT, evdev.ecodes.KEY_RIGHTSHIFT}
CONTROL_KEYCODES = {evdev.ecodes.KEY_LEFTCTRL, evdev.ecodes.KEY_RIGHTCTRL}
CAPSLOCK_KEYCODE = evdev.ecodes.KEY_CAPSLOCK

class KeyboardPlugin(object):
    def __init__(self):
        logger.info('created plugin instance')
        self.device = None
        self.queue = queue.Queue()
        self.thread = None
        self.grabbed = False
        self.shift_pressed = False
        self.control_pressed = False
        self.capslock_on = False

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
            if event.type == evdev.ecodes.EV_KEY:
                if event.code in SHIFT_KEYCODES:
                    self.shift_pressed = event.value != 0
                elif event.code in CONTROL_KEYCODES:
                    self.control_pressed = event.value != 0
                elif event.code == CAPSLOCK_KEYCODE and event.value == 1:
                    self.capslock_on = not self.capslock_on
                elif event.value == 1:  # Key press event
                    ascii_code = KEYCODE_TO_ASCII.get(event.code, None)
                    if ascii_code is not None:
                        if self.control_pressed:
                            ascii_code = ascii_code & 0x1F  # Control character
                        elif self.shift_pressed or self.capslock_on:
                            if ord('a') <= ascii_code <= ord('z'):
                                ascii_code = ascii_code - ord('a') + ord('A')
                            elif ascii_code in range(ord('1'), ord('9') + 1):
                                ascii_code = ord('!@#$%^&*()'[ascii_code - ord('1')])
                            elif ascii_code == ord('0'):
                                ascii_code = ord(')')
                            elif ascii_code == ord('-'):
                                ascii_code = ord('_')
                            elif ascii_code == ord('='):
                                ascii_code = ord('+')
                            elif ascii_code == ord('['):
                                ascii_code = ord('{')
                            elif ascii_code == ord(']'):
                                ascii_code = ord('}')
                            elif ascii_code == ord('\\'):
                                ascii_code = ord('|')
                            elif ascii_code == ord(';'):
                                ascii_code = ord(':')
                            elif ascii_code == ord('\''):
                                ascii_code = ord('"')
                            elif ascii_code == ord('`'):
                                ascii_code = ord('~')
                            elif ascii_code == ord(','):
                                ascii_code = ord('<')
                            elif ascii_code == ord('.'):
                                ascii_code = ord('>')
                            elif ascii_code == ord('/'):
                                ascii_code = ord('?')
                        self.queue.put(ascii_code)
                        logger.info(f'key pressed: {evdev.ecodes.KEY[event.code]}, ascii code: {ascii_code}')
                    else:
                        logger.warning(f'key code {event.code} not mapped to ASCII')

    def handle(self, bytes):
        try:
            if not self.grabbed:
                self.grab_keyboard()
                self.thread = threading.Thread(target=self.read_keyboard, daemon=True)
                self.thread.start()
                self.grabbed = True

            if not self.queue.empty():
                ascii_code = self.queue.get()
                logger.info(f'handled plugin message, ascii code: {ascii_code}')
                return [ascii_code]
            else:
                return []

        except Exception as e:
            logger.error(f'something went wrong: {e}')
            return []


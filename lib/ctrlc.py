import sys
import time
import signal

class CtrlC:
    pressed = False

    @classmethod
    def handle(cls, signal, frame):
        print('Ctrl-C pressed, will exit soon')
        if cls.pressed:
            print('Ctrl-C pressed twice. Committing violent suicide.')
            sys.exit(1)
        cls.pressed = True

signal.signal(signal.SIGINT, CtrlC.handle)

if __name__ == '__main__':
    time.sleep(2)
    if CtrlC.pressed:
        print('yay')
    time.sleep(2)

""" Configuration Module """

import sys
import shutil

COLUMNS = shutil.get_terminal_size().columns
ROWS = shutil.get_terminal_size().lines

MARGINX = 6
MARGINY = 3


class AlarmException(Exception):
    """ALarm Exception"""
    pass


def pos(x_coord, y_coord):
    """Returns coordinates in right format to use colorama"""
    return '\033[' + str(x_coord) + ';' + str(y_coord) + 'H'


def alarm_handler(signum, frame):
    """Alarm Handler"""
    if signum and frame:
        raise AlarmException


def get_input(timeout=1):
    """Gets input character by character"""
    import signal
    signal.signal(signal.SIGALRM, alarm_handler)
    signal.alarm(timeout)
    try:
        text = GETCH()
        signal.alarm(0)
        return text
    except AlarmException:
        pass
    signal.signal(signal.SIGALRM, signal.SIG_IGN)
    return ''


# Gets a single character from standard input.  Does not echo to the screen.
class _Getch: # pylint: disable=too-few-public-methods
    """Decides wether being run on windows or linux and takes input accordingly"""
    def __init__(self):
        try:
            import msvcrt
            self.impl = msvcrt.getch()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self):
        return self.impl()


class _GetchUnix:

    def __init__(self):
        pass

    def __call__(self):
        import tty
        import termios
        file_descriptor = sys.stdin.fileno()
        old_settings = termios.tcgetattr(file_descriptor)
        try:
            tty.setraw(sys.stdin.fileno())
            char = sys.stdin.read(1)
        finally:
            termios.tcsetattr(file_descriptor, termios.TCSADRAIN, old_settings)
        return char


GETCH = _Getch()

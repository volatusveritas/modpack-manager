from ctypes import c_void_p
from typing import Callable
import unicurses as curses


WIN_TITLE_COLOR = 1
SEC_TITLE_COLOR = 2
SPECIAL_COLOR = 3

stdscr: c_void_p


def _set_color_pairs() -> None:
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)


def _initialize() -> None:
    global stdscr

    stdscr = curses.initscr()
    curses.start_color()
    curses.noecho()
    curses.cbreak()
    curses.keypad(stdscr, True)
    curses.curs_set(False)
    _set_color_pairs()


def _finalize() -> None:
    curses.echo()
    curses.nocbreak()
    curses.keypad(stdscr, False)
    curses.curs_set(True)
    curses.endwin()


def wrap_execute(mainfunc: Callable[..., None]) -> None:
    try:
        _initialize()
        mainfunc()
        _finalize()
    except Exception as e:
        _finalize()
        raise e

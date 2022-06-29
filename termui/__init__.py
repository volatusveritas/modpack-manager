from ctypes import c_void_p
from typing import Callable
import unicurses as curses

import filehandling


WIN_TITLE_COLOR = 1
SEC_TITLE_COLOR = 2
SPECIAL_COLOR = 3
STANDOUT_COLOR = 4
STANDOUT2_COLOR = 5

stdscr: c_void_p


def _set_color_pairs() -> None:
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)


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
    finally:
        filehandling.clean_exiting()


def newline() -> None:
    curses.addch("\n")


def input(text: str = "") -> str:
    curses.echo()
    curses.nocbreak()
    curses.curs_set(True)

    curses.addstr(text)
    input: str = curses.getstr()

    curses.noecho()
    curses.cbreak()
    curses.curs_set(False)

    return input

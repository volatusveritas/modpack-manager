from __future__ import annotations
from dataclasses import dataclass
import unicurses as curses
from typing import Any, Callable

import termui
from termui import constants


@dataclass
class Hop:
    description: str
    target: Menu


@dataclass
class Option:
    description: str
    target: Callable


class MenuManager:
    def __init__(self) -> None:
        self.next: Menu | None = None

    def start(self, starting_menu: Menu) -> None:
        starting_menu.display()

        while self.next:
            next = self.next
            self.next = None
            next.display()

    def queue_menu(self, menu: Menu) -> None:
        self.next = menu


class Menu:
    def __init__(self, manager: MenuManager, title: str) -> None:
        self.manager: MenuManager = manager
        self.title: str = title.upper()
        self.hops: dict[str, Hop] = {}

    def add_hop(self, key: str, description: str, target: Menu) -> Menu:
        if key == constants.QUIT_KEY:
            raise ValueError(
                f"Can not assign a hop to the quit key ({constants.QUIT_KEY})"
            )

        self.hops[key] = Hop(description, target)

        return self

    def remove_hop(self, key) -> Menu:
        del self.hops[key]

        return self

    def _render_title(self) -> None:
        curses.addstr(self.title, curses.color_pair(termui.WIN_TITLE_COLOR))
        termui.newline()

    def _render_content(self) -> None: ...

    def _render_hops(self) -> None:
        if not self.hops:
            return

        curses.addstr(constants.CONTENT_PADDING*" ")
        curses.addstr("Hops\n", curses.color_pair(termui.SEC_TITLE_COLOR))
        for hop in self.hops:
            curses.addstr(constants.CONTENT_PADDING*2*" " + "[")
            curses.addstr(hop, curses.color_pair(termui.SPECIAL_COLOR))
            curses.addstr("] " + self.hops[hop].description)
            termui.newline()

    def _cleanup(self) -> None: ...

    def _extra_input(self, key: str) -> bool: return True

    def _handle_input(self) -> None:
        while True:
            key = curses.getkey().decode("utf8")

            if key == constants.QUIT_KEY:
                break
            elif key in self.hops:
                self._cleanup()
                self.manager.queue_menu(self.hops[key].target)
                break
            else:
                if not self._extra_input(key):
                    break

    def display(self) -> None:
        curses.clear()

        self._render_title()
        termui.newline()
        self._render_content()
        self._render_hops()
        termui.newline()
        curses.addstr(
            f"{constants.CONTENT_PADDING*' '}"
            f"Press [{constants.QUIT_KEY}] to quit"
        )

        self._handle_input()


class PlainTextMenu(Menu):
    def __init__(
        self, manager: MenuManager, title: str, text: str = ""
    ) -> None:
        super().__init__(manager, title)
        self.text: str = text

    def _render_content(self) -> None:
        curses.addstr(constants.CONTENT_PADDING*" " + self.text + "\n")
        termui.newline()


class ScrollingTextMenu(Menu):
    def __init__(
        self, manager: MenuManager, title: str, lines: list[str] = []
    ) -> None:
        super().__init__(manager, title)
        self.lines: list[str] = lines
        self.offset: int = 0
        self.base_line: int = -1

    def render_lines(self) -> None:
        curses.move(self.base_line, 0)
        for line in self.lines[
            self.offset : self.offset + constants.SCROLLING_TEXT_SIZE
        ]:
            curses.addstr(constants.CONTENT_PADDING*" " + line)
            termui.newline()
        for _ in range(constants.SCROLLING_TEXT_SIZE - len(self.lines)):
            termui.newline()
        curses.refresh()

    def scroll_up(self, by: int = 1) -> None:
        self.offset = max(0, self.offset - by)
        self.render_lines()

    def scroll_down(self, by: int = 1) -> None:
        self.offset = min(
            max(constants.SCROLLING_TEXT_SIZE, len(self.lines))
            - constants.SCROLLING_TEXT_SIZE,
            self.offset + by
        )
        self.render_lines()

    def _extra_input(self, key: str) -> bool:
        if key == constants.SCROLL_UP_KEY:
            self.scroll_up()
        elif key == constants.SCROLL_DOWN_KEY:
            self.scroll_down()

        return True

    def _render_content(self) -> None:
        self.base_line = curses.getyx(termui.stdscr)[0]
        self.render_lines()
        termui.newline()
        curses.addstr(
            f"{constants.CONTENT_PADDING*' '}"
            f"Press [{constants.SCROLL_DOWN_KEY}] "
            f"or [{constants.SCROLL_UP_KEY}] to go up or down, respectively\n"
        )
        termui.newline()


class OptionsMenu(Menu):
    def __init__(
        self, manager: MenuManager, title: str, options: dict = {}
    ) -> None:
        super().__init__(manager, title)
        self.options: dict[str, Option] = options

    def add_option(
        self, key: str, description: str, target: Callable
    ) -> OptionsMenu:
        self.options[key] = Option(description, target)

        return self

    def remove_option(self, key: str) -> None:
        del self.options[key]

    def _render_content(self) -> None:
        for option in self.options:
            curses.addstr(f"{constants.CONTENT_PADDING*' '}")
            curses.addch("[")
            curses.addstr(option, curses.color_pair(termui.SPECIAL_COLOR))
            curses.addch("]")
            curses.addstr(f" {self.options[option].description}\n")

        termui.newline()

    def _extra_input(self, key: str) -> bool:
        if key in self.options:
            self.options[key].target()

        return True


class InputsMenu(Menu):
    def __init__(
        self, manager: MenuManager, title: str,
        do_when_filled: Callable[[list[str]], Any],
        input_queries: list[str] = []
    ) -> None:
        super().__init__(manager, title)
        self.do_when_filled = do_when_filled
        self.input_queries: list[str] = input_queries
        self.input_positions: list[tuple[int, int]] = []
        self.next_input: int = 0
        self.answers: list[str] = []

    def _render_content(self) -> None:
        for idx, input in list(enumerate(self.input_queries)):
            curses.addstr(
                f"{constants.CONTENT_PADDING*' '}"
                f"{input} "
            )
            curses.addch(
                constants.PROMPT_DIVISOR,
                curses.color_pair(termui.STANDOUT_COLOR)
            )
            curses.addch(" ")
            self.input_positions.append(curses.getyx(termui.stdscr))
            curses.addstr(
                constants.UNPROMPTED_INDICATOR,
                curses.color_pair(
                    termui.STANDOUT2_COLOR if idx == self.next_input
                    else termui.STANDOUT_COLOR
                )
            )
            termui.newline()

        termui.newline()
        curses.addstr(
            f"{constants.CONTENT_PADDING*' '}"
            f"Press [{constants.NEXT_INPUT_KEY}] to fill the next input\n"
        )
        termui.newline()

    def _cleanup(self) -> None:
        self.next_input = 0
        self.answers = []

    def _extra_input(self, key: str) -> bool:
        if self.next_input == len(self.input_queries):
            return True

        if key == constants.NEXT_INPUT_KEY:
            curses.move(*self.input_positions[self.next_input])
            curses.addstr(len(constants.UNPROMPTED_INDICATOR)*" ")
            curses.move(*self.input_positions[self.next_input])
            self.answers.append(termui.input())
            self.next_input += 1

            if self.next_input == len(self.input_queries):
                self.do_when_filled(self.answers)
                return False
            else:
                curses.move(*self.input_positions[self.next_input])
                curses.addstr(
                    constants.UNPROMPTED_INDICATOR,
                    curses.color_pair(termui.STANDOUT2_COLOR)
                )

        return True

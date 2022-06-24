from __future__ import annotations
import unicurses as curses

import termui
from termui import constants


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
        self.manager = manager
        self.title = title.upper()
        self.hops = {}

    def add_hop(self, key: str, description: str, target: Menu) -> Menu:
        if key == constants.QUIT_KEY:
            raise ValueError(
                f"Can not assign a hop to the quit key ({constants.QUIT_KEY})"
            )

        self.hops[key] = {
            "description": description,
            "target": target
        }

        return self

    def remove_hop(self, key) -> Menu:
        del self.hops[key]

        return self

    def render_title(self) -> None:
        curses.addstr(self.title, curses.color_pair(termui.WIN_TITLE_COLOR))
        curses.addch("\n")

    def render_content(self) -> None: ...

    def render_hops(self) -> None:
        if not self.hops:
            return

        curses.addstr("Hops\n", curses.color_pair(termui.SEC_TITLE_COLOR))
        for hop in self.hops:
            curses.addstr(constants.SUB_PADDING*" " + "[")
            curses.addstr(hop, curses.color_pair(termui.SPECIAL_COLOR))
            curses.addstr("] " + self.hops[hop]["description"])
            curses.addch("\n")

    def extra_input(self, key: str) -> bool: return True

    def handle_input(self) -> None:
        while True:
            key = curses.getkey().decode("utf8")

            if key == constants.QUIT_KEY:
                break
            elif key in self.hops:
                self.manager.queue_menu(self.hops[key]["target"])
                break
            else:
                if not self.extra_input(key):
                    break

    def display(self) -> None:
        curses.clear()

        curses.addch("\n")
        self.render_title()
        curses.addch("\n")
        self.render_content()
        self.render_hops()
        curses.addch("\n")
        curses.addstr(f"Press [{constants.QUIT_KEY}] to quit")
        curses.addch("\n")

        self.handle_input()


class PlainTextMenu(Menu):
    def __init__(self, manager: MenuManager, title: str, text: str) -> None:
        super().__init__(manager, title)
        self.text = text

    def render_content(self) -> None:
        curses.addstr(constants.CONTENT_PADDING*" " + self.text + "\n")
        curses.addch("\n")


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
            curses.addch("\n")
        curses.refresh()

    def scroll_up(self, by: int = 1) -> None:
        self.offset = max(0, self.offset - by)
        self.render_lines()

    def scroll_down(self, by: int = 1) -> None:
        self.offset = min(
            len(self.lines) - constants.SCROLLING_TEXT_SIZE, self.offset + by
        )
        self.render_lines()

    def extra_input(self, key: str) -> bool:
        if key == constants.SCROLL_UP_KEY:
            self.scroll_up()
        elif key == constants.SCROLL_DOWN_KEY:
            self.scroll_down()

        return True

    def render_content(self) -> None:
        self.base_line = curses.getyx(termui.stdscr)[0]
        self.render_lines()
        curses.addch("\n")
        curses.addstr(
            f"Press [{constants.SCROLL_DOWN_KEY}] "
            f"or [{constants.SCROLL_UP_KEY}] to go up or down, respectively\n"
        )
        curses.addch("\n")

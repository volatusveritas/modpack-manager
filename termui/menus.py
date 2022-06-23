from __future__ import annotations
import unicurses as curses

import termui


class Menu:
    def __init__(self, manager: MenuManager, title: str) -> None:
        self.manager = manager
        self.title = title.upper()
        self.hops = {}

    def add_hop(self, key: str, description: str, target: Menu) -> Menu:
        if key == "q":
            raise ValueError("Can not assign a hop to the quit key (q)")

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
            curses.addstr(4*" " + "[")
            curses.addstr(hop, curses.color_pair(termui.SPECIAL_COLOR))
            curses.addstr("] " + self.hops[hop]["description"])
            curses.addch("\n")

    def handle_input(self) -> None:
        while True:
            key = curses.getkey().decode("utf8")

            if key == "q":
                break
            elif key in self.hops:
                self.manager.queue_menu(self.hops[key]["target"])
                break

    def display(self) -> None:
        curses.clear()

        curses.addch("\n")
        self.render_title()
        curses.addch("\n")
        self.render_content()
        self.render_hops()
        curses.addch("\n")
        curses.addstr("Press [q] to quit")
        curses.addch("\n")

        self.handle_input()


class PlainTextMenu(Menu):
    def __init__(self, manager: MenuManager, title: str, text: str) -> None:
        super().__init__(manager, title)
        self.text = text

    def render_content(self) -> None:
        curses.addstr(2*" " + self.text + "\n")
        curses.addch("\n")


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

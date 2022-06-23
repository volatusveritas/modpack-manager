from __future__ import annotations

import os
import time
from typing import Callable

from modpackmanager import constants


class MenuManager:
    def __init__(self) -> None:
        self.next: OptionsMenu | None = None

    def start(self, menu: OptionsMenu) -> None:
        self.next = menu
        menu.query()

        while self.next:
            self.next.query()

    def stage_next(self, menu: OptionsMenu) -> None:
        self.next = menu


class OptionsMenu:
    def __init__(self, manager: MenuManager) -> None:
        self.manager: MenuManager = manager
        self.options: dict = {}
        self.hops: dict = {}

    def add_option(
        self, name: str, target: Callable[[], None],
        display_name: str, description: str
    ) -> OptionsMenu:
        self.options[name] = {
            "target": target,
            "display_name": display_name,
            "description": description
        }

        return self

    def remove_option(self, name: str) -> OptionsMenu:
        del self.options[name]

        return self

    def add_hop(
        self, name: str, target: OptionsMenu,
        display_name: str, description: str
    ) -> OptionsMenu:
        self.hops[name] = {
            "target": target,
            "display_name": display_name,
            "description": description
        }

        return self

    def remove_hop(self, name: str) -> OptionsMenu:
        del self.hops[name]

        return self

    def query(self) -> OptionsMenu:
        clear_screen()

        if self.options:
            print("Opções:")
            print()
            for option in self.options:
                print(
                    f"[{option}] {self.options[option]['display_name']}:"
                    + f" {self.options[option]['description']}"
                )
            print()
        if self.hops:
            print("Pulos:")
            print()
            for hop in self.hops:
                print(
                    f"[{hop}] {self.hops[hop]['display_name']}:"
                    + f" {self.hops[hop]['description']}"
                )
            print()
        choice: str = input("> ")
        if choice in self.options:
            print()
            self.options[choice]["target"]()
            time.sleep(constants.QUERY_SLEEP_TIME)
        elif choice in self.hops:
            self.manager.stage_next(self.hops[choice]["target"])
        else:
            print()
            print("Opção não encontrada")
            time.sleep(constants.QUERY_SLEEP_TIME)

        return self


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")

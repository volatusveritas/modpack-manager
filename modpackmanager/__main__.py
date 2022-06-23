import unicurses as curses
import time

import termui
from termui import menus


def window_error_test() -> None:
    manager = menus.MenuManager()
    main_menu = menus.PlainTextMenu(manager,
        "main menu",
        "From the main menu you may hop to other screens"
    )
    new_menu = menus.PlainTextMenu(manager,
        "new modpack",
        "Create a new modpack"
    )
    edit_menu = menus.PlainTextMenu(manager,
        "edit modpack",
        "Edit an existing modpack"
    )
    del_menu = menus.PlainTextMenu(manager,
        "delete modpack",
        "Delete an existing modpack"
    )

    (main_menu
        .add_hop("n", "new modpack", new_menu)
        .add_hop("e", "edit modpack", edit_menu)
        .add_hop("d", "delete modpack", del_menu)
    )

    for menu in [new_menu, edit_menu, del_menu]:
        menu.add_hop("b", "back to main menu", main_menu)

    manager.start(main_menu)


termui.wrap_execute(window_error_test)

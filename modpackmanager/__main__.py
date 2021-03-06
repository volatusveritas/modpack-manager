import termui
from termui import menus

import filehandling


def mainfunc() -> None:
    manager = menus.MenuManager()
    main_menu = menus.PlainTextMenu(
        manager, "main menu",
        "From the main menu you may hop to other menus"
    )
    new_menu = menus.PlainTextMenu(
        manager, "new modpack",
        "Create a new modpack"
    )
    edit_menu = menus.PlainTextMenu(
        manager, "edit modpack",
        "Edit an existing modpack"
    )
    view_menu = menus.PlainTextMenu(
        manager, "view modpack",
        "View the contents of an existing modpack"
    )
    del_menu = menus.PlainTextMenu(
        manager, "delete modpack",
        "Delete an existing modpack"
    )

    input_queries = [
        "Amount of mastery points you have on Gwen",
        "Amount of potatoes at the barn",
        "Size of apples in the farm's sacks",
    ]
    inputs_menu = menus.InputsMenu(
        manager, "inputs menu", lambda x: print(x), input_queries
    )

    (main_menu
        .add_hop("n", "new modpack", new_menu)
        .add_hop("e", "edit modpack", edit_menu)
        .add_hop("v", "view modpack", view_menu)
        .add_hop("d", "delete modpack", del_menu)
        .add_hop("i", "inputs menu", inputs_menu)
    )

    for menu in [new_menu, edit_menu, view_menu, del_menu, inputs_menu]:
        menu.add_hop("b", "back to main menu", main_menu)

    manager.start(main_menu)


try:
    termui.wrap_execute(mainfunc)
finally:
    filehandling.clean_exiting()

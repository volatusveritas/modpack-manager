from modpackmanager import tui


main_mng = tui.MenuManager()

main_menu = tui.OptionsMenu(main_mng)
new_modpack_menu = tui.OptionsMenu(main_mng)
view_modpack_menu = tui.OptionsMenu(main_mng)
edit_modpack_menu = tui.OptionsMenu(main_mng)
del_modpack_menu = tui.OptionsMenu(main_mng)

main_menu\
.add_hop(
    "new", new_modpack_menu, "New modpack", "create a new modpack"
).add_hop(
    "view", view_modpack_menu, "View modpack", "explore an existing modpack"
).add_hop(
    "edit", edit_modpack_menu, "Edit modpack", "edit an existing modpack"
).add_hop(
    "del", del_modpack_menu, "Delete modpack", "delete an existing modpack"
)

new_modpack_menu.add_hop(
    "back", main_menu, "Menu", "return to the main menu"
)

view_modpack_menu.add_hop(
    "back", main_menu, "Menu", "return to the main menu"
)

edit_modpack_menu.add_hop(
    "back", main_menu, "Menu", "return to the main menu"
)

del_modpack_menu.add_hop(
    "back", main_menu, "Menu", "return to the main menu"
)

main_mng.start(main_menu)

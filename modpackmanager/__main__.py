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
    lyrics_menu = menus.ScrollingTextMenu(manager,
        "lyrics",
        [
            "Eu vou rimando e você tem que responder",
            "eu vou chupar a sua pica mano, e cê nem vai vê",
            "mano aqui é só improviso o que que você vai fazer",
            "vou fazer uma live, no câmera privê",
            "agora, legal, eu gostei da sua levada",
            "eu vou te dar uma mamada",
            "só me responde uma coisa, isso é rima decorada?",
            "meu cú é o Batman, seu pau é o Charada",
            "Dahora, eu gostei, deu pra ver que é improviso",
            "meu pau no seu ouvido",
            "mas você não ganha de mim, então já te dou um aviso",
            "EU VOU RIMANDO E VOCÊ TEM QUE RESPONDER",
            "EU VOU CHUPAR A SUA PICA MANO, E CÊ NEM VAI VÊ",
            "MANO AQUI É SÓ IMPROVISO O QUE QUE VOCÊ VAI FAZER",
            "VOU FAZER UMA LIVE, NO CÂMERA PRIVÊ",
            "AGORA, LEGAL, EU GOSTEI DA SUA LEVADA",
            "EU VOU TE DAR UMA MAMADA",
            "SÓ ME RESPONDE UMA COISA, ISSO É RIMA DECORADA?",
            "MEU CÚ É O BATMAN, SEU PAU É O CHARADA",
            "DAHORA, EU GOSTEI, DEU PRA VER QUE É IMPROVISO",
            "MEU PAU NO SEU OUVIDO",
            "MAS VOCÊ NÃO GANHA DE MIM, ENTÃO JÁ TE DOU UM AVISO",
            "eu vou rimando e você tem que responder",
            "eu vou chupar a sua pica mano, e cê nem vai vê",
            "mano aqui é só improviso o que que você vai fazer",
            "vou fazer uma live, no câmera privê",
            "agora, legal, eu gostei da sua levada",
            "eu vou te dar uma mamada",
            "só me responde uma coisa, isso é rima decorada?",
            "meu cú é o batman, seu pau é o charada",
            "dahora, eu gostei, deu pra ver que é improviso",
            "meu pau no seu ouvido",
            "mas você não ganha de mim, então já te dou um aviso",
        ]
    )

    (main_menu
        .add_hop("n", "new modpack", new_menu)
        .add_hop("e", "edit modpack", edit_menu)
        .add_hop("d", "delete modpack", del_menu)
        .add_hop("l", "lyrics", lyrics_menu)
    )

    for menu in [new_menu, edit_menu, del_menu, lyrics_menu]:
        menu.add_hop("b", "back to main menu", main_menu)

    manager.start(main_menu)


termui.wrap_execute(window_error_test)

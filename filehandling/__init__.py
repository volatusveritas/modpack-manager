from io import TextIOWrapper
import os
import os.path
import json
from uuid import UUID, uuid4 as random_uuid

from filehandling import constants


modpack_file: TextIOWrapper | None = None


def assert_modpack_folder() -> None:
    if os.path.exists(constants.MODPACKS_DIR_PATH):
        return

    os.mkdir(constants.MODPACKS_DIR_PATH)


def new_modpack(name: str, description: str, version: str) -> None:
    assert_modpack_folder()

    identifier: UUID = random_uuid()
    new_modpack_file = open(os.path.join(
        constants.MODPACKS_DIR_PATH, f"{identifier.hex}.json"
    ))

    initial_modpack_content: dict = {
        "name": name,
        "description": description,
        "version": version,
        "mods": []
    }

    json.dump(initial_modpack_content, new_modpack_file)

    new_modpack_file.close()


def open_modpack(identifier: UUID) -> None:
    global modpack_file

    modpack_file = open(os.path.join(
        constants.MODPACKS_DIR_PATH, f"{identifier.hex}.json"
    ))


def delete_modpack(identifier: UUID) -> None:
    assert_modpack_folder()

    os.remove(os.path.join(
        constants.MODPACKS_DIR_PATH, f"{identifier.hex}.json"
    ))


def clean_exiting() -> None:
    if modpack_file:
        modpack_file.close()

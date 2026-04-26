# Created 2026-04-25

import json, os

import private

SCRIPT_DIR = private.SCRIPT_DIR
COMPLIMENTS_FILENAME = "compliments.json"

COMPLIMENTS_FILEPATH = os.path.join(SCRIPT_DIR, COMPLIMENTS_FILENAME)

def load_compliments() -> list[dict]:
    with open(COMPLIMENTS_FILEPATH, encoding="ascii") as file:
        return json.load(file)

def store_compliments(data: list[dict]) -> None:
    with open(COMPLIMENTS_FILEPATH, mode="w", encoding="ascii") as file:
        json.dump(data, file, ensure_ascii=True, indent=2)

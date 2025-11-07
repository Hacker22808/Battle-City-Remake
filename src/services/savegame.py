"""
Збереження прогресу: рівень, рахунок, налаштування гучності/керування. Формат JSON, валідація схеми.
"""

import json
import os

SAVE_FILE = "savegame.json"

default_save = {
    "level": 1,
    "score": 0,
    "settings": {
        "volume": 100,
        "controls": {
            "left": "A",
            "right": "D",
            "jump": "SPACE",
            "fire": "F"
        }
    }
}

def save_game(data):
    """Сохранение прогресса в JSON"""
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_game():
    """Загрузка прогресса, с валидацией"""
    if not os.path.exists(SAVE_FILE):
        return default_save.copy()
    with open(SAVE_FILE, "r") as f:
        data = json.load(f)
    # Простая валидация
    if "level" not in data or "score" not in data or "settings" not in data:
        return default_save.copy()
    return data

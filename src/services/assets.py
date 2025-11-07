"""
Сервіс завантаження/кешування ресурсів: читає resources.yaml, валідуючи наявність файлів; описує нотацію ключів і правила віддачі спрайтів/атласів/звуків/шрифтів.
"""

import os
import yaml
import pygame

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")

class ResourceManager:
    def __init__(self, yaml_file="resources.yaml"):
        self.yaml_file = yaml_file
        self.resources = {}  # raw data from yaml
        self.cache = {}      # loaded pygame objects
        self._load_yaml()

    def _load_yaml(self):
        path = os.path.join(ASSETS_DIR, self.yaml_file)
        if not os.path.exists(path):
            raise FileNotFoundError(f"{self.yaml_file} not found in assets folder")
        with open(path, "r", encoding="utf-8") as f:
            self.resources = yaml.safe_load(f)

    def _validate_file(self, filepath):
        full_path = os.path.join(ASSETS_DIR, filepath)
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"Resource file not found: {full_path}")
        return full_path

    def get(self, key):
        """
        Получение ресурса по ключу.
        Типы: image, atlas, sound, font
        """
        if key in self.cache:
            return self.cache[key]

        if key not in self.resources:
            raise KeyError(f"Resource key '{key}' not defined in {self.yaml_file}")

        res_info = self.resources[key]
        rtype = res_info.get("type")
        path = res_info.get("path")

        full_path = self._validate_file(path)

        if rtype == "image":
            obj = pygame.image.load(full_path).convert_alpha()
        elif rtype == "sound":
            obj = pygame.mixer.Sound(full_path)
        elif rtype == "font":
            size = res_info.get("size", 24)
            obj = pygame.font.Font(full_path, size)
        elif rtype == "atlas":
            # простой спрайтовый атлас: path = image, frames = [x, y, w, h]
            base_image = pygame.image.load(full_path).convert_alpha()
            frames = {}
            for frame_name, rect in res_info.get("frames", {}).items():
                x, y, w, h = rect
                frames[frame_name] = base_image.subsurface(pygame.Rect(x, y, w, h))
            obj = frames
        else:
            raise ValueError(f"Unknown resource type: {rtype}")

        self.cache[key] = obj
        return obj

# -----------------------------
# Пример использования
# -----------------------------
# resources.yaml
# player_image:
#   type: image
#   path: images/player.png
# explosion_sound:
#   type: sound
#   path: sounds/explosion.wav
# main_font:
#   type: font
#   path: fonts/verdana.ttf
#   size: 32
# enemy_atlas:
#   type: atlas
#   path: images/enemies.png
#   frames:
#       enemy1: [0,0,32,32]
#       enemy2: [32,0,32,32]

# Использование:
# from assets import ResourceManager
# res_mgr = ResourceManager()
# player_img = res_mgr.get("player_image")
# explosion = res_mgr.get("explosion_sound")
# font = res_mgr.get("main_font")
# enemy_frames = res_mgr.get("enemy_atlas")["enemy1"]

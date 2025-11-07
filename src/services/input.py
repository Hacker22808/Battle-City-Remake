"""
Мапінг клавіш → дії (вліво/вправо/вогонь/пауза). Підтримка ремапу та геймпада.
"""

import pygame

class InputManager:
    def __init__(self):
        # Стандартные настройки клавиш
        self.key_map = {
            "MOVE_LEFT": pygame.K_a,
            "MOVE_RIGHT": pygame.K_d,
            "FIRE": pygame.K_SPACE,
            "PAUSE": pygame.K_ESCAPE
        }
        # Для геймпада
        self.joystick = None
        pygame.joystick.init()
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()

    def remap_key(self, action, new_key):
        """Переназначить клавишу для действия"""
        self.key_map[action] = new_key

    def get_actions(self):
        """Возвращает текущие активные действия"""
        actions = []
        keys = pygame.key.get_pressed()

        if keys[self.key_map["MOVE_LEFT"]]:
            actions.append("MOVE_LEFT")
        if keys[self.key_map["MOVE_RIGHT"]]:
            actions.append("MOVE_RIGHT")
        if keys[self.key_map["FIRE"]]:
            actions.append("FIRE")
        if keys[self.key_map["PAUSE"]]:
            actions.append("PAUSE")

        # Проверка геймпада (пример для оси и кнопки A)
        if self.joystick:
            axis_x = self.joystick.get_axis(0)
            if axis_x < -0.5:
                actions.append("MOVE_LEFT")
            elif axis_x > 0.5:
                actions.append("MOVE_RIGHT")
            if self.joystick.get_button(0):  # кнопка A
                actions.append("FIRE")

        return actions

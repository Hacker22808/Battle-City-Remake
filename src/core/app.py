"""
«Компонозитор» застосунку: ініціалізує Pygame, створює сервіси (Assets, Audio, Input, UI, Physics), шину подій, менеджер сцен; запускає головний цикл (tick → handle_input → update → render).
Патерн: Application/Composition Root + Game Loop.
Використання: імпортується в run.py, де створюється екземпляр App і викликається метод запуску.
"""
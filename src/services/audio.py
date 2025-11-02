"""
Відтворення SFX і музики, глобальна гучність, одночасні канали. Маршрутизація подій зі звуком (наприклад, подія «HIT_STEEL» → звук стіни).
"""

import pygame

class AudioManager:
    def __init__(self, resources, sfx_volume=1.0, music_volume=1.0, max_channels=8):
        pygame.mixer.init()
        pygame.mixer.set_num_channels(max_channels)
        self.resources = resources
        self.sfx_volume = sfx_volume
        self.music_volume = music_volume
        self.sounds = {}
        self.load_sounds()

    def load_sounds(self):
        for name, path in self.resources['sounds'].items():
            self.sounds[name] = pygame.mixer.Sound(path)
            self.sounds[name].set_volume(self.sfx_volume)

    def play_sfx(self, name):
        if name in self.sounds:
            self.sounds[name].play()

    def play_music(self, name, loops=-1):
        if name in self.resources['sounds']:
            pygame.mixer.music.load(self.resources['sounds'][name])
            pygame.mixer.music.set_volume(self.music_volume)
            pygame.mixer.music.play(loops)

    def set_sfx_volume(self, volume):
        self.sfx_volume = volume
        for s in self.sounds.values():
            s.set_volume(volume)

    def set_music_volume(self, volume):
        self.music_volume = volume
        pygame.mixer.music.set_volume(volume)

    # Пример маршрутизации событий
    def handle_event(self, event_type):
        event_sound_map = {
            "HIT_STEEL": "hit_steel",
            "FIRE": "fire",
            "EXPLOSION": "explosion",
        }
        if event_type in event_sound_map:
            self.play_sfx(event_sound_map[event_type])

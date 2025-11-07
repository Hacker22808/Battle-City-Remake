"""
Узгодження часу кадру: дельта-час, таймери перезарядки/ефектів, планувальник відкладених подій (наприклад, інвертований контроль на льоду).
"""
"""
Управління ігровим часом та FPS
"""

import pygame

class GameClock:
    def __init__(self, target_fps: int = 60):
        self.clock = pygame.time.Clock()
        self.target_fps = target_fps
        self.delta_time = 0.0
        self.elapsed_time = 0.0
    
    def tick(self) -> float:
        self.delta_time = self.clock.tick(self.target_fps) / 1000.0
        self.elapsed_time += self.delta_time
        return self.delta_time
    
    def get_fps(self) -> float:
        return self.clock.get_fps()
    
    def set_target_fps(self, fps: int) -> None:
        self.target_fps = fps
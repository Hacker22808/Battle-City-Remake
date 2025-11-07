"""
Базовий контракт для сцен (Menu/Game/Pause): методи enter/exit, handle_events, update, render, запит переходів між сценами.
"""
"""
Менеджер сцен гри (меню, гра, пауза, game over)
"""

from typing import Dict, Optional


class Scene:
    
    def __init__(self, scene_manager):
        self.scene_manager = scene_manager
        self.settings = scene_manager.app.settings 
    
    def enter(self) -> None:
        pass                
    def exit(self) -> None:
        pass
    def handle_input(self) -> None:
        pass
    def update(self, dt: float) -> None:
        pass
    def render(self, screen) -> None:
        pass




class SceneManager:

    def __init__(self, event_bus, assets_service, audio_service, 
                 input_service, ui_service, physics_service):
        self.event_bus = event_bus
        self.assets_service = assets_service
        self.audio_service = audio_service
        self.input_service = input_service
        self.ui_service = ui_service
        self.physics_service = physics_service
        self.app = None
        
        self.scenes: Dict[str, Scene] = {}
        self.current_scene: Optional[Scene] = None
        self.current_scene_name: Optional[str] = None
    
    def set_app(self, app):
        self.app = app
    
    def register_scene(self, name: str, scene: Scene) -> None:
        self.scenes[name] = scene
    
    def switch_to(self, name: str) -> None:
        if name in self.scenes:
            if self.current_scene:
                self.current_scene.exit()
            
            self.current_scene = self.scenes[name]
            self.current_scene_name = name
            self.current_scene.enter()
    
    def update(self, dt: float) -> None:
        if self.current_scene:
            self.current_scene.update(dt)
    
    def render(self, screen) -> None:
        if self.current_scene:
            self.current_scene.render(screen)
    
    def handle_input(self) -> None:
        if self.current_scene:
            self.current_scene.handle_input()
    
    def cleanup(self) -> None:
        if self.current_scene:
            self.current_scene.exit()
        self.scenes.clear()
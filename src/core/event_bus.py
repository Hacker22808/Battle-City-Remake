
from typing import Dict, List, Callable, Any

class EventBus:
    
    def __init__(self):
        self._listeners: Dict[str, List[Callable]] = {}
    
    def subscribe(self, event_type: str, listener: Callable) -> None:
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(listener)
    
    def unsubscribe(self, event_type: str, listener: Callable) -> None:
        if event_type in self._listeners:
            self._listeners[event_type].remove(listener)
    
    def emit(self, event_type: str, *args, **kwargs) -> None:

        if event_type in self._listeners:
            for listener in self._listeners[event_type]:
                listener(*args, **kwargs)
    
    def clear(self) -> None:
        self._listeners.clear()
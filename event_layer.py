# event layer contains management for events
from typing import Dict, Any, Callable


class Event:
    def __init__(self, name: str, data: Dict[str, Any]):
        self.name = name
        self.data = data


class EventHandler:
    def __init__(self):
        self.handlers = {}

    def register(self, event_name: str, handler: Callable):
        self.handlers[event_name] = handler

    def handle(self, event: Event):
        if event.name in self.handlers:
            self.handlers[event.name](event.data)

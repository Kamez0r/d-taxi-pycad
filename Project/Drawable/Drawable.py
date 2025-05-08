from abc import ABC,abstractmethod

from PyQt6.QtCore import QPoint


class Drawable(ABC):

    position: QPoint

    def __init__(self, serialized_data: dict):
        raise TypeError("Drawable is an abstract class and cannot be instantiated directly")

    @abstractmethod
    def draw(self):
        raise NotImplementedError("Subclasses must implement draw()")

    @abstractmethod
    def get_serialized(self) -> dict:
        raise NotImplementedError("Subclasses must implement get_serialized()")

    @abstractmethod
    def load_from_serialized(self, serialized: dict):
        raise NotImplementedError("Subclasses must implement load_from_serialized()")
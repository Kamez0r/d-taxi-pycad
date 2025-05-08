from abc import abstractmethod

from PyQt6.QtCore import QPoint
from PyQt6.QtWidgets import QGraphicsItem


class Drawable(QGraphicsItem):

    position: QPoint

    @abstractmethod
    def __init__(self):
        super().__init__()

    @abstractmethod
    def get_serialized(self) -> dict:
        raise NotImplementedError("Subclasses must implement get_serialized()")

    @abstractmethod
    def load_from_serialized(self, serialized: dict):
        raise NotImplementedError("Subclasses must implement load_from_serialized()")
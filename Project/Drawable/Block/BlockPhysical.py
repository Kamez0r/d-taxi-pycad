from abc import abstractmethod

from PyQt6.QtGui import QColor

from Project.GeoCoordinate import GeoCoordinate
from Project.Drawable.Block.Block import Block


class BlockPhysical(Block):

    geo_pos: GeoCoordinate

    def __init__(self):
        super().__init__()
        self.penColor = QColor(0, 0, 255)
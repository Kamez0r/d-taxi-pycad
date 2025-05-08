from abc import ABC, abstractmethod

from Project import Drawable


class Block(Drawable, ABC):
    pass

    # Inherits:
    # __init__(serialized_data)
    # draw()
    # get_serialized()
    # load_from_serialized(serialized)

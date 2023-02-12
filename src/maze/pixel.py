from enum import Enum

class PixelType(Enum):
    UNSET = 0
    WALL = 1
    FREE = 2
    KEY = 3
    ZONE = 4
    START = 5
    END = 6

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, PixelType):
            return NotImplemented
        
        return self.value < other.value

class Pixel:
    def __init__(self, color, pixel_type=PixelType.UNSET) -> None:
        self.color: tuple[int, int, int] = color
        self.type: PixelType = pixel_type

    def is_grey(self) -> bool:
        return self.color[0] == self.color[1] == self.color[2]



__all__ = ['Pixel', 'PixelType']
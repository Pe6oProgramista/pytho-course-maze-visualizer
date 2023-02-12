from src.maze.pixel import Pixel, PixelType

def test_pixel_type_ordering():
    assert PixelType.UNSET < PixelType.WALL
    assert PixelType.WALL < PixelType.FREE
    assert PixelType.FREE < PixelType.KEY
    assert PixelType.KEY < PixelType.ZONE
    assert PixelType.ZONE < PixelType.START
    assert PixelType.START < PixelType.END

def test_pixel_grey_detection():
    grey_pixel = Pixel((128, 128, 128))
    non_grey_pixel = Pixel((255, 0, 0))

    assert grey_pixel.is_grey() is True
    assert non_grey_pixel.is_grey() is False
import os
import png, array
import sys

class Playground:
    def __init__(self, screenshot_path):
        (w, h, pixels, metadata) = read_screenshot(screenshot_path)
        self.width = w
        self.height = h
        self.pixels = pixels
        self.metadata = metadata

    def is_black(self, x, y):
        pixel = self.pixel_at(x,y)
        return pixel[0] == 33 and pixel[1] == 32 and pixel[2] == 31

    def is_gray(self, x, y):
        pixel = self.pixel_at(x, y)
        return pixel[0] == 58 and pixel[1] == 56 and pixel[2] == 54

    def pixel_at(self, x, y):
        pixel_byte_width = 4 if self.metadata['alpha'] else 3
        pixel_position = x + y * self.width
        return self.pixels[pixel_position * pixel_byte_width : (pixel_position + 1) * pixel_byte_width]

def read_screenshot(screenshot_path):
    reader = png.Reader(filename = screenshot_path)
    w, h, pixels, metadata = reader.read_flat()
    return (w, h, pixels, metadata)

if __name__ == '__main__':
    screenshot_name = sys.argv[1]
    ss = Playground(screenshot_name)
    print ss.is_gray(312, 703)

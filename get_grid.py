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
        self.intersections = False
        self.tile_width = False
        self.tile_height = False
        self.start_intersection = False
        self.topleft_point = False
        self.inset = False

    def is_black(self, x, y):
        pixel = self.pixel_at(x,y)
        return pixel[0] == 33 and pixel[1] == 32 and pixel[2] == 31

    def is_kinda_black(self, x, y):
        pixel = self.pixel_at(x, y)
        min = 28
        max = 42
        return pixel[0] >= min and pixel[0] < max and pixel[1] >= min and pixel[1] < max and pixel[2] >= min and pixel[2] <max

    def is_gray(self, x, y):
        pixel = self.pixel_at(x, y)
        return pixel[0] == 58 and pixel[1] == 56 and pixel[2] == 54

    def is_kinda_gray(self, x, y):
        pixel = self.pixel_at(x, y)
        min = 50
        max = 65
        return pixel[0] >= min and pixel[0] < max and pixel[1] >= min and pixel[1] < max and pixel[2] >= min and pixel[2] < max

    def is_intersection(self, x, y):
        top_left = (x, y)
        top_right = (x + 5, y)
        bottom_left = (x, y + 5)
        bottom_right = (x + 5, y + 5)
        return self.is_black(x, y) and self.is_gray(x + 5, y) and self.is_gray(x, y + 5) and self.is_black(x + 5, y + 5)
        

    def pixel_at(self, x, y):
        pixel_byte_width = 4 if self.metadata['alpha'] else 3
        pixel_position = x + y * self.width
        return self.pixels[pixel_position * pixel_byte_width : (pixel_position + 1) * pixel_byte_width]

    def get_intersections(self):
        if (self.intersections):
            return self.intersections
        intersections = []
        for x in range(0, self.width):
            for y in range(0, self.height):
                if self.is_intersection(x, y):
                    intersections.append((x, y))
        self.intersections = intersections
        return self.intersections

    def get_tile_width(self):
        if self.tile_width:
            return self.tile_width
        
        intersections = self.get_intersections()
        for i in range(0, len(intersections) - 1):
            (x1, y1) = intersections[i]
            (x2, y2) = intersections[i + 1]
            if (x1 != x2 and x1 + 1 != x2):
                self.tile_width = abs(x1 - x2)
                return self.tile_width
        raise ValueError('Expected to have found more than one item in intersections that differ')

    def get_tile_height(self):
        if self.tile_height:
            return self.tile_height
        
        intersections = self.get_intersections()
        current_y = -1
        ys = []
        for i in range(0, len(intersections)):
            (x, y) = intersections[i]
            if current_y != y:
                current_y = y
                ys.append(current_y)
        for i in range(0, len(ys) - 1):
            current_y = ys[i]
            next_y = ys[i + 1]
            if current_y + 1 != next_y:
                self.tile_height = abs(current_y - next_y) / 2 # this is because the vertical pattern only repeats every two lines
                return self.tile_height
            
        raise ValueError('Expected to have found more than one item in intersections that differ')

    def get_topleft_point(self):
        if self.topleft_point:
            return self.topleft_point

        intersections = self.get_intersections()
        (x, y) = intersections[0]
        min_x = x
        for inside in range(0,5):
            leftmost_point = ((x - self.get_tile_width() + inside), (y - self.get_tile_height() + inside))
            if self.is_black(leftmost_point[0], leftmost_point[1]):
                self.topleft_point = leftmost_point
                self.inset = inside
                return self.topleft_point
        raise ValueError('Could not find a leftmost point')

    def get_tile_tops(self):
        topleft = self.get_topleft_point()
        tile_width = self.get_tile_width()
        tile_height = self.get_tile_height()
        res = []
        for x in range(topleft[0], self.width - self.inset, tile_width + self.inset):
            for y in range(topleft[1], self.height - self.inset, tile_height + self.inset):
                if self.is_kinda_black(x, y) or self.is_kinda_gray(x, y):
                    res.append((x, y))
        return res
        

def read_screenshot(screenshot_path):
    reader = png.Reader(filename = screenshot_path)
    w, h, pixels, metadata = reader.read_flat()
    return (w, h, pixels, metadata)

if __name__ == '__main__':
    screenshot_name = sys.argv[1]
    ss = Playground(screenshot_name)
    tt = ss.get_tile_tops()
    print tt
    print len(tt)

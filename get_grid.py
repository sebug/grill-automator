import os
import png, array
import sys
import glob

class Playground:
    def __init__(self, screenshot_path):
        (w, h, pixels, metadata) = read_image(screenshot_path)
        tile_paths = glob.glob('tiles/*.png')
        tiles_and_path = map(lambda p: (p.replace('tiles/','').replace('.png',''), p), tile_paths)
        self.tile_dict = {}
        for t in tiles_and_path:
            self.tile_dict[t[0]] = read_image(t[1])

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
        self.tile_tops = False
        self.color_averages = False
        self.whitecounts = False

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

    def is_kinda_white(self, x, y):
        pixel = self.pixel_at(x, y)
        return pixel[0] >= 250 and pixel[1] >= 250 and pixel[2] >= 250

    def is_intersection(self, x, y):
        top_left = (x, y)
        top_right = (x + 5, y)
        bottom_left = (x, y + 5)
        bottom_right = (x + 5, y + 5)
        return self.is_black(x, y) and self.is_gray(x + 5, y) and self.is_gray(x, y + 5) and self.is_black(x + 5, y + 5)
        

    def pixel_at(self, x, y):
        return self.pixel_at_for_image(x, y, self.width, self.metadata, self.pixels)

    def pixel_at_for_image(self, x, y, width, metadata, pixels):
        pixel_byte_width = 4 if metadata['alpha'] else 3
        pixel_position = x + y * width
        return pixels[pixel_position * pixel_byte_width : (pixel_position + 1) * pixel_byte_width]

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
        if self.tile_tops:
            return self.tile_tops
        
        topleft = self.get_topleft_point()
        tile_width = self.get_tile_width()
        tile_height = self.get_tile_height()
        res = []
        for x in range(topleft[0], self.width - self.inset, tile_width + self.inset):
            for y in range(topleft[1], self.height - self.inset, tile_height + self.inset):
                if self.is_kinda_black(x, y) or self.is_kinda_gray(x, y):
                    res.append((x, y))

        self.tile_tops = res
        return self.tile_tops

    def color_average(self, topx, topy):
        sum_red = 0
        sum_green = 0
        sum_blue = 0
        tile_width = self.get_tile_width()
        tile_height = self.get_tile_height()
        total_traversed = 0
        for x in range(topx, topx + tile_width):
            for y in range(topy, topy + tile_height):
                if not self.is_kinda_black(x, y) and not self.is_kinda_gray(x, y):
                    total_traversed += 1
                    pixel = self.pixel_at(x, y)
                    sum_red += pixel[0]
                    sum_green += pixel[1]
                    sum_blue += pixel[2]

        if total_traversed == 0:
            return self.pixel_at(topx, topy)
        else:
            return (sum_red / total_traversed,
                    sum_green / total_traversed,
                    sum_blue / total_traversed)

    def get_white_pixel_count(self, topx, topy):
        whitecount = 0
        tile_width = self.get_tile_width()
        tile_height = self.get_tile_height()
        for x in range(topx, topx + tile_width):
            for y in range(topy, topy + tile_height):
                if self.is_kinda_white(x, y):
                    whitecount += 1
        return whitecount

    def pixel_diff(self, pixel1, pixel2):
        return abs(pixel1[0] - pixel2[0]) + abs(pixel1[1] - pixel2[1]) + abs(pixel1[2] - pixel2[2])

    def difference_to(self, tileName, topx, topy):
        (tile_width, tile_height, pixels, metadata) = self.tile_dict[tileName]
        min_width = min(self.tile_width, tile_width)
        min_height = min(self.tile_height, tile_height)
        total_difference = 0
        for x in range(0, min_width):
            for y in range(0, min_height):
                px1 = self.pixel_at_for_image(x + topx, y + topy, self.width, self.metadata, self.pixels)
                px2 = self.pixel_at_for_image(x, y, tile_width, metadata, pixels)
                total_difference += self.pixel_diff(px1, px2)
        return total_difference

    def get_color_averages(self):
        if self.color_averages:
            return self.color_averages
        averages = []
        for top in self.get_tile_tops():
            avg = self.color_average(top[0], top[1])
            averages.append((top,avg))
        self.color_averages = averages
        return self.color_averages

    def get_whitecounts(self):
        if self.whitecounts:
            return self.whitecounts
        whitecounts = []
        for top in self.get_tile_tops():
            wc = self.get_white_pixel_count(top[0], top[1])
            whitecounts.append((top,wc))
        self.whitecounts = whitecounts
        return self.whitecounts
        
    def representation_grid(self):
        ys = []
        xs = []
        tile_tops = self.get_tile_tops()
        for ca in tile_tops:
            y = ca[1]
            x = ca[0]
            if not (x in xs):
                xs.append(x)
            if not (y in ys):
                ys.append(y)
        # now make the grid
        grid = []
        for y in ys:
            line = []
            for x in xs:
                symbol = ' '
                t = (x, y)
                matching = filter(lambda ca: ca == t, tile_tops)
                if len(matching) > 0:
                    tile_tuples = [('fish', 'F'), ('sausage', 'W'), ('steak', 'S'), ('corn', 'M'), ('cheese', 'K'), ('potato', '0'), ('burger', '2'), ('paprika', 'P'), ('skewer', '1'), ('empty', ' ')]
                    differences = map(lambda tile: self.difference_to(tile[0], x, y), tile_tuples)
                    min_diff = min(differences)
                    tile_index = differences.index(min_diff)
                    tile_symbol = tile_tuples[tile_index][1]
                line.append(tile_symbol)
            grid.append(line)
        
        return grid
        

def read_image(screenshot_path):
    reader = png.Reader(filename = screenshot_path)
    w, h, pixels, metadata = reader.read_flat()
    return (w, h, pixels, metadata)

if __name__ == '__main__':
    screenshot_name = sys.argv[1]
    ss = Playground(screenshot_name)
    grid = ss.representation_grid()
    for line in grid:
        print ''.join(line)







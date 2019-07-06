import os
import png, array

adb_path = '~/Library/Android/sdk/platform-tools/adb'

def adb_do(cmd):
    os.system(adb_path + ' ' + cmd)

def get_current_screenshot():
    adb_do('shell screencap -p /sdcard/screen.png')
    adb_do('pull /sdcard/screen.png')

def read_screenshot():
    reader = png.Reader(filename = 'screen.png')
    w, h, pixels, metadata = reader.read_flat()
    return (w,h,pixels,metadata)

def pixels_to_tuple_array(w, h, pixels):
    tuple_array = []
    pixel_byte_width = 3
    for y in range(0, h):
        line_array = []
        for x in range(0, w):
            pixel_position = y * w
            line_array.append(pixels[pixel_position * pixel_byte_width : (pixel_position + 1) * pixel_byte_width])
        tuple_array.append(line_array)
    return tuple_array

def is_white_pixel(pixel):
    return pixel[0] == 255 and pixel[1] == 255 and pixel[2] == 255

# but skip first black pixel on every line
def is_white_line(line):
    for pixel in line[5:-5]:
        if not is_white_pixel(pixel):
            return False
    return True

def line_sum(line):
    result = 0
    for pixel in line:
        result += sum(pixel)
    return result

def get_grid(w, h, pixels):
    print (w, h)

def get_last_white_line(pixel_array):
    y = -1
    last_line = -1
    previous_line = pixel_array[0]
    for line in pixel_array:
        y += 1
        if is_white_line(line) and is_white_line(previous_line):
            last_line = y
        previous_line = line
    return last_line

# idea: find an intersection between four tiles and go from there
def is_edge_pixel(y,x,pixels):
    return False

if __name__ == '__main__':
    # get_current_screenshot()
    ss = read_screenshot()
    pixel_array = pixels_to_tuple_array(ss[0], ss[1], ss[2])
    height = len(pixel_array)
    width = len(pixel_array[0])
    for y in range(1,height - 1):
        for x in range(1,width - 1):
            is_edge_pixel(y, x)





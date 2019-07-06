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

def get_grid(w, h, pixels):
    print (w, h)

if __name__ == '__main__':
    # get_current_screenshot()
    ss = read_screenshot()
    pixel_array = pixels_to_tuple_array(ss[0], ss[1], ss[2])
    for line in pixel_array:
        print is_white_line(line)




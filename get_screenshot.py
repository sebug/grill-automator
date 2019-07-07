import os
import png, array
import sys

adb_path = '~/Library/Android/sdk/platform-tools/adb'

def adb_do(cmd):
    os.system(adb_path + ' ' + cmd)

def get_current_screenshot():
    adb_do('shell screencap -p /sdcard/screen.png')
    adb_do('pull /sdcard/screen.png')

def read_screenshot(screenshot_path):
    reader = png.Reader(filename = screenshot_path)
    # todo - resize according to tile size
    w, h, pixels, metadata = reader.read_flat()
    return (w,h,pixels,metadata)

if __name__ == '__main__':
    get_current_screenshot()
    print 'Got screenshot'




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

if __name__ == '__main__':
    get_current_screenshot()
    print read_screenshot()


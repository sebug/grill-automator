# Notes Grill Automator
Using adb to get a screenshot

	./adb shell screencap -p /sdcard/screen.png
	./adb pull /sdcard/screen.png

The tool is here: ~/Library/Android/sdk/platform-tools

	./adb shell input swipe 611 911 626 1000

Swipe to exchange blocks.


To solve:

	python get_grid.py sample_screenshots/6.png | ruby suggest.rb i

"""import pyautogui, time

color = None

def report(color):
    loc = pyautogui.position()
    color = pyautogui.screenshot().getpixel(loc)
    print("position is:",loc,"color is",color)
    return color

while True:
    colors = report(color)
    time.sleep(0.5)
    if colors == (181, 71, 71):
        break"""

import pyautogui, time

color = None

def report():
    loc = pyautogui.position()
    global color #表示local要修改全域變數color
    color = pyautogui.screenshot().getpixel(loc)
    print("position is:",loc,"color is",color)


while True:
    report()
    time.sleep(0.5)
    if color == (181, 71, 71):
        break
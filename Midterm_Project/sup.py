import pyautogui
import time

#補充: 讀取當前滑鼠位置的像素顏色
def show_pixel_color():
    print("5 秒後讀取當前滑鼠位置像素顏色...")
    time.sleep(5)
    x, y = pyautogui.position()
    rgb = pyautogui.screenshot().getpixel((x, y))
    print(f"你現在指的位置 ({x},{y}) 的顏色是：{rgb}")

show_pixel_color()
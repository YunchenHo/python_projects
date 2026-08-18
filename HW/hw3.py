import pyautogui
import time
import subprocess

def switch_to_english():
    subprocess.run(r"powershell.exe Set-WinUserLanguageList en-US -Force", shell=True)
    time.sleep(0.5)

pyautogui.PAUSE = 1

# 1. 打開 Chrome
pyautogui.hotkey('win', 'r')
time.sleep(0.5)
pyautogui.typewrite('chrome')
pyautogui.press('enter')

# 2. 確保輸入法是英文
switch_to_english()

# 3. 選擇網址列
pyautogui.hotkey('ctrl', 'l')
time.sleep(0.5)

# 4. 輸入網址
pyautogui.write('https://sketch.io/sketchpad/', interval=0.01)
pyautogui.press('enter')
time.sleep(0.5)

#畫樹
#
pyautogui.moveTo(960,200)
pyautogui.dragRel(-100,100, 3)
pyautogui.dragRel(50,0, 3)
pyautogui.dragRel(-100,100, 3)
pyautogui.dragRel(50,0, 3)
pyautogui.dragRel(-100,100, 3)

pyautogui.dragTo(940,500,3)
pyautogui.dragRel(0,100, 3)
pyautogui.dragRel(40,0, 3)
pyautogui.dragRel(0,-100, 3)

pyautogui.moveTo(960,200)
pyautogui.mouseDown()
pyautogui.moveRel(100,100, 3)
pyautogui.moveRel(-50,0, 3)
pyautogui.moveRel(100,100, 3)
pyautogui.moveRel(-50,0, 3)
pyautogui.moveRel(100,100, 3)
pyautogui.moveTo(980,500, 3)
pyautogui.mouseUp()

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
pyautogui.write('https://www.geogebra.org/classic', interval=0.01)
pyautogui.press('enter')
time.sleep(0.5)

pyautogui.click(305, 214, 1)
pyautogui.click(305, 240, 1)
time.sleep(0.5)

pyautogui.click(1172, 457, 1)
pyautogui.click(1024, 677, 1)
pyautogui.click(1323, 677, 1)
pyautogui.click(1172, 457, 1)
import pyautogui
import time

def wait_pic(pic, timeout=10):

    #等待pic圖片出現在螢幕上，最多等待timeout秒
    start_time = time.time()
    while True:
        try:
            found = pyautogui.locateOnScreen(pic, confidence=0.8)
            if found:
                print(f"找到圖片 {pic} 在 {found}")
                return found
        except Exception as e:
            print(f"發生錯誤：{e}")

        if time.time() - start_time > timeout:
            print(f"Timeout: {pic} 沒找到！")
            return None  # 超時後回傳None，避免無限等待

        time.sleep(0.5)  # 每0.5秒檢查一次


def click_all(pic):
    found_locations = list(pyautogui.locateAllOnScreen(pic, confidence=0.8))

    if not found_locations:
        print(f"未找到 {pic}，無法點擊！")
        return

    for loc_i in found_locations:
        print("找到圖片位置：", loc_i)
        center = pyautogui.center(loc_i)
        print("計算中心點：", center)
        pyautogui.moveTo(center, duration=0.5)  # 移動到該位置
        pyautogui.click(center)  # 點擊該位置


# 主執行流程
found = wait_pic('box.png')

if found:
    click_all('box.png')
else:
    print("未找到圖片，程式結束。")

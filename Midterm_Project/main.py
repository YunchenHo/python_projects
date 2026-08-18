import pyautogui
import subprocess
import cv2
import numpy as np
from PIL import ImageGrab
import time
import colorsys
import sys


#新手教學: 找空白區域
def find_image_on_screen(template_path, confidence=0.7, timeout=10, region=None, bottom_center=False):
    print(f"尋找圖像: {template_path}（最長等待 {timeout} 秒）")
    start_time = time.time()

    while time.time() - start_time < timeout:
        location = pyautogui.locateOnScreen(template_path, confidence=confidence, region=region)
        if location:
            if bottom_center:
                center_x = location.left + location.width // 2
                center_y = location.top + location.height
            else:
                center = pyautogui.center(location)
                center_x, center_y = center.x, center.y

            point = pyautogui.Point(center_x, center_y)
            print(f"✅ 找到位置: {point}")
            return point

        time.sleep(0.2)

    print("❌ 超過時間仍找不到圖像")
    return None


#新手教學: 找積木
def find_image_on_block(template_path, confidence=0.7):
    return find_image_on_screen(template_path, confidence=confidence, timeout=10, region=(1100, 300, 250, 350))


#新手教學: 拖曳積木(找圖片的方式)
def drag_piece_to_target(piece_img, target_img):
    piece_pos = find_image_on_block(piece_img)
    target_pos = find_image_on_screen(target_img, bottom_center=True)

    if piece_pos and target_pos:
        pyautogui.moveTo(piece_pos.x, piece_pos.y, duration=0.3)
        pyautogui.mouseDown()
        time.sleep(0.2)
        pyautogui.moveTo(target_pos.x, target_pos.y, duration=0.5)
        pyautogui.mouseUp()
        print("完成拖曳拼圖")
    else:
        print("無法完成拖曳，請確認圖像正確")


#新手教學: 拖曳積木(找座標的方式)
def drag_piece_to_target_by_coord(piece_coord, target_coord):
    print(f"從 {piece_coord} 拖曳到 {target_coord}")
    pyautogui.moveTo(piece_coord[0], piece_coord[1], duration=0.3)
    pyautogui.mouseDown()
    time.sleep(0.2)
    pyautogui.moveTo(target_coord[0], target_coord[1], duration=0.5)
    pyautogui.mouseUp()
    print("✅ 完成拖曳拼圖")

pyautogui.PAUSE = 1

GRID_ORIGIN = (685, 342)  # 棋盤左上角的格子中心點（你需要微調）
GRID_SIZE = 47            # 每格寬高 px
GRID_WIDTH = 9            # 棋盤寬度（格子數量）

# 右側三個區塊（大概座標範圍）
BLOCK_AREAS = [
    (1210, 325, 70, 100),
    (1210, 450, 70, 100),
    (1210, 575, 70, 100),
]

# 這個函數會計算格子中心點的座標
def get_cell_center(row, col):
    x = GRID_ORIGIN[0] + col * GRID_SIZE
    y = GRID_ORIGIN[1] + row * GRID_SIZE
    return x, y

# 這個函數會檢查兩個顏色是否相似
def is_similar(c1, c2, tolerance=8):
    return all(abs(a - b) <= tolerance for a, b in zip(c1, c2))

# 這個函數會檢查某個格子是否為空白
def is_cell_empty(x, y):
    rgb = pyautogui.screenshot().getpixel((x, y))
    empty_colors = [(35, 9, 2), (52, 25, 9), (61, 30, 10)]
    return any(is_similar(rgb, c) for c in empty_colors)

# 這個函數會檢查某個區域是否有方塊
def detect_block_in_area(area):
    img = pyautogui.screenshot(region=area)
    pixels = img.getcolors(maxcolors=10000)
    if len(pixels) >= 250:  # 有多種顏色表示可能有方塊
        return True
    return False

# 這個函數會計算區域內與目標顏色相似的像素數量
def count_similar_pixels(img, target_rgb, tolerance=7):
    pixels = img.getdata()
    return sum(1 for px in pixels if is_similar(px, target_rgb, tolerance))

# 這個函數會檢查區域內的方塊是否被禁用(灰階)--實際上是檢查方塊顏色是否變灰階(但效果不太好)
def is_block_disabled(index, target_color=(177, 126, 75), tolerance=7, threshold_ratio=0.1):
    area = BLOCK_AREAS[index]
    img = pyautogui.screenshot(region=area)
    total_pixels = img.width * img.height
    similar_count = count_similar_pixels(img, target_color, tolerance)
    return (similar_count / total_pixels) > threshold_ratio

# 這個函數會拖曳方塊到指定位置
def drag_block(index, to_x, to_y):
    # 假設三個方塊固定抓中央點當起點
    src_area = BLOCK_AREAS[index]
    from_x = src_area[0] + src_area[2] // 2
    from_y = src_area[1] + src_area[3] // 2

    pyautogui.moveTo(from_x, from_y, duration=0.2)
    pyautogui.mouseDown()
    time.sleep(0.15)
    pyautogui.moveTo(to_x, to_y, duration=0.2)
    pyautogui.mouseUp()

# 這個函數會檢查是否所有區域都已更新方塊(每次要從第一個方塊開始拖曳)
def wait_for_blocks_ready(required_passes=2, max_wait=2):
    passes = 0
    start_time = time.time()

    while time.time() - start_time < max_wait:
        results = [detect_block_in_area(area) for area in BLOCK_AREAS]

        if all(results):
            passes += 1
            if passes >= required_passes:
                print(f"✅ 連續 {required_passes} 次偵測成功，刷新完成")
                return [0, 1, 2]  # 全部區域都可用
        else:
            failed_indexes = [i for i, ok in enumerate(results) if not ok]
            print(f"⏳ 第 {passes + 1} 次檢查失敗，尚未刷新區域: {failed_indexes}")
            passes = 0

        time.sleep(0.05)

    print("⚠️ 等待刷新失敗，可能有未更新區域")
    return [i for i, ok in enumerate(results) if ok]  # 只返回成功的 index


#這個函數會檢查是否需要看廣告，廣告是否播放完畢
def handle_ad_continue():
    try:
        # Step 1: 嘗試找綠色 CONTINUE
        location = pyautogui.locateCenterOnScreen("green_continue.png", confidence=0.6)

        if location:
            print("🟩 找到綠色 CONTINUE，點擊播放廣告")
            time.sleep(0.2)
            pyautogui.click(871,588)
            # Step 2: 等待廣告播放
            print("⏳ 廣告播放中...")
            time.sleep(18)
            return True

        elif not location:
            print("🟩 沒有出現綠色 CONTINUE 按鈕")
            return False

    except pyautogui.ImageNotFoundException:
        print("🔍 綠色 CONTINUE 按鈕沒找到")
        return False

#這個函數會檢查是否有遊戲結束的畫面
def find_image_opencv(template_path, threshold=0.8):
    # 截圖整個螢幕
    screenshot = ImageGrab.grab()
    screenshot_np = np.array(screenshot)

    # 轉換成灰階
    screenshot_gray = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(template_path, 0)  # 0 表示以灰階讀取

    result = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(result >= threshold)

    if len(loc[0]) > 0:
        print("🖼️ 圖片已出現，準備結束程式")
        return True
    else:
        return False


#這個函數會重複拖曳每個方塊到空白區域直到成功放置，從左下開始往右上找空白區域
def try_place_block_until_success(index, threshold=100):
    area = BLOCK_AREAS[index]

    # 拖曳前：擷取來源區域的顏色數量
    before_img = pyautogui.screenshot(region=area)
    before_colors = before_img.getcolors(maxcolors=10000)
    before_color_count = len(before_colors)
    print(f"🎨 拖曳前色彩種類數量：{before_color_count}")


    for row in reversed(range(GRID_WIDTH)):  # 從下往上
        for col in range(GRID_WIDTH):        # 從左到右
            cx, cy = get_cell_center(row, col)
            if is_cell_empty(cx, cy) and not is_block_disabled(index):
                if handle_ad_continue():
                    print("成功進廣告重玩!")
                    return False

                elif find_image_opencv("game_over.png", threshold=0.8):
                    print("不要再找了，遊戲結束!")
                    return False

                elif find_image_opencv("milestone2.png", threshold=0.8):
                    print("不要再找了，遊戲結束!")
                    return False

                elif before_color_count < 300:
                    print("暫時沒有小方塊，先跳過!")
                    return False

                else:
                    time.sleep(0.35)
                    drag_block(index, cx, cy)
                    time.sleep(0.15)  # 等待動畫完成

                    # 拖曳後：擷取相同區域，再比一次顏色數
                    after_img = pyautogui.screenshot(region=area)
                    after_colors = after_img.getcolors(maxcolors=10000)
                    after_color_count = len(after_colors)
                    print(f"🎨 拖曳後色彩種類數量：{after_color_count}")

                    if after_color_count > before_color_count or 0 < before_color_count - after_color_count < threshold:
                        print(f"⚠️ 疑似截到新方塊，跳過這一塊")
                        return False
                    # 如果顏色數量明顯變少，視為方塊成功被移走
                    elif before_color_count - after_color_count >= threshold:
                        print(f"✅ 方塊 {index} 成功放置（顏色明顯變少）")
                        return True
                    else:
                        print(f"⚠️ 嘗試放在 ({row}, {col}) 失敗，顏色未變少")
    return False


#這個函數會不斷檢查遊戲狀態，直到遊戲結束或達到某個里程碑
def play_until_stopped():
    round_num = 0

    while True:
        if find_image_opencv("game_over.png", threshold=0.8) or find_image_opencv("milestone2.png", threshold=0.8):
            print("🎉程式結束")
            break

        round_num += 1
        print(f"第{round_num}輪開始")

        available_indexes = wait_for_blocks_ready()
        print(f"🟩 本輪可用的區域 index：{available_indexes}")

        for i in available_indexes:
            time.sleep(0.1)
            placed = try_place_block_until_success(i)
            if not placed:
                print(f"⚠️ 方塊 {i} 無法放置")
                if find_image_opencv("game_over.png", threshold=0.8) or find_image_opencv("milestone2.png", threshold=0.8):
                    print("主程式已偵測到遊戲結束畫面")
                    break
        time.sleep(0.5)


#主程式
subprocess.Popen(['start', 'chrome.exe', '--incognito', 'https://www.crazygames.com/game/wood-block-journey'], shell=True)
time.sleep(8)

#按下play_now
pyautogui.click(868, 612)
time.sleep(8)

#新手教學部分
drag_piece_to_target_by_coord((1246, 379), (874, 535))
time.sleep(1.5)
drag_piece_to_target("newHand_block2.png", "newHand_box2.png")
time.sleep(1.5)
drag_piece_to_target("newHand_block3.png", "newHand_box3.png")
time.sleep(1.5)
drag_piece_to_target("newHand_block4.png", "newHand_box4.png")
time.sleep(5)

#開始實際玩的過程
play_until_stopped()
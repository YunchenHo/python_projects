import pyautogui
import time

#補充: 截圖特定區域

# 等待 10 秒（你有時間切到想截圖的畫面）
print("⏳ 將在 10 秒後自動截圖...")
time.sleep(10)

# 自訂你要截圖的區域座標（左上角 + 寬高）
region = (695, 300, 348, 348)  # (left, top, width, height)

# 擷取該區域畫面
screenshot = pyautogui.screenshot(region=region)

# 儲存圖片
screenshot.save("game_over1.png")
print("📸 截圖完成")

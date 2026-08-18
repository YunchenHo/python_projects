# python_projects

課堂作業與練習專案的集合，內容如下：

## 資料夾說明

### Final_Project — Telegram 撲克 Bot
用 [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) 寫的 Telegram 德州撲克小遊戲，真人玩家對戰 3 個電腦玩家（各自有簡單策略）。
- `main.py`：正式版主程式（`/start` 開局、`/deal` 發牌，按鈕操作下注/棄牌/All in）
- `main2.py` / `main_prac.py`：開發過程中的其他版本
- `poker.py`：牌型評分邏輯（洗牌、產生牌組、判斷牌型）
- `poker_prac.py`：`poker.py` 的練習/草稿版
- `test_bot.py` / `test_bot_judgeCard.py`：功能測試用的簡化 bot
- `mytoken.py`（**未上傳**）：存放 Telegram Bot token，見下方「執行前準備」

### Midterm_Project — 螢幕自動化 / 影像辨識腳本
用 `pyautogui` + `opencv` 抓螢幕截圖比對圖片位置，自動偵測遊戲畫面（`milestone*.png`、`newHand_*.png` 等為比對用的素材圖），並自動操作滑鼠。

### HW — 作業練習
一系列 `pyautogui` 自動化操作練習（切換輸入法、等待畫面元素出現、抓取滑鼠位置顏色等）。

### PracForLecture — 上課練習
隨堂練習程式碼（猜數字遊戲邏輯、九宮格、`itertools`/`random` 練習等）。

## 執行前準備

1. 建立並啟用虛擬環境：
   ```bash
   python -m venv .venv
   .venv\Scripts\Activate.ps1   # Windows PowerShell
   ```

2. 安裝套件：
   ```bash
   pip install -r requirements.txt
   ```

3. 若要跑 `Final_Project`（Telegram Bot），需自行建立 `Final_Project/mytoken.py`，內容如下（token 向 [@BotFather](https://t.me/BotFather) 申請）：
   ```python
   token = "你的 Telegram Bot Token"
   ```
   此檔案已列在 `.gitignore`，不會被提交，避免 token 外洩。

4. `HW` 與 `Midterm_Project` 內的腳本使用 `pyautogui` 做螢幕自動化，僅在有畫面的 Windows 環境下可執行，且部分腳本（如 `hw1.py`~`hw3.py`）會呼叫 PowerShell 切換輸入法，僅限 Windows。

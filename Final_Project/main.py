# 引入必要模組
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from poker import generate_deck, shuffle_deck, evaluate_hand
from mytoken import token


player_names = ["Computer1", "Computer2", "Computer3", "YunChen Ho"]  # 玩家名稱，最後一位為真人玩家
money = [100, 100, 100, 100]  # 玩家起始金額
status = [None, None, None, None]  # 玩家目前狀態（BET、FOLD、ALL IN）
rnd = 0  # 第幾回合
stage = 0  # 當前輪次（2 = PREFLOP, 4 = FLOP, 6 = TURN, 8 = RIVER）
community = ""  # 公共牌顯示字串
bet = [0, 0, 0, 0]  # 各玩家本輪投注金額
hand_raw = [[], [], [], []]  # 每位玩家的兩張手牌
community_raw = []  # 共五張公共牌
deck = []  # 當前牌堆
all_in_flag = [False, False, False, False]  # 各玩家是否已經 ALL IN
f_fold_skip = False  # 玩家若棄牌，是否跳過操作階段


# 重設所有變數（新遊戲）
def reset():
    global money, status, rnd, stage, community, bet, hand_raw, community_raw, deck, all_in_flag, f_fold_skip
    money = [100, 100, 100, 100]
    status = [None, None, None, None]
    rnd, stage = 0, 0
    community = ""
    bet = [0, 0, 0, 0]
    hand_raw = [[], [], [], []]
    community_raw = []
    deck = []
    all_in_flag = [False, False, False, False]
    f_fold_skip = False

# 根據stage編號回傳輪次名稱
def get_stage_name(stage):
    return {
        2: "PREFLOP",
        4: "FLOP",
        6: "TURN",
        8: "RIVER",
    }.get(stage, "")

# 顯示目前牌桌狀態（文字）
def board():
    board_text = f"Round: {rnd} | Stage: {get_stage_name(stage)}\n\nCommunity: {community}\n\n"
    for i in range(4):
        board_text += f"{player_names[i]}: {status[i]} | Bet: {bet[i]} | Money: {money[i]}\n"
    board_text += f"\nHand: {' '.join(hand_raw[3])}" # 顯示真人玩家的手牌
    return board_text

# 根據分數代號回傳對應牌型名稱
def score_name(score):
    names = ["High Card", "One Pair", "Two Pairs", "Three of a Kind",
             "Straight", "Flush", "Full House", "Four of a Kind",
             "Straight Flush", "Royal Flush"]
    return names[score - 1]

# 發牌並初始化每回合狀態
def round_init():
    global deck, hand_raw, community_raw, stage, status, bet, community, all_in_flag, f_fold_skip
    deck = generate_deck()  # 產生牌組
    shuffle_deck(deck)  # 洗牌
    hand_raw = [[deck.pop(), deck.pop()] for _ in range(4)]  # 每位玩家發兩張牌
    community_raw = [deck.pop() for _ in range(5)]  # 發五張公共牌
    stage = 2  # 進入 PREFLOP
    status[:] = [None, None, None, None]
    bet[:] = [0, 0, 0, 0]
    all_in_flag[:] = [False, False, False, False]
    f_fold_skip = False
    community = ""  # 清空顯示用公共牌字串

# 使用 /start 指令開始新遊戲
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reset()
    await update.message.reply_text("遊戲開始！每位玩家有100元。輸入 /deal 開始發牌。")

# 使用 /deal 指令開始新一回合
async def deal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global rnd, stage
    if stage > 0:
        return
    round_init()
    rnd += 1
    await player_action(context, update.effective_chat.id)

# 電腦自動決策 & 玩家操作階段
async def player_action(context, chat_id):
    global stage, community, f_fold_skip

    # 根據輪次決定要翻幾張公共牌
    if stage == 4:
        community = ' '.join(community_raw[:3])
    elif stage == 6:
        community = ' '.join(community_raw[:4])
    elif stage == 8:
        community = ' '.join(community_raw[:5])

    for i in range(3):
        # 若已棄牌或 ALL IN，跳過
        if all_in_flag[i] or status[i] == "FOLD":
            continue

        # 評估該玩家的手牌（根據目前輪次合併部分公共牌）
        combined = hand_raw[i] + community_raw[:(stage-2)//2+3] if stage >= 4 else hand_raw[i]
        score = evaluate_hand(combined)
        # Computer 1: 無論如何都壓1塊
        if i == 0:
            if money[i] > 0:
                money[i] -= 1
                bet[i] += 1
                status[i] = "BET"
        # Computer 2: PREFLOP下注；Flop時如果只有High Card就棄牌，不然壓1塊；Turn和River如果拿到Full House以上就All in，不然壓1塊
        elif i == 1:
            if stage == 2:
                money[i] -= 1
                bet[i] += 1
                status[i] = "BET"
            elif stage == 4 and score[0] == 1:
                status[i] = "FOLD"
            elif stage in [6, 8] and score[0] >= 7:
                bet[i] += money[i]
                money[i] = 0
                all_in_flag[i] = True
                status[i] = "ALL IN"
            else:
                money[i] -= 1
                bet[i] += 1
                status[i] = "BET"
        # Computer 3: PREFLOP下注；FLOP時，score≤3 (只有two pairs時) 就 FOLD；否則 ALL IN
        elif i == 2:
            if stage == 2:
                money[i] -= 1
                bet[i] += 1
                status[i] = "BET"
            elif stage == 4 and score[0] <= 3:
                status[i] = "FOLD"
            else:
                bet[i] += money[i]
                money[i] = 0
                all_in_flag[i] = True
                status[i] = "ALL IN"

    # 判斷玩家是否要跳過（已 ALL IN 或 FOLD）
    if all_in_flag[3] or status[3] == "FOLD":
        f_fold_skip = True
        await context.bot.send_message(chat_id, text=board(), reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton('跳過', callback_data='skip')]]))
        return
    # 玩家操作按鈕：下注、棄牌、ALL IN
    await context.bot.send_message(chat_id, text=board(), reply_markup=InlineKeyboardMarkup([[
        InlineKeyboardButton('All in', callback_data='a'),
        InlineKeyboardButton('下注 1元', callback_data='b'),
        InlineKeyboardButton('棄牌', callback_data='f')]]))

# 玩家按下按鈕的回應處理
async def action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global bet, money, stage, status, all_in_flag, f_fold_skip
    query = update.callback_query
    await query.answer()
    user = 3 #真人玩家為第4位

    if query.data == 'a':
        bet[user] += money[user]
        money[user] = 0
        status[user] = "ALL IN"
        all_in_flag[user] = True
    elif query.data == 'b':
        money[user] -= 1
        bet[user] += 1
        status[user] = "BET"
    elif query.data == 'f':
        status[user] = "FOLD"
    elif query.data == 'skip' and f_fold_skip:
        f_fold_skip = False

    # 更新 UI 顯示
    await context.bot.edit_message_text(chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=board())

    await next_stage_or_result(context, query.message.chat_id)

# 控制輪次推進或顯示結果
async def next_stage_or_result(context, chat_id):
    global stage, rnd
    stage += 2
    if stage <= 8:
        await player_action(context, chat_id)  # 下一輪操作
    else:
        await show_result(context, chat_id)  # 顯示結果
        stage = 0  # 重置輪次

        # 檢查是否結束遊戲（有玩家沒錢或有玩家超過 250）
        if any(m <= 0 for m in money) or any(m >= 250 for m in money):
            final = "\n\n🎉 遊戲結束！最終結果：\n"
            sorted_final = sorted(zip(money, player_names), reverse=True)
            for m, name in sorted_final:
                final += f"{name}: ${m}\n"
            final += "\n請按 /start 重玩。"
            await context.bot.send_message(chat_id, text=final)

# 取得完整牌型分數
def get_hand_score(i):
    full_hand = hand_raw[i] + community_raw
    return evaluate_hand(full_hand)

# 顯示牌局結果與發獎金
async def show_result(context, chat_id):
    global money
    scores = [(get_hand_score(i), i) for i in range(4)]
    scores.sort(reverse=True) # 分數從高到低

    result = f"Round: {rnd}\nCommunity: {' '.join(community_raw)}\n\n"
    for score, i in scores:
        result += f"{player_names[i]}: {' '.join(hand_raw[i])} | [{score_name(score[0])}] | Bet: {bet[i]} | Money: {money[i]}\n"

    top_score_val = scores[0][0][0]  # 只取牌型編號
    winners = [i for score, i in scores if score[0] == top_score_val] # 找出贏家（可能多人）

    pot = sum(bet)
    for i in winners:
        money[i] += pot // len(winners) # 平分彩池

    if len(winners) == 1:
        result += f"\nPot: {pot}\n🏆 {player_names[winners[0]]} wins the pot of {pot}!"
    else:
        share = pot // len(winners)
        names = ' and '.join(player_names[i] for i in winners)
        result += f"\nPot: {pot}\n🏆 {names} each win {share}!"

    await context.bot.send_message(chat_id, text=result + "\n\n輸入 /deal 進行下一回合。")

# 主程式入口：註冊 Bot 指令與回傳
def main():
    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("deal", deal))
    application.add_handler(CallbackQueryHandler(action))
    application.run_polling()

if __name__ == "__main__":
    main()
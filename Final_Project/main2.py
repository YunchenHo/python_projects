# 引入必要模組
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from poker import generate_deck, shuffle_deck, evaluate_hand
from mytoken import token

player_names = ["Computer1", "Computer2", "Computer3", "YunChen Ho"]
money = [100, 100, 100, 100]
status = [None, None, None, None]
rnd = 0
stage = 0
community = ""
bet = [0, 0, 0, 0]
hand_raw = [[], [], [], []]
community_raw = []
deck = []
all_in_flag = [False, False, False, False]
f_fold_skip = False
last_game_message = None  # 新增訊息記錄變數

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

def get_stage_name(stage):
    return {2: "PREFLOP", 4: "FLOP", 6: "TURN", 8: "RIVER"}.get(stage, "")

def board():
    board_text = f"Round: {rnd} | Stage: {get_stage_name(stage)}\n\nCommunity: {community}\n\n"
    for i in range(4):
        board_text += f"{player_names[i]}: {status[i]} | Bet: {bet[i]} | Money: {money[i]}\n"
    board_text += f"\nHand: {' '.join(hand_raw[3])}"
    return board_text

def score_name(score):
    names = ["High Card", "One Pair", "Two Pairs", "Three of a Kind", "Straight", "Flush", "Full House", "Four of a Kind", "Straight Flush", "Royal Flush"]
    return names[score - 1]

def round_init():
    global deck, hand_raw, community_raw, stage, status, bet, community, all_in_flag, f_fold_skip
    deck = generate_deck()
    shuffle_deck(deck)
    hand_raw = [[deck.pop(), deck.pop()] for _ in range(4)]
    community_raw = [deck.pop() for _ in range(5)]
    stage = 2
    status[:] = [None, None, None, None]
    bet[:] = [0, 0, 0, 0]
    all_in_flag[:] = [False, False, False, False]
    f_fold_skip = False
    community = ""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reset()
    await update.message.reply_text("遊戲開始！每位玩家有100元。輸入 /deal 開始發牌。")

async def deal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global rnd, stage, last_game_message
    if stage > 0:
        return
    round_init()
    rnd += 1
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('All in', callback_data='a'),
         InlineKeyboardButton('下注 1元', callback_data='b'),
         InlineKeyboardButton('棄牌', callback_data='f')]
    ])
    last_game_message = await update.message.reply_text(board(), reply_markup=markup)

async def player_action(context, message):
    global stage, community, f_fold_skip
    if stage == 4:
        community = ' '.join(community_raw[:3])
    elif stage == 6:
        community = ' '.join(community_raw[:4])
    elif stage == 8:
        community = ' '.join(community_raw[:5])

    for i in range(3):
        if all_in_flag[i] or status[i] == "FOLD":
            continue
        combined = hand_raw[i] + community_raw[:(stage - 2) // 2 + 3] if stage >= 4 else hand_raw[i]
        score = evaluate_hand(combined)
        if i == 0:
            if money[i] > 0:
                money[i] -= 1
                bet[i] += 1
                status[i] = "BET"
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

    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('跳過', callback_data='skip')] if all_in_flag[3] or status[3] == "FOLD" else
        [InlineKeyboardButton('All in', callback_data='a'),
         InlineKeyboardButton('下注 1元', callback_data='b'),
         InlineKeyboardButton('棄牌', callback_data='f')]
    ])
    await message.edit_text(text=board(), reply_markup=markup)

async def action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global bet, money, stage, status, all_in_flag, f_fold_skip
    query = update.callback_query
    await query.answer()
    user = 3

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

    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('跳過', callback_data='skip')] if f_fold_skip else
        [InlineKeyboardButton('All in', callback_data='a'),
         InlineKeyboardButton('下注 1元', callback_data='b'),
         InlineKeyboardButton('棄牌', callback_data='f')]
    ])
    await query.edit_message_text(text=board(), reply_markup=markup)
    await next_stage_or_result(context)

async def next_stage_or_result(context):
    global stage, rnd, last_game_message
    stage += 2
    if stage <= 8:
        await player_action(context, last_game_message)
    else:
        await show_result(context, last_game_message)
        stage = 0
        if any(m <= 0 for m in money) or any(m >= 250 for m in money):
            final = "\n\n🎉 遊戲結束！最終結果：\n"
            sorted_final = sorted(zip(money, player_names), reverse=True)
            for m, name in sorted_final:
                final += f"{name}: ${m}\n"
            final += "\n請按 /start 重玩。"
            await last_game_message.edit_text(final)

def get_hand_score(i):
    full_hand = hand_raw[i] + community_raw
    return evaluate_hand(full_hand)

async def show_result(context, message):
    global money
    scores = [(get_hand_score(i), i) for i in range(4)]
    scores.sort(reverse=True)
    result = f"Round: {rnd}\nCommunity: {' '.join(community_raw)}\n\n"
    for score, i in scores:
        result += f"{player_names[i]}: {' '.join(hand_raw[i])} | [{score_name(score[0])}] | Bet: {bet[i]} | Money: {money[i]}\n"

    top_score_val = scores[0][0][0]
    winners = [i for score, i in scores if score[0] == top_score_val]
    pot = sum(bet)
    for i in winners:
        money[i] += pot // len(winners)

    if len(winners) == 1:
        result += f"\nPot: {pot}\n🏆 {player_names[winners[0]]} wins the pot of {pot}!"
    else:
        share = pot // len(winners)
        names = ' and '.join(player_names[i] for i in winners)
        result += f"\nPot: {pot}\n🏆 {names} each win {share}!"

    result += "\n\n輸入 /deal 進行下一回合。"
    await message.edit_text(text=result)

def main():
    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("deal", deal))
    application.add_handler(CallbackQueryHandler(action))
    application.run_polling()

if __name__ == "__main__":
    main()
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from mytoken import token

SUITS = ['♠', '♥', '♦', '♣']
RANK = list('23456789TJQKA')

money = [100, 100, 100, 100]
status = [None, None, None, None]
rnd = 0
stage = 0
community = ""
bet = [0, 0, 0, 0]
hand = ["", "", "", ""]

def reset(): # reset game
    global money, status, rnd, stage, community, bet, hand
    money = [100, 100, 100, 100]
    status = [None, None, None, None]
    rnd, stage = 0, 0
    community = ""
    bet = [0, 0, 0, 0]
    hand = ["", "", "", ""]

def board():
    return f'''Round: {rnd} | Stage: {stage}

Community: {community}

Computer 1: {status[0]} | Bet: {bet[0]} Money: {money[0]}
Computer 2: {status[1]} | Bet: {bet[1]} Money: {money[1]}
Computer 3: {status[2]} | Bet: {bet[2]} Money: {money[2]}

Hand: {hand[-1]} | Status: {status[-1]} | Bet: {bet[-1]} Money: {money[-1]}
'''

def round_init():
    pass

async def start(update, context):
    # Reset game
    reset()
    await update.message.reply_text("Game starts! Every player has $100. Send /deal to start a round.")

async def deal(update, context):
    global rnd, stage
    if stage > 0: return # Do nothing if a round has been started
    round_init()
    rnd += 1
    # 1. shuffle the deck
    # shuffle_deck()
    stage = 1
    # 2. issue cards
    # issue_cards()
    stage = 2

    await update.message.reply_text(board(), reply_markup=InlineKeyboardMarkup([[
        InlineKeyboardButton('All in', callback_data='a'),
        InlineKeyboardButton('Bet', callback_data='b'),
        InlineKeyboardButton('Fold', callback_data='f')]]))


async def action(update, context):
    global bet, money, stage
    buttons = InlineKeyboardMarkup([[
        InlineKeyboardButton('Pass', callback_data='p')]])
    if update.callback_query.data == 'a':
        bet[-1] = money[-1]
    elif update.callback_query.data == 'b':
        bet[-1] += 1
        if bet[-1] < money[-1]:
            buttons = InlineKeyboardMarkup([[
                InlineKeyboardButton('All in', callback_data='a'),
                InlineKeyboardButton('Bet', callback_data='b'),
                InlineKeyboardButton('Fold', callback_data='f')]])
    elif update.callback_query.data == 'f':
        pass
    elif update.callback_query.data == 'p':
        pass

    if stage == 2: # Preflop
        pass
    elif stage == 4: # Flop
        pass
    elif stage == 6: # Turn
        pass
    elif stage == 8: # River
        pass
    stage += 1 # Should be changed
    if stage < 10:
        await context.bot.edit_message_text(board(),
                                        reply_markup=buttons,
                                        chat_id=update.callback_query.message.chat_id,
                                        message_id=update.callback_query.message.message_id)
    else:
        await context.bot.edit_message_text("round_over. /deal to start another round.",
                                            chat_id=update.callback_query.message.chat_id,
                                            message_id=update.callback_query.message.message_id)
        stage = 0

def main():
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(token).build()

    # Start / Restart games
    application.add_handler(CommandHandler("start", start))

    # Start a round
    application.add_handler(CommandHandler("deal", deal))

    # Process the button press to advance stages
    application.add_handler(CallbackQueryHandler(action))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
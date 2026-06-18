import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

import os

TOKEN = os.getenv("TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [InlineKeyboardButton("рулетка", callback_data="spin")]
    ]
    await update.message.reply_photo(
        photo="https://chatgpt.com/backend-api/estuary/content?id=file_000000007a6c7208a2cce34601ef1ff1&ts=494932&p=fs&cid=1&sig=d7d5b8bd54c9315b10d61760eaa965114abc4e349722f21c6dc6e6e5399ed70b&v=0",
        caption="привет! добро пожаловать в spinercash_bot, давай начнем игру",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button(update: Update, context: CallbackQueryHandler):
    query = update.callback_query
    await query.answer()
    data = query.data

    try:
        await query.message.delete()
    except:
        pass
    
    if data == "spin":
        num1 = random.randint(1,9)
        num2 = random.randint(1,9)
        num3 = random.randint(1,9)

        keyboard = [
            [InlineKeyboardButton("Попробовать снова", callback_data="spin")]
        ]
        if num1 != num2 and num1 != num3 and num2 != num3:
            await query.message.reply_photo(
                photo="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS_evFF4YgfBdb2LrX4CrQxax3TxNSsvwd8CvQvHljhZw&s=10",
                caption=f"Неудача, вам выпала комбинация {num1} {num2} {num3} попробуйте снова чтобы выбить куш",
                reply_markup = InlineKeyboardMarkup(keyboard)
            )

        elif num1 == num2 and num1 != num3 or num2 == num3 and num2 != num1 or num3 == num1 and num3 != num2:
            await query.message.reply_photo(
                photo="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQXALfkocC1KZlZoeddzLlc5T6eFUBniCNV3FaxwGwpIfsp3xEUR4_Krck&s=10",
                caption=f"вам выпала комбинация {num1} {num2} {num3} вы почти у цели, попробуйте снова!",
                reply_markup = InlineKeyboardMarkup(keyboard)
            )

        elif num1 == num2 == num3:
            await query.message.reply_photo(
                photo="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSKlrnKemS8QkJB6_NwFseFnVtKPYuGlAHi_sdQASQLCbgU9kHmc2HuWLA&s=10",
                caption=f"Поздравляем! вам выпала комбинация {num1} {num2} {num3} и вы выиграли куш!",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))

    print("Бот запущен")
    app.run_polling()


if __name__ == "__main__":
    main()

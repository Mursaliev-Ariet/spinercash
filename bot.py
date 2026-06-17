import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

import os

TOKEN = os.getenv("TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [InlineKeyboardButton("рулетка", callback_data="spin")]
    ]
    await update.message.reply_text(
        "привет! давай начнем игру",
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
                photo="https://chatgpt.com/backend-api/estuary/content?id=file_00000000cda072089d150efd0a25b39a&ts=494908&p=fs&cid=1&sig=72ee3457df474ebeb2f234a913faf5a3200decac00525efc3b92c99bbc7f56e0&v=0",
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

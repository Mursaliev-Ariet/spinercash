import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

import os
TOKEN = os.getenv("TOKEN")

boosts = {
    "Карта spinercash" : {
        "name" : "spinercash card",
        "text" : "Карта spinercash позволяет получать на 10% больше токенов при куше",
        "price" : 250
    }
}
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [InlineKeyboardButton("рулетка", callback_data="spin")],
        [InlineKeyboardButton("магазин бустов", callback_data="shop")],
    ]
    await update.message.reply_photo(
        photo="AgACAgIAAxkBAAORajNyvbMvHAHLJ9ayhg4etxJjuzYAAoEbaxu7rJlJk9siUonpj9MBAAMCAAN5AAM8BA",
        caption="привет! добро пожаловать в spinercash_bot, давай начнем игру",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.edit_reply_markup(reply_markup=None)
    data = query.data
    try:
        await query.message.delete()
    except:
        pass
    if "balance" not in context.user_data:
        context.user_data["balance"] = 0
    if "boosts" not in context.user_data:
        context.user_data["boosts"] = []
    if data == "spin":
        num1 = random.randint(1,9)
        num2 = random.randint(1,9)
        num3 = random.randint(1,9)

        keyboard = [
            [InlineKeyboardButton("Попробовать снова", callback_data="spin")],
            [InlineKeyboardButton("⬅️ Назад", callback_data="start")]
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
            if "spinercash card" in context.user_data["boosts"]:
                context.user_data["balance"] += 55
            else:
                context.user_data["balance"] += 50
            await query.message.reply_photo(
                photo="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSKlrnKemS8QkJB6_NwFseFnVtKPYuGlAHi_sdQASQLCbgU9kHmc2HuWLA&s=10",
                caption=(
                    f"🎉 Поздравляем!\n"
                    f"Вам выпала комбинация {num1} {num2} {num3}\n"
                    f"Вы выиграли джекпот и получили 50 токенов!\n"
                    f"Ваш текущий баланс: {context.user_data['balance']}"
                ),
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
    elif data == "start":

        keyboard = [

            [InlineKeyboardButton("рулетка", callback_data="spin")],

            [InlineKeyboardButton("магазин бустов", callback_data="shop")]

        ]

        await query.message.reply_photo(

            photo="AgACAgIAAxkBAAORajNyvbMvHAHLJ9ayhg4etxJjuzYAAoEbaxu7rJlJk9siUonpj9MBAAMCAAN5AAM8BA",

            caption="привет! добро пожаловать в spinercash_bot, давай начнем игру",

            reply_markup=InlineKeyboardMarkup(keyboard)

        )
    elif data == "shop":
        keyboard = [
            [InlineKeyboardButton(name, callback_data=f"boost_{name}")]
            for name in boosts.keys()
        ]
        keyboard.append([InlineKeyboardButton("⬅️ Назад", callback_data="start")])

        await query.message.reply_text(
            f"Магазин бустов\n💰 Ваш баланс {context.user_data['balance']} токенов",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return
    elif data.startswith("buy_"):
        boost_name = data.split("_", 1)[1]
        boost = boosts.get(boost_name)

        if not boost:
            return

        if "boosts" not in context.user_data:
            context.user_data["boosts"] = []

        if context.user_data["balance"] >= boost["price"]:
            context.user_data["balance"] -= boost["price"]
            context.user_data["boosts"].append(boost["name"])

            await query.message.reply_text(
                f"✅ Вы купили: {boost['name']}\n"
                f"Ваш баланс: {context.user_data['balance']} токенов"
            )
        else:
            await query.message.reply_text(
                f"❌ Не хватает токенов\n"
                f"Для покупки этого буста нужно: {boost['price']} токенов"
            )
        return
    elif data.startswith("boost_"):
        boost_name = data.split("_", 1)[1]
        boost = boosts.get(boost_name)

        if not boost:
            return

        keyboard = [
            [InlineKeyboardButton("Купить", callback_data=f"buy_{boost_name}")],
            [InlineKeyboardButton("⬅️ Назад", callback_data="shop")]
        ]

        await query.message.reply_text(
            f"🛍 {boost['name']}\n"
            f"{boost['text']}\n"
            f"💰 Цена: {boost['price']}",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))

    print("Бот запущен")
    app.run_polling()
if __name__ == "__main__":
    main()

import random
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

import os
TOKEN = os.getenv("TOKEN")


REWARDS = [
    {"name": "💥 Джекпот x10", "value": 10, "chance": 5},
    {"name": "🔥 x3", "value": 3, "chance": 15},
    {"name": "✨ x2", "value": 2, "chance": 25},
    {"name": "❌ проигрыш", "value": 0, "chance": 55},
]


boosts = {
    "Карта spinercash" : {
        "name" : "spinercash card",
        "text" : "Карта spinercash позволяет получать на 10% больше токенов при куше",
        "price" : 250
    }
}


def get_reward():
    total = sum(r["chance"] for r in REWARDS)
    roll = random.randint(1, total)

    current = 0
    for r in REWARDS:
        current += r["chance"]
        if roll <= current:
            return r
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
        msg = await query.message.reply_text("🎰 Крутим барабан...")
        keyboard = [
            [InlineKeyboardButton("крутить еще", callback_data="spin")],
        ]
        keyboard.append([InlineKeyboardButton("назад", callback_data="start")])

        frames = ["🎰|", "🎰/", "🎰--", "🎰\\", "🎰|"]

        for f in frames:
            await msg.edit_text(f"Крутится... {f}")
            await asyncio.sleep(0.4)

        reward = get_reward()

        # баланс
        if "balance" not in context.user_data:
            context.user_data["balance"] = 0

        BASE_REWARD = 10

        if reward["value"] > 0:

            win = reward["value"] * BASE_REWARD

            # бонус карты
            if "spinercash card" in context.user_data.get("boosts", []):
                bonus = int(win * 0.1)
                win += bonus

            context.user_data["balance"] += win

        else:
            win = 0

        boost_text = ""

        if "spinercash card" in context.user_data.get("boosts", []):
            boost_text = "\n💳 Карта spinercash: +10%"

        await msg.edit_text(
            f"🎰 Результат: {reward['name']}\n"
            f"💰 Выигрыш: {win} токенов"
            f"{boost_text}\n"
            f"📊 Баланс: {context.user_data['balance']}",
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

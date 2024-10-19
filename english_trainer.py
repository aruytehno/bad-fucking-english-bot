import nest_asyncio
nest_asyncio.apply()

import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from telegram import InputFile
import random
from dotenv import load_dotenv
import os

load_dotenv()  # Загружаем переменные из .env файла
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Уличные фразы и оскорбления
street_phrases = {
    "greetings": [
        {"phrase": "Yo, what it do, fam?", "translation": "Йо, как дела, брат?"},
        {"phrase": "Sup, homie?", "translation": "Как жизнь, чувак?"},
        {"phrase": "What’s poppin’ dawg?", "translation": "Чё как, братан?"},
        {"phrase": "Ayy! What's good?", "translation": "Эй! Как оно?"},
        {"phrase": "Yo yo yo, how's life?", "translation": "Йо, йо, йо, как жизнь?"}
    ],
    "responses": [
        {"phrase": "Just chillin', bro.", "translation": "Просто отдыхаю, брат."},
        {"phrase": "Ain't nothin', just hangin'.", "translation": "Да ничего, просто зависаю."},
        {"phrase": "Livin’ the dream, you feel me?", "translation": "Живу по полной, понимаешь?"},
        {"phrase": "Tryna make it out here, dog.", "translation": "Просто выживаю тут, братан."},
        {"phrase": "You know how it is.", "translation": "Ты же знаешь, как оно бывает."}
    ],
    "insults": [
        {"phrase": "Yo, you trippin', fool!", "translation": "Ты чё, гонишь, дурак?"},
        {"phrase": "Man, you wildin'!", "translation": "Чувак, ты совсем рехнулся!"},
        {"phrase": "Don’t make me come over there, bro.", "translation": "Не заставляй меня приходить туда, брат."},
        {"phrase": "You ain't bout that life!", "translation": "Ты не из тех, кто живет этой жизнью!"},
        {"phrase": "Better back up, fool!", "translation": "Лучше отвали, дурак!"}
    ]
}

# Возможные приветственные входящие сообщения
greetings = ["hello", "hi", "hey", "yo", "heya", "sup", "what's up"]

# Функция для обработки команды /start с приветствием
async def start(update: Update, context: CallbackContext) -> None:
    with open("images/ah_shit_here_we_go_again.jpg", "rb") as image:
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=InputFile(image),
            caption="Ah shit, here we go again"
        )

# Функция для обработки сообщений
async def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text.strip().lower()

    # Проверяем приветствие пользователя
    if any(greet in user_message for greet in greetings):
        selected_greeting = random.choice(street_phrases["greetings"])  # Случайное приветствие
        bot_reply = f"{selected_greeting['phrase']}\n\n||Перевод: {selected_greeting['translation']}||"
        await update.message.reply_text(bot_reply, parse_mode="MarkdownV2")

    # Проверяем, если пользователь спрашивает что-то вроде "how are you?"
    elif "how are you" in user_message or "how's it going" in user_message:
        selected_response = random.choice(street_phrases["responses"])  # Случайный ответ
        bot_reply = f"{selected_response['phrase']}\n\n||Перевод: {selected_response['translation']}||"
        await update.message.reply_text(bot_reply, parse_mode="MarkdownV2")

    # Проверяем, если пользователь пытается кого-то оскорбить
    elif "stupid" in user_message or "idiot" in user_message:
        selected_insult = random.choice(street_phrases["insults"])  # Случайное оскорбление
        bot_reply = f"{selected_insult['phrase']}\n\n||Перевод: {selected_insult['translation']}||"
        await update.message.reply_text(bot_reply, parse_mode="MarkdownV2")

    else:
        # Если сообщение не распознано, бот будет отвечать случайной фразой
        selected_response = random.choice(street_phrases["responses"])  # Случайный ответ
        bot_reply = f"{selected_response['phrase']}\n\n||Перевод: {selected_response['translation']}||"
        await update.message.reply_text(bot_reply, parse_mode="MarkdownV2")

# Основной код для запуска бота
async def main() -> None:
    application = Application.builder().token(TOKEN).build()

    # Обработчик для команды /start
    application.add_handler(CommandHandler("start", start))

    # Обработчик для всех текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запуск бота
    await application.run_polling()

if __name__ == '__main__':
    asyncio.run(main())

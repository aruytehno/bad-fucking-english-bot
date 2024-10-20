import nest_asyncio
nest_asyncio.apply()

import asyncio
import os
import sys
import re  # Импортируем модуль re
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from telegram import InputFile
import random
from dotenv import load_dotenv
import os
import re

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
    ],
    "feelings": {
        "happy": [
            {"phrase": "Glad to hear that, fam!", "translation": "Рад это слышать, брат!"},
            {"phrase": "That's what's up!", "translation": "Вот это хорошо!"}
        ],
        "sad": [
            {"phrase": "Aw man, that's rough.", "translation": "Ох, чувак, это тяжело."},
            {"phrase": "Keep your head up, bro.", "translation": "Держись, брат."}
        ],
        "angry": [
            {"phrase": "I feel ya, bro. It's frustrating.", "translation": "Понимаю тебя, брат. Это бесит."},
            {"phrase": "Yeah, that can be real annoying.", "translation": "Да, это действительно может быть раздражающим."}
        ]
    }
}

# Возможные приветственные входящие сообщения
greetings = ["hello", "hi", "hey", "yo", "heya", "sup", "what's up"]
user_names = {}  # Словарь для хранения имен пользователей

# Функция для обработки команды /start с приветствием
async def start(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_chat.id
    user_name = update.effective_user.first_name  # Получаем имя пользователя
    user_names[user_id] = user_name  # Сохраняем имя пользователя

    # Отправляем изображение
    with open("images/ah_shit_here_we_go_again.jpg", "rb") as image:
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=InputFile(image),
            caption=f"Ah shit, here we go again, {user_name}!"
        )

    # Отправляем случайное приветственное сообщение
    selected_greeting = random.choice(street_phrases["greetings"])  # Случайное приветствие
    bot_reply = f"{escape_markdown(selected_greeting['phrase'])}\n\n||Перевод: {escape_markdown(selected_greeting['translation'])}||"
    await update.message.reply_text(bot_reply, parse_mode="MarkdownV2")

# Функция для обработки команды /restart
async def restart(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Перезапуск бота...")
    os.execv(sys.executable, ['python'] + sys.argv)

# Функция для экранирования символов Markdown
def escape_markdown(text: str) -> str:
    return re.sub(r'([_.*[\]()~`>#+\-=|{}.!])', r'\\\1', text)

# Функция для обработки сообщений
async def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text.strip().lower()

    # Проверяем приветствие пользователя
    if any(greet in user_message for greet in greetings):
        selected_greeting = random.choice(street_phrases["greetings"])  # Случайное приветствие
        bot_reply = f"{escape_markdown(selected_greeting['phrase'])}\n\n||Перевод: {escape_markdown(selected_greeting['translation'])}||"
        await update.message.reply_text(bot_reply, parse_mode="MarkdownV2")

    # Проверяем, если пользователь спрашивает что-то вроде "how are you?"
    elif "how are you" in user_message or "how's it going" in user_message:
        selected_response = random.choice(street_phrases["responses"])  # Случайный ответ
        bot_reply = f"{escape_markdown(selected_response['phrase'])}\n\n||Перевод: {escape_markdown(selected_response['translation'])}||"
        await update.message.reply_text(bot_reply, parse_mode="MarkdownV2")

    # Проверяем, если пользователь пытается кого-то оскорбить
    elif "stupid" in user_message or "idiot" in user_message:
        selected_insult = random.choice(street_phrases["insults"])  # Случайное оскорбление
        bot_reply = f"{escape_markdown(selected_insult['phrase'])}\n\n||Перевод: {escape_markdown(selected_insult['translation'])}||"
        await update.message.reply_text(bot_reply, parse_mode="MarkdownV2")

    else:
        # Если сообщение не распознано, бот будет отвечать случайной фразой
        selected_response = random.choice(street_phrases["responses"])  # Случайный ответ
        bot_reply = f"{escape_markdown(selected_response['phrase'])}\n\n||Перевод: {escape_markdown(selected_response['translation'])}||"
        await update.message.reply_text(bot_reply, parse_mode="MarkdownV2")

# Основной код для запуска бота
async def main() -> None:
    application = Application.builder().token(TOKEN).build()

    # Обработчик для команды /start
    application.add_handler(CommandHandler("start", start))

    # Обработчик для команды /restart
    application.add_handler(CommandHandler("restart", restart))

    # Обработчик для всех текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запуск бота
    await application.run_polling()

if __name__ == '__main__':
    asyncio.run(main())

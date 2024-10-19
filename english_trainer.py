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

# Простые ругательства с переводами
phrases_with_translations = [
    {"phrase": "You're such an idiot!", "translation": "Ты такой идиот!"},
    {"phrase": "Shut up!", "translation": "Заткнись!"},
    {"phrase": "You're annoying!", "translation": "Ты раздражаешь!"},
    {"phrase": "What a moron!", "translation": "Какой дурак!"},
    {"phrase": "Don't be stupid!", "translation": "Не будь дураком!"},
    {"phrase": "Go away!", "translation": "Убирайся!"},
    {"phrase": "That's just pathetic!", "translation": "Это просто жалко!"},
    {"phrase": "Get a life!", "translation": "Займись делом!"}
]

# Функция для обработки команды /start с отправкой изображения
async def start(update: Update, context: CallbackContext) -> None:
    # Отправляем картинку с подписью
    with open("images/ah_shit_here_we_go_again.jpg", "rb") as image:
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=InputFile(image),
            caption="Ah shit, here we go again"  # Подпись к изображению
        )

# Функция для обработки сообщений с ругательствами
async def handle_message(update: Update, context: CallbackContext) -> None:
    selected_phrase = random.choice(phrases_with_translations)  # Случайная фраза с переводом
    bot_reply = f"{selected_phrase['phrase']}\n(Перевод: {selected_phrase['translation']})"
    await update.message.reply_text(bot_reply)

# Основной код для запуска бота
async def main() -> None:
    # Создаем объект приложения
    application = Application.builder().token(TOKEN).build()

    # Обработчик для команды /start
    application.add_handler(CommandHandler("start", start))

    # Обработчик для всех текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запуск бота
    await application.run_polling()

if __name__ == '__main__':
    asyncio.run(main())

import nest_asyncio
nest_asyncio.apply()

import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import random
from dotenv import load_dotenv
import os

load_dotenv()  # Загружаем переменные из .env файла
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')


# Заготовленные фразы для ругани
phrases = [
    "Что за бред ты несёшь?",
    "Ты совсем ничего не понимаешь!",
    "Твои доводы просто смехотворны!",
    "Ты серьёзно?",
    "Это не аргумент!"
]

# Функция для обработки команды /start
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Привет! Готов поспорить?')

# Функция для обработки сообщений
async def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text  # Сообщение пользователя
    bot_reply = random.choice(phrases)  # Случайная фраза
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

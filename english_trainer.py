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

# Простые фразы с переводами
phrases_with_translations = [
    {"phrase": "You're wrong!", "translation": "Ты не прав!"},
    {"phrase": "I don't think so.", "translation": "Я так не думаю."},
    {"phrase": "That's not true!", "translation": "Это не правда!"},
    {"phrase": "I disagree.", "translation": "Я не согласен."},
    {"phrase": "Are you serious?", "translation": "Ты серьёзно?"},
    {"phrase": "No way!", "translation": "Ни за что!"},
    {"phrase": "That's ridiculous!", "translation": "Это смешно!"},
    {"phrase": "Stop it!", "translation": "Прекрати!"}
]

# Функция для обработки команды /start с отправкой изображения
async def start(update: Update, context: CallbackContext) -> None:
    # # Отправляем приветственное сообщение
    # await update.message.reply_text('Ah shit, here we go again')

    # Отправляем картинку с подписью
    with open("images/ah_shit_here_we_go_again.jpg", "rb") as image:
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=InputFile(image),
            caption="Ah shit, here we go again"  # Подпись к изображению
        )

# Функция для обработки сообщений с переводами
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

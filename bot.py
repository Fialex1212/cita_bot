import asyncio
import logging
import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
from dotenv import load_dotenv
import os

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


def add_user(telegram_id, username):
    db_path = "/app/database.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR IGNORE INTO users (telegram_id, username) VALUES (?, ?)",
        (telegram_id, username),
    )
    conn.commit()
    conn.close()


@dp.message(Command("start"))
async def start(message: Message):
    add_user(message.from_user.id, message.from_user.username)
    await message.answer(
        f"Hello, {message.from_user.first_name}! You have been added to the database."
    )


@dp.message()
async def echo(message: Message):
    await message.answer(f"You said: {message.text}")


async def main():
    logging.basicConfig(level=logging.INFO)
    print("Bot is running...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

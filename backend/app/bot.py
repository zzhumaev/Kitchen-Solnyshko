import asyncio, os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command

bot = Bot(token=os.environ["TELEGRAM_BOT_TOKEN"])
dp = Dispatcher()

@dp.message(Command("start"))
async def start(m: Message):
    await m.answer("Бот запущен на сервере! ✅")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

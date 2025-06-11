import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from bot.handlers.start import router as start_router
from config import BOT_TOKEN
from database.db import init_db

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()
dp.include_router(start_router)

async def main():
    init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from bot.handlers.start import router as start_router
from database.db import init_db
from config import BOT_TOKEN
from web.web_main import app  # У тебе FastAPI app тут

import uvicorn

async def start_fastapi():
    config = uvicorn.Config(app, host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

async def start_telegram():
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.include_router(start_router)
    await dp.start_polling(bot)

async def main():
    init_db()
    await asyncio.gather(
        start_fastapi(),
        start_telegram()
    )

if __name__ == "__main__":
    asyncio.run(main())

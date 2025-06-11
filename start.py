import threading
from main import bot, dp
from web.web_main import app
import uvicorn

def run_bot():
    from aiogram.enums import ParseMode
    from aiogram import Dispatcher
    import asyncio
    asyncio.run(dp.start_polling(bot))

if __name__ == "__main__":
    print("[INFO] Starting Telegram bot...")
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()

    print("[INFO] Starting FastAPI app...")
    uvicorn.run("web.web_main:app", host="0.0.0.0", port=8000, reload=False)

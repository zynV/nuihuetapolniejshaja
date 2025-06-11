import logging
import sys
import os

# Добавляем корневую директорию проекта в PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message

from config import BOT_TOKEN
from bot.handlers.utils import get_auth_url
from bot.handlers.start import router as start_router
from bot.handlers.admin import router as admin_router

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/bot.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Подключаем роутеры
dp.include_router(start_router)
dp.include_router(admin_router)

@dp.message(Command("help"))
async def cmd_help(message: Message):
    """Обработчик команды /help"""
    await message.answer(
        "🤖 Я бот для доступа к приватным каналам.\n\n"
        "Доступные команды:\n"
        "/start - Начать процесс авторизации\n"
        "/help - Показать это сообщение\n\n"
        "Для получения доступа к каналу вам необходимо:\n"
        "1. Иметь активную подписку на Patreon\n"
        "2. Пройти авторизацию через команду /start\n"
        "3. Использовать полученную ссылку для вступления в канал"
    )

async def main():
    """Запуск бота"""
    try:
        logger.info("Запуск бота...")
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")
        raise

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
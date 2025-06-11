import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message

from config import BOT_TOKEN
from bot.handlers.utils import get_auth_url

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

@dp.message(Command("start"))
async def cmd_start(message: Message):
    """Обработчик команды /start"""
    try:
        auth_url = get_auth_url(message.from_user.id)
        
        await message.answer(
            "👋 Привет! Я бот для доступа к приватным каналам.\n\n"
            "Для получения доступа, пожалуйста, авторизуйтесь через Patreon:\n"
            f"{auth_url}\n\n"
            "После авторизации вы получите ссылку для вступления в канал."
        )
        
        logger.info(f"Отправлена ссылка авторизации пользователю {message.from_user.id}")
        
    except Exception as e:
        logger.error(f"Ошибка при обработке команды /start: {e}")
        await message.answer(
            "😔 Произошла ошибка. Пожалуйста, попробуйте позже или обратитесь к администратору."
        )

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
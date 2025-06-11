import os
import logging
from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv()

# Настройка логирования
logging.basicConfig(
    level=logging.DEBUG,  # Можно заменить на INFO в проде
    format="%(levelname)s:%(name)s:%(message)s"
)
logger = logging.getLogger(__name__)

# Переменные окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
CLIENT_ID = os.getenv("PATREON_CLIENT_ID")
CLIENT_SECRET = os.getenv("PATREON_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

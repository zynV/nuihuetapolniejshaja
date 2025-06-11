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

# Telegram Bot
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Patreon OAuth2
PATREON_CLIENT_ID = os.getenv('PATREON_CLIENT_ID')
PATREON_CLIENT_SECRET = os.getenv('PATREON_CLIENT_SECRET')
PATREON_REDIRECT_URI = os.getenv('PATREON_REDIRECT_URI')

# Database
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///database/auth.db')

# Logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = os.getenv('LOG_FILE', 'logs/auth.log')

# Patreon Tier to Channel mapping
TIER_TO_CHANNEL = {
    'tier1': 'channel_id_1',  # Замените на реальные ID каналов
    'tier2': 'channel_id_2',
    'tier3': 'channel_id_3',
}

# Patreon API endpoints
PATREON_API_BASE = 'https://www.patreon.com/api/oauth2/v2'
PATREON_TOKEN_URL = 'https://www.patreon.com/api/oauth2/token'
PATREON_USER_URL = f'{PATREON_API_BASE}/identity'
PATREON_MEMBERSHIP_URL = f'{PATREON_API_BASE}/memberships'

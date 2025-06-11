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
    'tier1': -1002666322243,  # $3: Tier 1
    'tier2': -1002546535049,  # $4: Tier 2
    'tier3': -1002860483229,  # $5: Tier 3
}

# Patreon API endpoints
PATREON_API_BASE = 'https://www.patreon.com/api/oauth2/v2'
PATREON_TOKEN_URL = 'https://www.patreon.com/api/oauth2/token'
PATREON_USER_URL = f'{PATREON_API_BASE}/identity'
PATREON_MEMBERSHIP_URL = f'{PATREON_API_BASE}/memberships'

# Список администраторов бота (Telegram ID)
ADMIN_IDS = [
    5770917737,
    420413105,  # Ваш ID
    # Добавьте сюда другие ID администраторов
]

import logging
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from web.oauth_callback import router as oauth_router
from database.db import init_db

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/auth.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Инициализация FastAPI приложения
app = FastAPI(title="Patreon Telegram Bot Auth")

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Монтирование статических файлов
app.mount("/static", StaticFiles(directory="web/static"), name="static")

# Подключение роутеров
app.include_router(oauth_router)

@app.on_event("startup")
async def startup_event():
    """Действия при запуске приложения"""
    try:
        init_db()
        logger.info("Приложение успешно запущено")
    except Exception as e:
        logger.error(f"Ошибка при запуске приложения: {e}")
        raise

@app.get("/")
async def root():
    """Корневой эндпоинт"""
    return {"status": "ok", "message": "Patreon Telegram Bot Auth Service"}


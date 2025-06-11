import logging
import httpx
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Dict, Any

from config import (
    PATREON_CLIENT_ID,
    PATREON_CLIENT_SECRET,
    PATREON_TOKEN_URL,
    PATREON_USER_URL,
    PATREON_MEMBERSHIP_URL,
    REDIRECT_URI,
    CLIENT_ID,
    CLIENT_SECRET,
    BOT_TOKEN,
    TIER_TO_CHANNEL
)
from database.db import save_user_data, get_user_by_patreon_id
from aiogram import Bot
from bot.handlers.utils import invite_user

router = APIRouter()
templates = Jinja2Templates(directory="web/templates")
logger = logging.getLogger(__name__)

async def get_patreon_user_data(access_token: str) -> Dict[str, Any]:
    """Получение данных пользователя от Patreon API"""
    async with httpx.AsyncClient() as client:
        headers = {"Authorization": f"Bearer {access_token}"}
        
        # Получение информации о пользователе
        user_response = await client.get(
            f"{PATREON_USER_URL}?include=memberships",
            headers=headers
        )
        user_data = user_response.json()
        
        if "data" not in user_data:
            raise HTTPException(status_code=400, detail="Не удалось получить данные пользователя")
        
        return user_data

async def get_patreon_token(code: str) -> Dict[str, Any]:
    """Получение токена доступа от Patreon"""
    async with httpx.AsyncClient() as client:
        data = {
            "code": code,
            "grant_type": "authorization_code",
            "client_id": PATREON_CLIENT_ID,
            "client_secret": PATREON_CLIENT_SECRET,
            "redirect_uri": REDIRECT_URI
        }
        
        response = await client.post(PATREON_TOKEN_URL, data=data)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Ошибка получения токена")
        
        return response.json()

@router.get("/callback", response_class=HTMLResponse)
async def oauth_callback(request: Request, code: str, state: str):
    """Обработка callback от Patreon OAuth"""
    try:
        # Получение токена
        token_data = await get_patreon_token(code)
        access_token = token_data["access_token"]
        
        # Получение данных пользователя
        user_data = await get_patreon_user_data(access_token)
        
        # Извлечение необходимой информации
        patreon_id = user_data["data"]["id"]
        email = user_data["data"]["attributes"].get("email")
        
        # Определение уровня подписки
        tier = None
        if "included" in user_data:
            for item in user_data["included"]:
                if item["type"] == "member":
                    tier = item["attributes"].get("patron_status")
                    break
        
        # Сохранение данных пользователя
        user_info = {
            "patreon_id": patreon_id,
            "telegram_id": int(state),  # state содержит telegram_id
            "email": email,
            "access_token": access_token,
            "tier": tier
        }
        
        save_user_data(user_info)
        
        # Логируем tier и карту каналов
        logger.info(f"tier from Patreon: {tier}")
        logger.info(f"TIER_TO_CHANNEL: {TIER_TO_CHANNEL}")
        
        # Отправляем инвайт в Telegram
        try:
            bot = Bot(token=BOT_TOKEN)
            invite_result = await invite_user(bot, int(state), tier)
            logger.info(f"invite_user result: {invite_result}")
        except Exception as e:
            logger.error(f"Ошибка при вызове invite_user: {e}")
        
        # Отображение страницы успешной авторизации
        return templates.TemplateResponse(
            "accept.html",
            {"request": request}
        )
        
    except Exception as e:
        logger.error(f"Ошибка при обработке OAuth callback: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

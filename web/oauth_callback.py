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
async def oauth_callback(request: Request, code: str, state: str = None):
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            token_resp = await client.post(
                "https://www.patreon.com/api/oauth2/token",
                data={
                    "code": code,
                    "grant_type": "authorization_code",
                    "client_id": CLIENT_ID,
                    "client_secret": CLIENT_SECRET,
                    "redirect_uri": REDIRECT_URI,
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )
            logger.warning(f"Patreon token status: {token_resp.status_code}")
            logger.warning(f"Patreon token raw: {token_resp.text}")
            token_data = token_resp.json()
            access_token = token_data.get("access_token")
    except httpx.RequestError as e:
        logger.error(f"Patreon token exchange failed: {e}")
        raise HTTPException(status_code=400, detail="Patreon request failed or timed out")

    if not access_token:
        raise HTTPException(status_code=400, detail="Access token not received")

    try:
        async with httpx.AsyncClient() as client:
            user_resp = await client.get(
                "https://www.patreon.com/api/oauth2/v2/identity?include=memberships&fields[user]=email&fields[member]=patron_status",
                headers={"Authorization": f"Bearer {access_token}"}
            )
            user_data = user_resp.json()
            logger.warning(f"Full user_data dump: {user_data}")

            if "data" not in user_data:
                logger.warning(f"Patreon API unexpected response: {user_data}")
                raise HTTPException(status_code=400, detail="Invalid response from Patreon")

    except Exception as e:
        logger.error(f"Patreon user info failed: {e}")
        raise HTTPException(status_code=400, detail="User info request failed")

    patreon_id = user_data["data"]["id"]
    email = user_data["data"]["attributes"].get("email", "unknown")
    memberships = user_data.get("included", [])

    tier = "none"
    for member in memberships:
        if member["type"] == "member":
            status = member["attributes"].get("patron_status")
            if status == "active_patron":
                tier = "tier1"  # Привязываем к ключу в TIER_TO_CHANNEL
                break

    if tier == "none":
        return templates.TemplateResponse(
            "accept.html",
            {"request": request, "error": "У пользователя нет активной подписки на Patreon"}
        )

    telegram_id = state

    # Сохраняем пользователя в базу
    user_info = {
        "patreon_id": patreon_id,
        "telegram_id": int(telegram_id),
        "email": email,
        "access_token": access_token,
        "tier": tier
    }
    save_user_data(user_info)

    try:
        bot = Bot(token=BOT_TOKEN)
        await invite_user(bot, int(telegram_id), tier)
        logger.info(f"Invite sent to telegram_id={telegram_id}, tier={tier}")
    except Exception as e:
        logger.warning(f"Invite error: {e}")

    return templates.TemplateResponse(
        "accept.html",
        {"request": request}
    )

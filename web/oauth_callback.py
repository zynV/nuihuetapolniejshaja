from fastapi import APIRouter, Request
from config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, logger, BOT_TOKEN
import httpx
from aiogram import Bot
from bot.handlers.utils import invite_user

router = APIRouter()

@router.get("/callback")
async def patreon_callback(request: Request, code: str, state: str = None):
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
            logger.warning(f"Patreon token_data: {token_data}")
            access_token = token_data.get("access_token")
    except httpx.RequestError as e:
        logger.error(f"Patreon token exchange failed: {e}")
        return {"error": "Patreon request failed or timed out"}

    if not access_token:
        return {"error": "Access token not received"}

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
                return {"error": "Invalid response from Patreon"}

    except Exception as e:
        logger.error(f"Patreon user info failed: {e}")
        return {"error": "User info request failed"}

    patreon_id = user_data["data"]["id"]
    email = user_data["data"]["attributes"].get("email", "unknown")
    memberships = user_data.get("included", [])

    tier = "none"
    for member in memberships:
        if member["type"] == "member":
            status = member["attributes"].get("patron_status")
            if status == "active_patron":
                tier = "1"
                break

    if tier == "none":
        return {"error": "У пользователя нет активной подписки на Patreon"}

    telegram_id = state

    try:
        bot = Bot(token=BOT_TOKEN)
        await invite_user(bot, int(telegram_id), tier)
        logger.info(f"Invite sent to telegram_id={telegram_id}, tier={tier}")
    except Exception as e:
        logger.warning(f"Invite error: {e}")

    return {"patreon_id": patreon_id, "tier": tier}

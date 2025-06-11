from aiogram import Bot
import logging
import asyncio

tier_channel_map = {
    "1": -1002666322243,
    "2": "@channel_y",
    "3": "@channel_z"
}

async def invite_user(bot: Bot, telegram_id: int, tier: str):
    try:
        channel = tier_channel_map.get(tier)
        if not channel:
            logging.warning(f"Wrong tier...:/ {tier}")
            return False

        # Генерация одноразовой ссылки
        invite_link = await bot.create_chat_invite_link(
            chat_id=channel,
            member_limit=1,
            creates_join_request=False
        )

        # Отправка ссылки пользователю
        await bot.send_message(
            chat_id=telegram_id,
            text=f"Your channel access link is ready — just for you: {invite_link.invite_link}"
        )

        logging.info(f"Выдана ссылка {invite_link.invite_link} для {telegram_id} в канал {channel}")
        return True

    except Exception as e:
        logging.exception(f"Link error: {e}")
        return False

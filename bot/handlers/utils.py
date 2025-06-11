import logging
from aiogram import Bot
from aiogram.types import ChatInviteLink
from config import TIER_TO_CHANNEL, PATREON_CLIENT_ID, PATREON_REDIRECT_URI

logger = logging.getLogger(__name__)

async def invite_user(bot: Bot, telegram_id: int, tier: str) -> bool:
    """
    Отправка приглашения пользователю в соответствующий канал
    
    Args:
        bot: Экземпляр бота
        telegram_id: ID пользователя в Telegram
        tier: Уровень подписки на Patreon
    
    Returns:
        bool: True если приглашение успешно отправлено, False в противном случае
    """
    try:
        # Получение ID канала для соответствующего уровня подписки
        channel_id = TIER_TO_CHANNEL.get(tier)
        if not channel_id:
            logger.error(f"Не найден канал для уровня подписки {tier}")
            return False
        
        # Создание одноразовой ссылки-приглашения
        invite_link: ChatInviteLink = await bot.create_chat_invite_link(
            chat_id=channel_id,
            member_limit=1,
            creates_join_request=False
        )
        
        # Отправка сообщения пользователю
        await bot.send_message(
            chat_id=telegram_id,
            text=f"Спасибо за поддержку! Вот ваша персональная ссылка для вступления в канал: {invite_link.invite_link}\n\n"
                 f"Ссылка одноразовая, поэтому используйте её сразу."
        )
        
        logger.info(f"Приглашение успешно отправлено пользователю {telegram_id} для канала {channel_id}")
        return True
        
    except Exception as e:
        logger.error(f"Ошибка при отправке приглашения пользователю {telegram_id}: {e}")
        return False

def get_auth_url(telegram_id: int) -> str:
    """
    Генерация URL для авторизации через Patreon
    
    Args:
        telegram_id: ID пользователя в Telegram
    
    Returns:
        str: URL для авторизации
    """
    scopes = [
        "identity",
        "identity.memberships",
        "identity[email]"
    ]
    
    return (
        f"https://www.patreon.com/oauth2/authorize"
        f"?response_type=code"
        f"&client_id={PATREON_CLIENT_ID}"
        f"&redirect_uri={PATREON_REDIRECT_URI}"
        f"&scope={' '.join(scopes)}"
        f"&state={telegram_id}"
    )

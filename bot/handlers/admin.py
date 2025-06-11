import os
import sys
import logging
from pathlib import Path

# Добавляем корневую директорию проекта в PYTHONPATH
project_root = str(Path(__file__).parent.parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

from aiogram import Router, types
from aiogram.filters import Command
from config import TIER_TO_CHANNEL, BOT_TOKEN, ADMIN_IDS
from aiogram import Bot

router = Router()
logger = logging.getLogger(__name__)

@router.message(Command("check_bot"))
async def check_bot_rights(message: types.Message):
    """
    Проверка прав бота в каналах
    Доступно только администраторам
    """
    # Проверяем, является ли пользователь администратором
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("Эта команда доступна только администраторам.")
        return

    bot = Bot(token=BOT_TOKEN)
    results = []

    try:
        # Получаем информацию о боте
        bot_info = await bot.get_me()
        results.append(f"🤖 Информация о боте:\nID: {bot_info.id}\nUsername: @{bot_info.username}")

        # Проверяем каждый канал
        for tier, channel_id in TIER_TO_CHANNEL.items():
            try:
                # Получаем информацию о канале
                chat = await bot.get_chat(channel_id)
                results.append(f"\n📢 Канал {tier}:\nID: {chat.id}\nTitle: {chat.title}")

                # Проверяем права бота
                bot_member = await bot.get_chat_member(channel_id, bot_info.id)
                results.append(f"Права бота: {bot_member.status}")

                # Пробуем создать тестовую ссылку
                try:
                    invite_link = await bot.create_chat_invite_link(
                        chat_id=channel_id,
                        member_limit=1,
                        creates_join_request=False
                    )
                    results.append(f"✅ Создание ссылок: Доступно\nПример: {invite_link.invite_link}")
                except Exception as e:
                    results.append(f"❌ Создание ссылок: Недоступно\nОшибка: {str(e)}")

            except Exception as e:
                results.append(f"\n❌ Ошибка при проверке канала {tier}:\n{str(e)}")

    except Exception as e:
        results.append(f"\n❌ Общая ошибка:\n{str(e)}")
    finally:
        await bot.session.close()

    # Отправляем результаты
    await message.answer("\n".join(results))

# Для тестирования
if __name__ == "__main__":
    print("Этот файл не предназначен для прямого запуска.")
    print("Используйте bot_main.py для запуска бота.") 
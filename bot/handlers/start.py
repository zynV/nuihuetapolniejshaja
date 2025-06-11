from aiogram import Router, types
from aiogram.filters import Command
from config import REDIRECT_URI, CLIENT_ID

router = Router()

@router.message(Command("start"))
async def start_command(message: types.Message):
    telegram_id = message.from_user.id
    auth_url = (
        f"https://www.patreon.com/oauth2/authorize?"
        f"response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}" 
        f"&scope=identity%20identity.memberships&state={telegram_id}"
    )

    await message.answer(
        f"Hi, {message.from_user.full_name}!\n"
        f"Your place is ready — just log in with Patreon and come closer:\n"
        f"<a href='{auth_url}'>A little sign-in moment...</a>",
        disable_web_page_preview=True
    )

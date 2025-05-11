from aiogram import Router, types
from aiogram.filters import Command
from auction import config

router = Router()

def is_admin(message: types.Message) -> bool:
    return message.from_user.id == config.ADMIN_ID

@router.message(Command("admin"))
async def cmd_admin(message: types.Message):
    if not is_admin(message):
        return
    await message.answer("✅ Привет, админ! Здесь будет твоя панель управления.")

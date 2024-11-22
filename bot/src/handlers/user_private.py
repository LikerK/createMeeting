from aiogram import F, types, Router
from aiogram.filters import CommandStart, Command, or_f
from bot.src.filters.chat_types import IsUser


user_private_router = Router()
user_private_router.message.filter(IsUser())

@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer(f"""Привет! Для того, чтобы создать
конференцию просто нажми на кнопку.""")






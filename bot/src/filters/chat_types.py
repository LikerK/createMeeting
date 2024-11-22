from aiogram.filters import Filter
from aiogram import Bot, types

class IsAdmin(Filter):
    def __init__(self) -> None:
        pass

    async def __call__(self, message, bot) -> bool:
        return message.from_user.id in bot.my_admins_list


class IsUser(Filter):
    def __init__(self) -> None:
        pass

    async def __call__(self, message, bot):
        for user in bot.my_users_list:
           if user.id == message.from_user.id:
               return True
        return False


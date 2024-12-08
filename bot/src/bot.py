import os
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from bot.src.middlewares.db import DataBaseSession
from bot.src.database.engine import create_db, session_maker
from bot.src.database.orm_query import orm_get_users
from bot.src.handlers.user_private import user_private_router
from bot.src.handlers.admin_private import admin_router
from dotenv import load_dotenv, find_dotenv
# from bot.src.meeting import create_meeting, get_last_meeting, delete_meeting
# from bot.src.keyboards import create_btn, del_keyboard, delete_btn

load_dotenv(find_dotenv())

TOKEN = os.getenv('TOKEN')
ALLOWED_UPDATES = ['message, edited_message']

dp = Dispatcher()
dp.include_router(user_private_router)
dp.include_router(admin_router)


async def on_startup(bot):
    await create_db()


async def on_shutdown(bot):
    print('бот лег')


async def start():
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    baseSession = DataBaseSession(session_pool=session_maker)
    dp.update.middleware(baseSession)
    session = baseSession.session_pool()
    bot.my_admins_list = []
    bot.cached_token = None
    bot.token_expiration = None
    bot.my_users_list = await orm_get_users(session)
    # bot.my_users_list = []
    rootId = 399289201
    for user in bot.my_users_list:
        if user.isAdmin:
            bot.my_admins_list.append(user.id)

    if rootId not in bot.my_admins_list:
        bot.my_admins_list.append(rootId)
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)

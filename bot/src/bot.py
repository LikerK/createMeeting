import datetime
import os
from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

from dotenv import load_dotenv, find_dotenv
# from bot.src.meeting import create_meeting, get_last_meeting, delete_meeting
# from bot.src.keyboards import create_btn, del_keyboard, delete_btn

load_dotenv(find_dotenv())
from bot.src.middlewares.db import DataBaseSession
from bot.src.database.engine import create_db, drop_db, session_maker
from bot.src.database.orm_query import orm_get_users
from bot.src.handlers.user_private import user_private_router
from bot.src.handlers.admin_private import admin_router
TOKEN = os.getenv('TOKEN')
ALLOWED_UPDATES = ['message, edited_message']

dp = Dispatcher()
dp.include_router(user_private_router)
dp.include_router(admin_router)


# @dp.message(F.text.lower() == 'создать конференцию')
# async def get_meeting(message: Message):
#     print(message.from_user)
#     try:
#         # Send a copy of the received message
#         offset = datetime.timezone(datetime.timedelta(hours=4))
#         today = datetime.datetime.now(offset)
#         date = today.today().isoformat()
#         time = today.strftime("%H:%M")
#         meeting = get_last_meeting()
#         if not meeting:
#             meeting = create_meeting('New', '60', date, time)
#         else:
#             await message.answer('''Конференция уже была создана до
# этого, осторожнее!''')
#         id = str(meeting['id'])
#         id = f'{id[0:3]} {id[3:7]} {id[7:13]}'
#         await message.answer(f'{id}\n{meeting['password']}')
#         await message.answer(meeting['meeting_url'], reply_markup=del_keyboard)
#         await message.answer('''**Не забудьте удалить конференцию после
# того, как используете ее**''', reply_markup=delete_btn)

#     except TypeError as error:
#         # But not all the types is supported to be copied so need to handle it
#         await message.answer(f'{error} {error.args}')


# @dp.message(F.text.lower() == 'удалить конференцию')
# async def del_meeting(message: Message):
#     meeting = get_last_meeting()
#     if not meeting:
#         await message.answer('За вас кто-то уже удалил конференцию :C',
#                              reply_markup=del_keyboard)
#     else:
#         delete_meeting(meeting['id'])
#         await message.answer('Конференция успешно удалена',
#                              reply_markup=del_keyboard)
#     await message.answer('Теперь ты снова можешь создать конфу',
#                          reply_markup=create_btn)
async def on_startup(bot):

    run_param = False
    if run_param:
        await drop_db()
    await create_db()


async def on_shutdown(bot):
    print('бот лег')

async def start():
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    baseSession = DataBaseSession(session_pool=session_maker)
    session = baseSession.session_pool()
    dp.update.middleware(baseSession)
    bot.my_admins_list = []
    bot.my_users_list = await orm_get_users(session)
    rootId = 399289201
    for user in bot.my_users_list:
        if user.isAdmin:
            bot.my_admins_list.append(user.id)

    # if not rootId in bot.my_admins_list:
    #     bot.my_admins_list.append(rootId)
    print(bot.my_users_list)
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)
    

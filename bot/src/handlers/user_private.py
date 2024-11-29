from aiogram import F, types, Router
from aiogram.filters import CommandStart, Command, or_f
from bot.src.filters.chat_types import IsUser
import datetime
from bot.src.keyboards import get_keyboard
from bot.src.meeting import get_last_meeting, create_meeting, get_data_meeting

USER_KEYBOARD = get_keyboard('Создать конференцию')
MEETINGS = []

user_private_router = Router()
user_private_router.message.filter(IsUser())

@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer("Привет! Тебе выдали доступ для создания конференции.")
    await message.answer("Привет! Чтобы создать конференцию, просто нажми на кнопку.", reply_markup=USER_KEYBOARD)


@user_private_router.message(F.text.lower() == 'создать конференцию')
async def get_meeting(message):
    print(message.from_user)
    try:
        # Send a copy of the received message
        offset = datetime.timezone(datetime.timedelta(hours=3))
        today = datetime.datetime.now(offset)
        date = today.today()
        time = today.strftime("%H:%M")

        if not MEETINGS:
            meeting = create_meeting('New', '30', date.isoformat(), time)
            MEETINGS.append({'meeting' : meeting['id'], 'created': message.from_user.first_name})
        else:
            last_id = MEETINGS[-1]['meeting']
            data = get_data_meeting(last_id)
            if data['status'] == 'started':
                await message.answer(f'Конференция на данный момент уже используется { MEETINGS[-1]['created'] }')
            
            date_meeting = data['created_at']
            date_obj = datetime.datetime.strptime(date_meeting, "%Y-%m-%dT%H:%M:%SZ")
            print(data)
            print(date)
            print(date_obj)
            print(date - date_obj)
            difference = date - date_obj
            seconds = difference.seconds
            if seconds >= 18000:
                meeting = create_meeting('New', '30', date.isoformat(), time)
                MEETINGS.append({'meeting' : meeting['id'], 'created': message.from_user.first_name})
                MEETINGS.pop(0)
            else:
                await message.answer(f'Конференция на данный момент уже используется { MEETINGS[-1]['created'] }')
                
         
#         if not meeting:
#             meeting = create_meeting('New', '60', date, time)
#         else:
#             await message.answer('''Конференция уже была создана до
# этого, осторожнее!''')
        
        # id = str(meeting['id'])
        # id = f'{id[0:3]} {id[3:7]} {id[7:13]}'
        # await message.answer(f'{id}\n{meeting['password']}')
        # await message.answer(meeting['meeting_url'], reply_markup=USER_KEYBOARD)

    except TypeError as error:
        # But not all the types is supported to be copied so need to handle it
        print(error)
        await message.answer(f'{error} {error.args}')

 









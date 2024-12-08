from aiogram import F, types, Router
from aiogram.filters import CommandStart
from bot.src.filters.chat_types import IsUser
import datetime
from bot.src.keyboards import get_keyboard
from bot.src.utils.zoom_token import get_token
from bot.src.meeting import create_meeting, get_data_meeting

USER_KEYBOARD = get_keyboard('Создать конференцию')
MEETINGS = []
messages = {}
user_private_router = Router()
user_private_router.message.filter(IsUser())

async def del_messages(bot, chat_id):
    # if len(messages[chat_id]['user_messages']) != 0:
    #     await bot.delete_messages(chat_id, messages[chat_id]['user_messages'])
    if len(messages) > 0:
        for answer in messages[chat_id]['bot_answers']:
            await answer.delete()
        messages[chat_id] = {'user_messages': [], 'bot_answers': []}

@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer("Привет! Тебе выдали доступ для создания конференции.")
    await message.answer("Чтобы создать конференцию, просто нажми на кнопку.", reply_markup=USER_KEYBOARD)


@user_private_router.message(F.text.lower() == 'создать конференцию')
async def get_meeting(message, bot):
    token = get_token(bot)
    header = token['header_config']
    await del_messages(bot, message.chat.id)
    try:
        offset = datetime.timezone(datetime.timedelta(hours=3))
        today = datetime.datetime.now(offset)
        date = today.today()
        time = today.strftime("%H:%M")
        if not message.chat.id in messages:
            messages[message.chat.id] = {'user_messages': [], 'bot_answers': []}
        
        if len(MEETINGS) == 0:
            meeting = create_meeting('New', '30', date.isoformat(), time, header)
            MEETINGS.append({'meeting' : meeting['id'], 'created': message.from_user.first_name})
        else:
            last_id = MEETINGS[-1]['meeting']
            meeting = get_data_meeting(last_id, header)
            if meeting['status'] == 'started':
                warning = await message.answer(f'Конференция на данный момент уже используется { MEETINGS[-1]['created'] }')
                messages[message.chat.id]['bot_answers'].append(warning)

            else:
                date_meeting = meeting['created_at']
                date_obj = datetime.datetime.strptime(date_meeting, "%Y-%m-%dT%H:%M:%SZ")
                difference = date - date_obj
                seconds = difference.seconds
                if seconds >= 15000:
                    meeting = create_meeting('New', '30', date.isoformat(), time, header)
                    MEETINGS.append({'meeting' : meeting['id'], 'created': message.from_user.first_name})
                    if len(MEETINGS) >= 5:
                        MEETINGS.pop(0)
                else:
                    warning = await message.answer(f'Конференция недавно создавалась { MEETINGS[-1]['created'] }')
                    messages[message.chat.id]['bot_answers'].append(warning)

        id = str(meeting['id'])
        id = f'{id[0:3]} {id[3:7]} {id[7:13]}'
        numbers = await message.answer(f'{id}\n{meeting['password']}')
        link = await message.answer(meeting['join_url'])
        await bot.delete_message(message.chat.id, message.message_id)
        messages[message.chat.id]['bot_answers'].append(numbers)
        messages[message.chat.id]['bot_answers'].append(link)
        # messages[message.chat.id]['user_messages'].append(message.message_id)
    except TypeError as error:
        await message.answer(f'{error} {error.args}')

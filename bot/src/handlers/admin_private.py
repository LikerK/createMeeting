from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.state import State, StatesGroup

from bot.src.filters.chat_types import IsAdmin
from bot.src.keyboards import get_keyboard
from bot.src.database.orm_query import orm_add_user, orm_delete_user, orm_update_user


admin_router = Router()
admin_router.message.filter(IsAdmin())

ADMIN_KB = get_keyboard(
    'Дать админку',
    'Добавить пользователя',
    'Удалить пользователя',
    'Список пользователей',
    sizes=(2, 2)
)

class AddUser(StatesGroup):
    id = State()
    name = State()

    texts = {
        'AddUser:id': 'Введите id пользователя:',
        'AddUser:name': 'Введите имя пользователя',
    }

class DelUser(StatesGroup):
    id = State()

class AddAdmin(StatesGroup):
    id = State()

def getCurrentUser(users, id):
    for user in users:
        print(type(user.id), type(id))
        if user.id == id:
            return user
    return False

@admin_router.message(Command('admin'))
async def get_admins(message):
    await message.answer("Что хотите сделать?", reply_markup=ADMIN_KB)


@admin_router.message(StateFilter(None), F.text == "Добавить пользователя")
async def add_id(message, state):
    await message.answer(
        "Введите id пользователя:", reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(AddUser.id)

@admin_router.message(StateFilter('*'), Command("отмена"))
@admin_router.message(StateFilter('*'), F.text.casefold() == "отмена")
async def cancel_handler(message, state) -> None:

    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer("Действия отменены", reply_markup=ADMIN_KB)

@admin_router.message(AddUser.id, F.text)
async def add_name(message, state):
    if len(message.text) >= 100:
        await message.answer("Id не должно превышать 100 символов. \n Введите заново")
        return
    # add user in database
    await state.update_data(id=int(message.text))
    await message.answer("Введите имя пользователя")
    await state.set_state(AddUser.name)


@admin_router.message(AddUser.name, F.text)
async def create_user(message, state, bot, session):
    await state.update_data(name=message.text)
    data = await state.get_data()
    data['isAdmin'] = False
    user = await orm_add_user(session, data)
    bot.my_users_list.append(user)
    await message.answer('Пользователь успешно добавлен', reply_markup=ADMIN_KB)
    await state.clear()
 
@admin_router.message(StateFilter(None), F.text == "Список пользователей")
async def get_user_list(message, session, bot):
    await message.answer("Вот список пользователей:")
    users = bot.my_users_list
    print(bot.my_users_list)
    for user in users:
        await message.answer(f'{user.name} | Id: {user.id} | Admin: {user.isAdmin}')

@admin_router.message(StateFilter(None), F.text == "Удалить пользователя")
async def get_id_user(message, state):
    await message.answer("Введите id пользователя:")
    await state.set_state(DelUser.id)

@admin_router.message(DelUser.id, F.text)
async def del_user(message, state, bot, session):
    users = bot.my_users_list
    print(bot.my_users_list)
    try:
        del_user_obj = next(filter(lambda user: user.id == int(message.text), users), False)
        if del_user_obj:
            await orm_delete_user(session, del_user_obj.id)
            bot.my_users_list.remove(del_user_obj)
            await message.answer('Пользователь успешно удален', reply_markup=ADMIN_KB)
        else:
            await message.answer('id пользователя не найден', reply_markup=ADMIN_KB)
        await state.clear()
    except:
        await message.answer('Введите id в формате числа!')
        

@admin_router.message(StateFilter(None), F.text == "Дать админку")
async def get_id_user_for_admin(message, state):
    await message.answer("Введите id пользователя:")
    await state.set_state(AddAdmin.id)

@admin_router.message(AddAdmin.id, F.text)
async def add_admin(message, state, bot, session):
    users = bot.my_users_list
    try:
        current_user = getCurrentUser(users, int(message.text))
        if current_user:
            current_user.isAdmin = True
            await orm_update_user(session, current_user.id, current_user)
            index = bot.my_users_list.index(current_user)
            print(index)
            bot.my_users_list[index].isAdmin = True
            await message.answer('Админка выдана!', reply_markup=ADMIN_KB)
        else:
            await message.answer('id пользователя не найден', reply_markup=ADMIN_KB)
        await state.clear()
    except:
        await message.answer('Введите id в формате числа!')
    
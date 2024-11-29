from aiogram.types import (
    KeyboardButton,
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def get_keyboard(*btns, sizes=[1]):
    keyboard = ReplyKeyboardBuilder()
    for btn in btns:
        keyboard.add(KeyboardButton(text=btn))
    return keyboard.adjust(*sizes).as_markup(
            resize_keyboard=True)

# create_btn = ReplyKeyboardMarkup(
#     keyboard=[
#         [KeyboardButton(text='Создать конференцию')]
#     ],
#     resize_keyboard=True
# )

# delete_btn = ReplyKeyboardMarkup(
#     keyboard=[
#        [KeyboardButton(text='Удалить конференцию')]
#     ],
#     resize_keyboard=True
# )

# del_keyboard = ReplyKeyboardRemove()

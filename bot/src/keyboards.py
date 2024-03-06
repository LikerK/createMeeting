from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove
)

create_btn = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Создать конференцию')]
    ],
    resize_keyboard=True
)

delete_btn = ReplyKeyboardMarkup(
    keyboard=[
       [KeyboardButton(text='Удалить конференцию')]
    ],
    resize_keyboard=True
)

del_keyboard = ReplyKeyboardRemove()

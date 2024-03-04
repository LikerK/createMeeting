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
    ]
)

del_keyboard = ReplyKeyboardRemove()

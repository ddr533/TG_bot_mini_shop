from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def create_replay_keyboard(row_width: int, *args):
    kb_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
    buttons: list[KeyboardButton] = \
        [KeyboardButton(text=text) for text in args]
    kb_builder.row(*buttons, width=row_width)
    return kb_builder.as_markup(resize_keyboard=True)

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def create_replay_keyboard(row_width: int, *args):
    keyboard = ReplyKeyboardMarkup(row_width = row_width, resize_keyboard=True, one_time_keyboard=True)
    for b in args:
        keyboard.add(b)
    return keyboard

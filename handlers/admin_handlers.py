from aiogram.types import Message, CallbackQuery
from aiogram import Dispatcher
from aiogram.types import ReplyKeyboardRemove
from keyboards.inline_user_keyboards import create_inline_kb
from keyboards.replaykeyboard import create_replay_keyboard


def process_admin_handlers(dp: Dispatcher, orders_dict: dict, admins_id: list):
    @dp.message_handler(commands=['admin'])
    async def process_start_command(message: Message):
        if message.from_user.id in admins_id:
            if orders_dict.keys():
                text = ''
                n = 1
                for key in orders_dict.keys():
                    text = text + f'{n}. \n' + key + '\n'
                    for val in orders_dict[key]:
                        text = text + val + ':    ' + orders_dict[key][val] + '\n'
                    text = text + '\n'
                    n += 1
            else:
                text = 'Заказов нет'
        else:
            text = 'Это команда только для админа'
        await message.answer(text=text)
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import Router


def process_admin_router(router: Router, orders_dict: dict):
    @router.message(Command(commands='admin'))
    async def process_admin_command(message: Message):
        if orders_dict.keys():
            text = ''
            num_order = 1
            for key in orders_dict.keys():
                text = text + f'{num_order}. \n' + key + '\n'
                for val in orders_dict[key]:
                    text = text + val + ':    ' + orders_dict[key][val] + '\n'
                text = text + '\n'
                num_order += 1
        else:
            text = 'Заказов нет'
        await message.answer(text=text)

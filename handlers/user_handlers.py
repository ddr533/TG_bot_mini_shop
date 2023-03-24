from aiogram.filters import CommandStart, Command, Text
from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
from aiogram.types import ReplyKeyboardRemove
from lexicon.lexicon import product_buttons, commands_text, bot_message
from keyboards.inline_user_keyboards import create_inline_kb
from keyboards.replaykeyboard import create_replay_keyboard


def process_users_router(router: Router, user_dict: dict, orders_dict: dict):
    @router.message(CommandStart())
    async def process_start_command(message: Message):
        user_id = message.from_user.id
        if user_id not in user_dict:
            user_dict.setdefault(user_id, {'Наименование': None,
                                           'Количество': 0,
                                           'Телефон': None,
                                           'Адрес': None})
        keyboard = create_inline_kb(1, **product_buttons)
        await message.answer(text=commands_text['/start'],
                             reply_markup=keyboard)

    @router.message(Command(commands='help'))
    async def process_help_command(message: Message):
        keyboard = create_inline_kb(1, *product_buttons.keys())
        await message.answer(text=commands_text['/help'],
                             reply_markup=keyboard)

    @router.message(Command(commands='cancel'))
    async def process_cancel_command(message: Message):
        await message.answer(text=commands_text['/cancel'],
                             reply_markup=ReplyKeyboardRemove())

    @router.callback_query(Text(text=[*product_buttons.keys()]))
    async def push_product_button(callback: CallbackQuery):
        user_dict[callback.from_user.id]['Наименование']\
                = product_buttons[callback.data]
        await callback.message.edit_text(
            text=f'Вы выбрали {product_buttons[callback.data]}\n'
                 f'Введите количество одним числом до 10 кг.')
        await callback.answer()

    @router.message(lambda x: x.text.isdigit() and 0 < int(x.text) <= 10)
    async def get_amount(message: Message):
        user_dict[message.from_user.id]['Количество'] = message.text
        await message.answer(
            text=f'<b>Количество</b>: {message.text.lstrip("0")} шт.\n'
                 f'Напишите номер телефона для связи или\n'
                 f'/cancel для отмены')


    @router.message(F.text.regexp(r'^8\d{10}$'))
    async def get_phone(message: Message):
        user_dict[message.from_user.id]['Телефон'] = message.text
        await message.answer(
            text=f'<b>Телефон</b>: {message.text}\n'
                 f'Укажите адрес для доставки,'
                 f'улица/дом или /cancel для отмены')


    @router.message(F.text.regexp(r'(\w\D+)\s*\d+.*'))
    async def get_address(message: Message):
        user_dict[message.from_user.id]['Адрес'] = message.text[:50]
        order = f"Вид: {user_dict[message.from_user.id]['Наименование']}\n" \
                f" Количество: {user_dict[message.from_user.id]['Количество']}\n" \
                f" Телефон: {user_dict[message.from_user.id]['Телефон']}\n" \
                f" Адрес: {user_dict[message.from_user.id]['Адрес']}\n"
        keyboard = create_replay_keyboard(2, 'Да', 'Нет')
        await message.answer(
            text=f'<b>Адрес</b>: {message.text[:30]}\n'
                 f'<b>Подтвердите заказ:</b>\n\n {order}',
            reply_markup=keyboard)


    @router.message(lambda x: x.text == 'Да')
    async def confirm_order(message: Message):
        order_id = str(message.from_user.id) + '_' + message.date.__str__()
        orders_dict[order_id] = user_dict[message.from_user.id]
        await message.answer(
            text=bot_message['created_order'],
            reply_markup=ReplyKeyboardRemove())

    @router.message(lambda x: x.text == 'Нет')
    async def cancel_order(message: Message):
        await message.answer(
            text=bot_message['canceled_order'],
            reply_markup=ReplyKeyboardRemove())

    @router.message()
    async def process_wrong_message(message: Message):
        await message.answer(
            text=bot_message['wrong_message'],
            reply_markup=ReplyKeyboardRemove())

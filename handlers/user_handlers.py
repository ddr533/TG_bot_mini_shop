from aiogram.dispatcher.filters import CommandStart, CommandHelp, Regexp
from aiogram.types import Message, CallbackQuery
from aiogram import Dispatcher
from aiogram.types import ReplyKeyboardRemove
from lexicon.lexicon import product_buttons, commands_text, bot_message
from keyboards.inline_user_keyboards import create_inline_kb
from keyboards.replaykeyboard import create_replay_keyboard


def process_user_handlers(dp: Dispatcher, user_dict: dict, orders_dict: dict):
    @dp.message_handler(CommandStart())
    async def process_start_command(message: Message):
        user_id = message.from_user.id
        if user_id not in user_dict:
            user_dict.setdefault(user_id, {'Наименование': None,
                                           'Количество': 0,
                                           'Телефон': None,
                                           'Адрес': None})
        keyboard = create_inline_kb(1, *product_buttons.keys())
        await message.answer(text=commands_text['/start'],
                             reply_markup=keyboard)

    @dp.message_handler(CommandHelp())
    async def process_help_command(message: Message):
        keyboard = create_inline_kb(1, *product_buttons.keys())
        await message.answer(text=commands_text['/help'],
                             reply_markup=keyboard)

    @dp.message_handler(commands=['cancel'])
    async def process_cancel_command(message: Message):
        keyboard = create_inline_kb(1, *product_buttons.keys())
        await message.answer(text=commands_text['/cancel'],
                             reply_markup=ReplyKeyboardRemove())

    @dp.callback_query_handler()
    async def push_product_button(callback: CallbackQuery):
        if callback.from_user.id in user_dict:
            user_dict[callback.from_user.id]['Наименование']\
                = product_buttons[callback.data]
        await dp.bot.send_message(chat_id = callback.message.chat.id,
                                  text=f'Вы выбрали {product_buttons[callback.data]}\n'
                                       f'<b>Сколько штучек нужно (не более 100)?</b>')
        await callback.answer()

    @dp.message_handler(lambda x: x.text.isdigit() and 1 <= len(x.text.lstrip('0')) <= 2)
    async def get_amount(message: Message):
        if message.from_user.id in user_dict:
            user_dict[message.from_user.id]['Количество'] = message.text.lstrip('0')
        await dp.bot.send_message(chat_id = message.chat.id,
                                  text=f'<b>Количество</b>: {message.text.lstrip("0")} шт.\n'
                                       f'Напишите номер телефона для связи или\n'
                                       f'/cancel для отмены')

    @dp.message_handler(Regexp(r'^8\d{10}$'))
    async def get_phone(message: Message):
        if message.from_user.id in user_dict:
            user_dict[message.from_user.id]['Телефон'] = message.text
        await dp.bot.send_message(chat_id = message.chat.id,
                                  text=f'<b>Телефон</b>: {message.text}\n'
                                       f'Укажите предварительный адрес доставки, '
                                       f'улица/дом или /cancel для отмены')


    @dp.message_handler(Regexp(r'(\w\D+)\s*\d+.*'))
    async def get_address(message: Message):
        if message.from_user.id in user_dict:
            user_dict[message.from_user.id]['Адрес'] = message.text[:50]
        order = f"Вид: {user_dict[message.from_user.id]['Наименование']}\n" \
                f" Количество: {user_dict[message.from_user.id]['Количество']}\n" \
                f" Телефон: {user_dict[message.from_user.id]['Телефон']}\n" \
                f" Адрес: {user_dict[message.from_user.id]['Адрес']}\n"
        keyboard = create_replay_keyboard(2, 'Да', 'Нет')
        await dp.bot.send_message(chat_id = message.chat.id,
                                  text=f'<b>Адрес</b>: {message.text[:30]}\n'
                                       f'<b>Подтвердите заказ:</b>\n\n {order}',
                                  reply_markup=keyboard)


    @dp.message_handler(lambda x: x.text == 'Да')
    async def confirm_order(message: Message):
        order_id = str(message.from_user.id) + '_' + message.date.__str__()
        orders_dict[order_id] = user_dict[message.from_user.id]
        await dp.bot.send_message(chat_id = message.chat.id,
                                  text=bot_message['created_order'],
                                  reply_markup=ReplyKeyboardRemove())

    @dp.message_handler(lambda x: x.text == 'Нет')
    async def cancel_order(message: Message):
        await dp.bot.send_message(chat_id = message.chat.id,
                                  text=bot_message['canceled_order'],
                                  reply_markup=ReplyKeyboardRemove())

    @dp.message_handler()
    async def process_wrong_message(message: Message):
        await dp.bot.send_message(chat_id = message.chat.id,
                                  text=bot_message['wrong_message'],
                                  reply_markup=ReplyKeyboardRemove())
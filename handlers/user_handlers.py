from aiogram.filters import CommandStart, Command, Text, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
from aiogram.types import ReplyKeyboardRemove
from lexicon.lexicon import product_buttons, commands_text, bot_message
from keyboards.inline_user_keyboards import create_inline_kb
from keyboards.replaykeyboard import create_replay_keyboard


class FSMFillForm(StatesGroup):
    choose_product = State()        # Состояние ожидания выбора продукта
    choose_amount = State()         # Состояние ожидания ввода количества
    put_phone_number = State()      # Состояние ожидания ввода номера телефона
    put_address = State()           # Состояние ожидания ввода вдреса
    confirm = State()               # Состояние ожидания подтверждения заказа



def process_users_router(router: Router, user_dict: dict, orders_dict: dict):
    @router.message(CommandStart(), StateFilter(default_state))
    async def process_start_command(message: Message, state: FSMContext):
        """
        Хэндлер срабатывает на команду /start.
        Предлагает выбрать категорию продукта, нажатием на кнопку.
        Запускает машину состояний.
        """
        user_id = message.from_user.id
        if user_id not in user_dict:
            user_dict.setdefault(user_id, {'Наименование': None,
                                           'Количество': 0,
                                           'Телефон': None,
                                           'Адрес': None})
        keyboard = create_inline_kb(1, **product_buttons)
        await message.answer(text=commands_text['/start'],
                             reply_markup=keyboard)
        await state.set_state(FSMFillForm.choose_product)

    @router.message(Command(commands='help'))
    async def process_help_command(message: Message, state: FSMContext):
        """Выводит справку о боте. Сбрасывает машину состояний."""
        await message.answer(text=commands_text['/help'])
        await state.clear()

    @router.message(Command(commands='cancel'), ~StateFilter(default_state))
    async def process_cancel_command(message: Message, state: FSMContext):
        """
        Хэндлер срабатывает на команду '/cancel' в состояниях кроме дефолтного.
        Сбрасывает Машину состояний.
        """
        await message.answer(text=commands_text['/cancel'],
                             reply_markup=ReplyKeyboardRemove())
        await state.clear()

    @router.message(Command(commands='cancel'), StateFilter(default_state))
    async def process_cancel_command(message: Message):
        """
        Хэндлер срабатывает на команду '/cancel' в дефолтном состоянии.
        Показывает сообщение, что пользователь находится вне процесса заказа.
        """
        await message.answer(text=commands_text['/cancel_from_no_fsm'],
                             reply_markup=ReplyKeyboardRemove())

    @router.callback_query(StateFilter(FSMFillForm.choose_product),
                           Text(text=[*product_buttons.keys()]))
    async def push_product_button(callback: CallbackQuery, state: FSMContext):
        """
        Ожидает нажатия на кнопку с наименованием продукта.
        Переводит бота в состояние ожидания ввода кол-ва.
        """
        user_dict[callback.from_user.id]['Наименование']\
                = product_buttons[callback.data]
        await callback.message.edit_text(
            text=f'Вы выбрали {product_buttons[callback.data]}\n'
                 f'Введите количество до 10 кг.')
        await state.update_data(name=callback.from_user.id)
        await state.set_state(FSMFillForm.choose_amount)

    @router.message(StateFilter(FSMFillForm.choose_product))
    async def wrong_product_button(messge: Message):
        """Срабатывает на неверное сообщение в процессе выбора продукта."""
        keyboard = create_inline_kb(1, **product_buttons)
        await messge.answer(text=bot_message['wrong_product'],
                            reply_markup=keyboard)

    @router.message(StateFilter(FSMFillForm.choose_amount),
                    F.text.regexp(r'^\d?.?\d$'),
                    lambda x: 0 < float(x.text) <= 10,
                    lambda x: float(x.text) % 0.5 == 0,
                    lambda x: len(x.text) <= 3,
                    )
    async def get_amount(message: Message, state: FSMContext):
        """
        Ожидает ввод количества продукта.
        Переводит бота в состояние ожидания ввода номера телефона.
        """
        user_dict[message.from_user.id]['Количество'] = message.text
        await message.answer(
            text=f'<b>Количество</b>: {message.text} кг.\n'
                 f'Напишите номер телефона для связи или\n'
                 f'/cancel для отмены')
        await state.set_state(FSMFillForm.put_phone_number)

    @router.message(StateFilter(FSMFillForm.choose_amount))
    async def wrong_amount(message: Message):
        """Срабатывет, если введено некорректное кол-во."""
        await message.answer(text=bot_message['wrong_amount'])

    @router.message(StateFilter(FSMFillForm.put_phone_number),
                    F.text.regexp(r'^8\d{10}$'))
    async def get_phone(message: Message, state: FSMContext):
        """
        Ожидает ввод номера телефона.
        Переводит бота в состояние ожидания ввода адреса.
        """
        user_dict[message.from_user.id]['Телефон'] = message.text
        await message.answer(
            text=f'<b>Телефон</b>: {message.text}\n'
                 f'Укажите адрес для доставки,'
                 f'улица/дом или /cancel для отмены')
        await state.set_state(FSMFillForm.put_address)

    @router.message(StateFilter(FSMFillForm.put_phone_number))
    async def wrong_phone(message: Message):
        """Срабатывает при непарвильном вводе номера телефона."""
        user_dict[message.from_user.id]['Телефон'] = message.text
        await message.answer(text=bot_message['wrong_phone'])

    @router.message(StateFilter(FSMFillForm.put_address),
                    F.text.regexp(r'(\w+\D+)\s*\d+.*'))
    async def get_address(message: Message, state: FSMContext):
        """Ожидает ввод адрес. Первеодит бота в состояние подтверждения."""
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
        await state.set_state(FSMFillForm.confirm)

    @router.message(StateFilter(FSMFillForm.put_address))
    async def wrong_address(message: Message):
        """Срабатывает при неправильном вводе адреса."""
        await message.answer(text=bot_message['wrong_address'])

    @router.message(StateFilter(FSMFillForm.confirm),
                    lambda x: x.text == 'Да')
    async def wrong_confirm_order(message: Message, state: FSMContext):
        """Ожидает подвтерждение заказа. Выключает машину состояний."""
        order_id = str(message.from_user.id) + '_' + message.date.__str__()
        orders_dict[order_id] = user_dict[message.from_user.id]
        await message.answer(
            text=bot_message['created_order'],
            reply_markup=ReplyKeyboardRemove())
        await state.clear()

    @router.message(StateFilter(FSMFillForm.confirm),
                    lambda x: x.text == 'Нет')
    async def cancel_order(message: Message, state: FSMContext):
        """Ожидает подтверждение заказа. Выключает машину состояний."""
        await message.answer(
            text=bot_message['canceled_order'],
            reply_markup=ReplyKeyboardRemove())
        await state.clear()

    @router.message(StateFilter(FSMFillForm.confirm))
    async def wrong_confirm(message: Message):
        """Срабатывает на некорректный ввод в состоянии подтверждения."""
        await message.answer(text=bot_message['confirm'])
        keyboard = create_replay_keyboard(2, 'Да', 'Нет')
        await message.answer(text=bot_message['confirm'], reply_markup=keyboard)

    @router.message(StateFilter(default_state))
    async def process_wrong_message(message: Message):
        """Срабатывает на ввод прочих сообщений вне машины состояний."""
        await message.answer(
            text=bot_message['wrong_message'],
            reply_markup=ReplyKeyboardRemove())

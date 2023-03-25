product_buttons: dict = {
    'but_1': '🍒 Вишня, 250 руб./кг.',
    'but_2': '🍓 Клубника, 350 руб./кг.',
    'but_3': '🍎 Ранетки, 100 руб./кг.',
    'but_4': '🍏 Зеленое яблоко, 150 руб./кг.',
    'but_5': '🍅 Помидоры,  200 руб./кг.'
}

commands_text: dict = {
    '/start': 'Вас приветствует бот, который поможет Вам заказать натуральные'
              'овощи и фрукты из сада ! ✌ \n Чтобы узнать правила пользования'
              'ботом, наберите /help\n <b>Чтобы начать заказ выберите'
              'категорию!!!</b>',
    '/help': '1. Для начала заказа наберите команду /start.\n'
             '2. Чтобы прервать заказ наберите команду /cancel.\n'
             '3. При вводе номера телефона пишите только цифры, '
             'без пробелов, начиная с 8. В формате 89237654538.\n'
             '4. Адрес лучше вводить в формате "улица дом".\n'
             'Например, Малахова 54.\n\n',
    '/cancel': 'Заказ отменен. Для нового заказа наберите /start',
    '/cancel_from_no_fsm': 'Вы не в процессе заказа, наберите команду /start'
}

bot_message: dict = {
    'created_order': '<b>Ваш заказ подтвержден! Скоро с Вами свяжутся 📞</b>\n'
                     'Чтобы сделать новый заказ напишите /start\n'
                     'Чтобы отменить сделанный заказ позвоните по телефону ...',
    'canceled_order': 'Заказ отменен, чтобы начать заново наберите /start',
    'wrong_message': 'Неверный формат ввода данных!\n'
                     'Начните заказ заново /start',
    'wrong_amount': 'Введите число от 0.5 до 10 кг, кратное 0.5',
    'wrong_phone': 'Введите номер телефона в формате 89111111111',
    'wrong_address': 'Введите адрес в формате Улица Номер дома\n,'
                     'например, Малахова 34',
    'confirm': 'Нажмите кнопку Да, или Нет.',
    'wrong_product': 'Выберите продукт из списка. Для отмены наберите /cancel.'
}

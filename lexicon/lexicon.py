product_buttons: dict =    {'but_1': '🍒 Сладенькая №1 (вишневая)  250 руб./л.🍒',
                           'but_2': '🍓 Сладенькая №2 (малиновая)  250 руб./л.🍓',
                           'but_3': '🔥 Ядреная, 45 градусов 350 руб./л.🔥',
                           'but_4': '🥃 Выдержанная из погреба  300 руб./л.🥃',
                           'but_5': '🍺 Крафтовое пиво лайт   150 руб./л.🍺'}


commands_text: dict =      {'/start': 'Вас приветствует бот, который поможет Вам заказать приятные напитки! ✌ \n'
                                  'Чтобы узнать правила пользования ботом, наберите /help\n'
                                  '<b>🍾Чтобы начать заказ выберите вкусняшку!!!!🍾</b>',
                            '/help': '1. Для начала заказа начните выбирать напиток.\n'
                                     '2. Чтобы прервать заказ наберите команду /cancel.\n'
                                     '3. Чтобы начать заказ заново наберите команду /start.\n'
                                     '4. При вводе номера телефона пишите только цифры, без пробелов, начиная с 8.'
                                     ' В формате 89237654538.\n'
                                     '5. Адрес лучше вводить в формате\n"улица дом". Например, Малахова 54.\n\n'
                                     '<b>Если всё понятно, то погнали?))))</b>\n',
                            '/cancel': 'Заказ отменен. Для нового заказа наберите /start'

                           }

bot_message: dict =        {'created_order': '<b>Ваш заказ подтвержден! Скоро с Вами свяжутся 📞</b>\n'
                                        f'Чтобы сделать новый заказ напишите /start\n'
                                        f'Чтобы отменить сделанный заказ позвоните по телефону 911',

                            'canceled_order': 'Заказ отменен, чтобы начать заново наберите /start',
                            'wrong_message': 'Неверный формат ввода данных!\nНачните заказ заново /start'}
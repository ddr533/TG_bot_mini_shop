from aiogram import Dispatcher, types


# Функция для настройки кнопки Menu бота
async def set_main_menu(dp: Dispatcher):
    main_menu_commands = [
        types.BotCommand(command='/start', description='Сделать новый заказ'),
        types.BotCommand(command='/help', description='Получить справку'),
        types.BotCommand(command='/cancel', description='Отменить текущий заказ')]
    await dp.bot.set_my_commands(main_menu_commands)
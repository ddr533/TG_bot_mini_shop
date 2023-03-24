from aiogram import types
from aiogram import Bot

async def set_main_menu(bot: Bot):
    """Функция для настройки кнопки Menu бота."""
    main_menu_commands = [
        types.BotCommand(command='/start', description='Сделать новый заказ'),
        types.BotCommand(command='/help', description='Получить справку'),
        types.BotCommand(command='/cancel', description='Отменить заказ')]
    await bot.set_my_commands(main_menu_commands)
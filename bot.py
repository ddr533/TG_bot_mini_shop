import asyncio
from aiogram import Bot, Dispatcher
from config.config import Config, load_config
from handlers.user_handlers import process_user_handlers
from handlers.admin_handlers import process_admin_handlers
from utils.utils import open_dict, dump_dict
from keyboards.command_menu import set_main_menu


async def main():
    config: Config = load_config()
    bot: Bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp: Dispatcher = Dispatcher(bot)

    admin_id = config.tg_bot.admin_ids
    print('Admin_id', admin_id)
    user_dict = open_dict('users_data.pickle')
    asyncio.create_task(dump_dict(user_dict, 'users_data.pickle'))

    orders_dict = open_dict('orders_data.pickle')
    asyncio.create_task(dump_dict(orders_dict, 'orders_data.pickle'))

    await set_main_menu(dp)
    process_admin_handlers(dp, orders_dict, admin_id)
    process_user_handlers(dp, user_dict, orders_dict)

    try:
        await dp.skip_updates()
        await dp.start_polling()

    finally:
        await bot.close()


if __name__ == '__main__':
    asyncio.run(main())
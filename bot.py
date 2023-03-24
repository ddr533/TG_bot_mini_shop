import asyncio
from aiogram import Bot, Dispatcher, Router, F

from config.config import Config, load_config
from handlers.user_handlers import process_users_router
from handlers.admin_handlers import process_admin_router
from utils.utils import open_dict, dump_dict


from keyboards.command_menu import set_main_menu

users_dict = open_dict('users_data.pickle')
orders_dict = open_dict('orders_data.pickle')


async def main():
    config: Config = load_config()
    admins_id = config.tg_bot.admin_ids
    bot: Bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp: Dispatcher = Dispatcher()

    router_user: Router = Router(name='user_router')

    router_admin: Router = Router(name='admin_router')
    router_admin.message.filter(F.from_user.id.in_(admins_id))

    await set_main_menu(bot)

    process_admin_router(router_admin, orders_dict)
    process_users_router(router_user, users_dict, orders_dict)

    asyncio.create_task(dump_dict(users_dict, 'users_data.pickle'))
    asyncio.create_task(dump_dict(orders_dict, 'orders_data.pickle'))

    dp.include_router(router_admin)
    dp.include_router(router_user)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)

    finally:
        await bot.close()


if __name__ == '__main__':
    asyncio.run(main())

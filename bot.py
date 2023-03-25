import asyncio
import logging
from logging.handlers import RotatingFileHandler

from aiogram import Bot, Dispatcher, Router, F
from aiogram.fsm.storage.memory import MemoryStorage

from config.config import Config, load_config
from handlers.user_handlers import process_users_router
from handlers.admin_handlers import process_admin_router
from utils.utils import open_dict, dump_dict

from keyboards.command_menu import set_main_menu


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s, %(levelname)s, %(message)s, %(name)s',
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = RotatingFileHandler('log/bot_main.log', maxBytes=50000000,
                              backupCount=5, encoding='UTF-8')
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger.addHandler(handler)
handler.setFormatter(formatter)

users_dict = open_dict('users_data.pickle')
orders_dict = open_dict('orders_data.pickle')


async def main():
    config: Config = load_config()
    admins_id = config.tg_bot.admin_ids
    storage: MemoryStorage = MemoryStorage()

    logger.info('Starting bot')
    bot: Bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp: Dispatcher = Dispatcher(storage=storage)

    router_user: Router = Router(name='user_router')

    router_admin: Router = Router(name='admin_router')
    router_admin.message.filter(F.from_user.id.in_(admins_id))

    await set_main_menu(bot)

    process_admin_router(router_admin, orders_dict)
    process_users_router(router_user, users_dict, orders_dict)

    asyncio.create_task(dump_dict(users_dict, 'users_data.pickle',
                                  sleep_time=120))
    asyncio.create_task(dump_dict(orders_dict, 'orders_data.pickle',
                                  sleep_time=60))

    dp.include_router(router_admin)
    dp.include_router(router_user)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)

    finally:
        await bot.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error('Bot stopped!')

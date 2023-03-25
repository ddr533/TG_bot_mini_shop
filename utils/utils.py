import asyncio
import logging
import pickle
from logging.handlers import RotatingFileHandler

logger = logging.getLogger(__name__)
handler = RotatingFileHandler('log/pickle.log', maxBytes=50000000, backupCount=5,
                              encoding='UTF-8')
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger.addHandler(handler)
handler.setFormatter(formatter)


def open_dict(file_name: str):
    try:
        with open(file_name, 'rb') as f:
            user: dict = pickle.load(f)
        return user if isinstance(user, dict) else None
    except FileNotFoundError:
        logger.error('Файл со словарем не найден. Создан новый файл.')
        user: dict = {}
        return user
    except Exception as e:
        logger.critical(f'Файл со словарем прочитан с ошибками {e}.')


async def dump_dict(dict: dict, file_name: str, sleep_time: int = 10):
    while True:
        with open(file_name, 'wb') as f:
            pickle.dump(dict, f)
            logger.debug('Создан дамп словаря.')
        await asyncio.sleep(sleep_time)

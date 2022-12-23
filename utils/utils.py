import asyncio
import pickle
import os

def open_dict(file_name):
    try:
        with open(file_name, 'rb') as f:
            user: dict = pickle.load(f)
        return user if isinstance(user, dict) else None
    except FileNotFoundError:
        user: dict = {}
        return user
    except Exception as e:
        print('Словарь с пользователями прочитан с ошибками', e)


async def dump_dict(dict: dict, file_name: str):
    while True:
        print(dict)
        with open(file_name, 'wb') as f:
            pickle.dump(dict, f)
        await asyncio.sleep(10)



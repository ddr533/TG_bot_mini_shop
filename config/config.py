from __future__ import annotations
from environs import Env


class TgBot:
    def __init__(self, token: str, admin_ids: list[int]):
        self.token = token
        self.admin_ids = admin_ids


class Config:
    def __init__(self, tg_bot: TgBot):
        self.tg_bot = tg_bot


def load_config(path: str | None = None) -> Config:
    env: Env = Env()
    env.read_env(path)
    return Config(tg_bot=TgBot(token=env('BOT_TOKEN'),
                               admin_ids=list(map(int, env.list('ADMIN_IDS')))))


__all__ = ['load_config']

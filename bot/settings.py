from pydantic_settings import BaseSettings, SettingsConfigDict

from dotenv import load_dotenv

import os

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from yarl import URL

load_dotenv()


class Settings(BaseSettings):

    BOT_TOKEN: str = os.getenv("BOT_TOKEN")
    BOT_TIMEZONE: str = "Europe/Moscow"

    # Путь к логам
    PATH_LOGS: str = "bot/data/logs.log"

    FSM_REDIS_HOST: str = os.getenv("FSM_REDIS_HOST").strip()
    FSM_REDIS_DB: int = os.getenv("FSM_REDIS_DB").strip()

    REDIS_HOST: str = os.getenv("REDIS_HOST").strip()
    REDIS_DB: int = os.getenv("REDIS_DB").strip()

    model_config = SettingsConfigDict(env_file='../.env', env_file_encoding='utf-8')

    @property
    def fsm_redis_url(self) -> str:
        """
        создание URL для подключения к редису

        :return: redis connection url
        """
        return str(URL.build(
            scheme="redis",
            host=self.FSM_REDIS_HOST,
            path="/" + str(self.FSM_REDIS_DB)
        ))

settings = Settings()

BOT_SCHEDULER = AsyncIOScheduler(timezone=settings.BOT_TIMEZONE)

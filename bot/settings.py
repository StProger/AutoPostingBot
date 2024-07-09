from pydantic_settings import BaseSettings, SettingsConfigDict

from dotenv import load_dotenv

import os

from apscheduler.schedulers.asyncio import AsyncIOScheduler


load_dotenv()


class Settings(BaseSettings):

    BOT_TOKEN: str = os.getenv("BOT_TOKEN")
    BOT_TIMEZONE: str = "Europe/Moscow"

    model_config = SettingsConfigDict(env_file='../.env', env_file_encoding='utf-8')


settings = Settings()

BOT_SCHEDULER = AsyncIOScheduler(timezone=settings.BOT_TIMEZONE)

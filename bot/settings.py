from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from pydantic_settings import BaseSettings, SettingsConfigDict

from dotenv import load_dotenv

import os, json

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler_di import ContextSchedulerDecorator
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

    ADMIN_IDS: list[int] = json.loads(os.getenv("ADMIN_IDS"))



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
jobstores = {
    'default': RedisJobStore(jobs_key='dispatched_trips_jobs',
                             run_times_key='dispatched_trips_running',
                             host='localhost',
                             db=3,
                             port=6379)
}
BOT_SCHEDULER = AsyncIOScheduler(jobstores=jobstores, timezone=settings.BOT_TIMEZONE)

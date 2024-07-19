import sys

from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Dispatcher, Bot

from bot.settings import settings, BOT_SCHEDULER
from bot.routers import register_all_routers
from bot import logging
from bot.database.engine import db
from bot.database.models.groups import Groups
from bot.database.models.admins import Admins
from bot.database.models.tasks_posts import TasksPosts
from bot.filters import init_filters

import asyncio


async def main():

    storage = RedisStorage.from_url(settings.fsm_redis_url)

    dp = Dispatcher(storage=storage)

    # dp.message.filter(IsAdmin())
    # dp.callback_query.filter(IsAdmin())

    bot = Bot(settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML", link_preview_is_disabled=True))
    BOT_SCHEDULER.ctx.add_instance(bot, declared_class=Bot)
    init_filters(dp)
    register_all_routers(dp)
    await bot.delete_webhook(drop_pending_updates=True)
    await logging.setup()

    BOT_SCHEDULER.start()

    try:

        await dp.start_polling(bot)

    except KeyboardInterrupt:
        sys.exit(1)
    finally:
        await bot.session.close()


if __name__ == '__main__':

    db.create_tables([Groups, Admins, TasksPosts])
    asyncio.run(main())
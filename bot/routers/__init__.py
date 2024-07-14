from aiogram import Dispatcher

from bot.routers.admin import add_admin, delete_admin
from bot.routers.admin import fast_post
from bot.routers import start
from bot.routers.chat_event import join, left
from bot.routers.admin import time_post


def register_all_routers(dp: Dispatcher):

    dp.include_router(add_admin.router)
    dp.include_router(delete_admin.router)
    dp.include_router(fast_post.router)
    dp.include_router(start.router)
    dp.include_router(join.router)
    dp.include_router(left.router)
    dp.include_router(time_post.router)

from aiogram import Dispatcher

from bot.routers.admin import add_admin, delete_admin


def register_all_routers(dp: Dispatcher):

    dp.include_router(add_admin.router)
    dp.include_router(delete_admin.router)

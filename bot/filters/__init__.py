from aiogram import Dispatcher

from bot.filters.admin_filter import IsAdmin


def init_filters(dp: Dispatcher):

    dp.callback_query.filter(IsAdmin())
    dp.message.filter(IsAdmin())

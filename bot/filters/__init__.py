from aiogram import Dispatcher

from bot.filters.admin_filter import IsAdmin
from bot.filters.chat_type import ChatTypeFilter


def init_filters(dp: Dispatcher):

    dp.callback_query.filter(IsAdmin())
    dp.message.filter(IsAdmin())

    dp.message.filter(ChatTypeFilter(chat_type="private"))
    dp.callback_query.filter(ChatTypeFilter(chat_type="private"))

from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery
from aiogram import Bot

from bot.database.api import get_admins


class IsAdmin(Filter):
    """
    Check if user is an admin
    """

    async def __call__(self, update: Message | CallbackQuery, bot: Bot) -> bool:

        admins = await get_admins()

        return update.from_user.id in admins

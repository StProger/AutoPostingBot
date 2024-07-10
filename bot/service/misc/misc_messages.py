from aiogram import types

from bot.database.models.groups import Groups
from bot.keyboards import get_menu_key, get_fast_post_choose_channel_key


async def start_message(message: types.Message):

    await message.answer(
        text="Главное меню",
        reply_markup=get_menu_key()
    )


async def fast_post_choose_channel(
        message: types.Message,
        groups: list[Groups]
):

    await message.answer(
        text="Выберите канал для поста👇",
        reply_markup=get_fast_post_choose_channel_key(groups)
    )

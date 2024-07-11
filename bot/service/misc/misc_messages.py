from aiogram import types

from bot.database.models.groups import Groups
from bot.keyboards import get_menu_key, get_fast_post_choose_channel_key, get_fast_post_thread_id_key, button_menu
from bot.service.redis_serv.user import set_msg_to_delete


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


async def fast_post_ask_thread_id(
        message: types.Message
):

    await message.answer(
        text="Пост в определённую тему?",
        reply_markup=get_fast_post_thread_id_key()
    )


async def fast_post_get_thread_id(
        message: types.Message
):

    mes_ = await message.answer(
        text="Отправьте ID темы.",
        reply_markup=button_menu()
    )

    await set_msg_to_delete(
        user_id=message.from_user.id,
        message_id=mes_.message_id
    )


async def fast_post_get_template(message: types.Message):

    await message.answer(
        text="Отправьте пост.",
        reply_markup=button_menu()
    )
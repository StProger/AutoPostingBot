from aiogram import types
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.database.models.groups import Groups


def get_menu_key():

    return types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text="Сделать пост", callback_data="make_post"
                    ),
                    types.InlineKeyboardButton(
                        text="Запланировать пост",callback_data="plan_post"
                    )
                ],
                [
                    types.InlineKeyboardButton(
                        text="Запланированные посты",callback_data="get_plan_posts"
                    )
                ]
            ]
        )


def get_fast_post_choose_channel_key(groups: list[Groups]):

    builder = InlineKeyboardBuilder()

    for group in groups:

        builder.button(
            text=group.name, callback_data=f"fast_post_{group.group_id}"
        )

    builder.button(
        text="Меню", callback_data="menu"
    )

    return builder.as_markup()
from operator import contains

from aiogram import types
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.database.models.groups import Groups
from bot.database.models.tasks_posts import TasksPosts


def button_menu():

    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="Меню", callback_data="menu"
                )
            ]
        ]
    )


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
            text=group.name, callback_data=f"channel_p_{group.id}"
        )

    builder.button(
        text="Меню", callback_data="menu"
    )
    builder.adjust(1)

    return builder.as_markup()


def get_fast_post_thread_id_key():

    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="Да✅", callback_data="with_thread_id"
                ),
                types.InlineKeyboardButton(
                    text="Нет❌", callback_data="no_thread_id"
                )
            ],
            [
                types.InlineKeyboardButton(
                    text="Меню", callback_data="menu"
                )
            ]
        ]
    )


def get_post_confirm_key():

    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="Да✅", callback_data="confirm_fp"
                ),
                types.InlineKeyboardButton(
                    text="Нет❌", callback_data="unconfirm_fp"
                )
            ],
            [
                types.InlineKeyboardButton(
                    text="Меню", callback_data="menu"
                )
            ]
        ]
    )


def select_time_post(selected_hours: int = 0):

    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="-", callback_data="minus_hour"
                ),
                types.InlineKeyboardButton(
                    text=str(selected_hours), callback_data="none"
                ),
                types.InlineKeyboardButton(
                    text="+", callback_data="plus_hour"
                )
            ],
            [
                types.InlineKeyboardButton(
                    text="Подтвердить время", callback_data="accept_time"
                )
            ],
            [
                types.InlineKeyboardButton(
                    text="Меню", callback_data="menu"
                )
            ]
        ]
    )


def lists_posts_key(posts: list[TasksPosts]):

    builder = InlineKeyboardBuilder()

    for index, post in enumerate(posts, start=1):

        if index % 4 == 0:

            builder.row(
                types.InlineKeyboardButton(
                    text=str(index), callback_data=f"get_post_{post.id}"
                )
            )
        else:

            builder.button(text=str(index), callback_data=f"get_post_{post.id}")

    builder.row(
        types.InlineKeyboardButton(
            text="Меню", callback_data="menu"
        )
    )

    return builder.as_markup()


def cancel_plan_post_key(post: TasksPosts):

    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="Отменить пост", callback_data=f"cancel_sp_{post.id}"
                )
            ],
            [
                types.InlineKeyboardButton(
                    text="Назад", callback_data="get_plan_posts"
                )
            ]
        ]
    )
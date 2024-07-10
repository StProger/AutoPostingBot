from aiogram import types


async def start_message(message: types.Message):

    await message.answer(
        text="Главное меню",
        reply_markup=types.InlineKeyboardMarkup(
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
    )
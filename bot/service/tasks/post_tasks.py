from aiogram import Bot


async def post_task(
        channel_name: str,
        channel_id: int,
        thread_id: int | None,
        message_id: int,
        user_id: int,
        bot: Bot
):

    try:

        await bot.copy_message(
            chat_id=channel_id,
            from_chat_id=user_id,
            message_id=message_id,
            message_thread_id=thread_id
        )
        await bot.copy_message(
            chat_id=user_id,
            message_id=message_id,
            from_chat_id=user_id
        )
        try:
            await bot.send_message(
                chat_id=user_id,
                text=f"Пост в группу {channel_name} сделан👆"
            )
        except:
            pass
    except:

        await bot.copy_message(
            chat_id=user_id,
            message_id=message_id,
            from_chat_id=user_id
        )
        await bot.send_message(
            text=f"Не получилось сделать пост выше в канал {channel_name} 👆.\n"
                 f"Убедитесь, что бот есть в группе и вы не удаляли свой пост из диалога с ботом.",
            chat_id=user_id
        )

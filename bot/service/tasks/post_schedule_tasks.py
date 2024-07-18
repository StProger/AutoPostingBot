from aiogram import Bot

from bot.database.models.tasks_posts import TasksPosts


async def post_schedule_task(
        channel_name: str,
        channel_id: int,
        thread_id: int | None,
        message_id: int,
        reply_markup,
        user_id: int,
        bot: Bot,
        job_id_db: int
):

    try:

        await bot.copy_message(
            chat_id=channel_id,
            from_chat_id=user_id,
            message_id=message_id,
            message_thread_id=thread_id,
            reply_markup=reply_markup
        )
        query = TasksPosts.delete().where(TasksPosts.id == job_id_db)
        query.execute()
        await bot.copy_message(
            chat_id=user_id,
            message_id=message_id,
            from_chat_id=user_id,
            reply_markup=reply_markup
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

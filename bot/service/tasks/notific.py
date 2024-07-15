from aiogram import Bot

from bot.database.models.tasks_posts import TasksPosts


async def notify_user(bot: Bot, post: TasksPosts, user_id):


    try:

        await bot.send_message(
            chat_id=post.user_id,
            text=f"Юзер с ID <code>{user_id}</code> отменил пост в канал {post.channel_name}"
        )
    except:
        pass
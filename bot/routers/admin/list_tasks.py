import asyncio
import json

from aiogram import Router, types, F
from apscheduler.job import Job

from bot.database.api import delete_task
from bot.keyboards import cancel_plan_post_key, button_menu
from bot.service.misc.misc_messages import list_posts_main
from bot.database.models.tasks_posts import TasksPosts
from bot.service.tasks.notific import notify_user
from bot.settings import BOT_SCHEDULER

router = Router()


@router.callback_query(F.data == "get_plan_posts")
async def get_plan_posts(callback: types.CallbackQuery):

    await callback.answer()
    await callback.message.delete()
    posts = TasksPosts.select()
    await list_posts_main(callback.message, posts)


@router.callback_query(F.data.startswith("get_post_"))
async def show_plan_post(callback: types.CallbackQuery):

    await callback.message.delete()

    post_id = int(callback.data.split("_")[-1])

    post: TasksPosts = TasksPosts.get(id=post_id)

    job: Job = BOT_SCHEDULER.get_job(post.task_id)

    reply_markup = post.reply_markup

    if reply_markup:

        reply_markup = json.loads(reply_markup)

    await callback.bot.copy_message(
        chat_id=callback.from_user.id,
        from_chat_id=post.user_id,
        message_id=post.message_id,
        reply_markup=reply_markup
    )

    await callback.message.answer(
        text=f"Вот запланированный пост👆\n\n"
             f"Название канала: {post.channel_name}\n"
             f"Время поста: {job.next_run_time}\n"
             f"<i><b>Чтобы отменить пост, нажмите кнопку ниже.</b></i>",
        reply_markup=cancel_plan_post_key(post)
    )


@router.callback_query(F.data.startswith("cancel_sp_"))
async def cancel_plan_post_key(callback: types.CallbackQuery):

    post_id = callback.data.split("_")[-1]
    post: TasksPosts = TasksPosts.get(id=post_id)
    await delete_task(int(post_id))

    if post.user_id != callback.from_user.id:

        asyncio.create_task(
            notify_user(
                callback.bot, post, callback.from_user.id
            )
        )

    await callback.message.edit_text(
        text="Пост отменён.",
        reply_markup=button_menu()
    )
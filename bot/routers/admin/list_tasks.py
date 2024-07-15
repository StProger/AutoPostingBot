from aiogram import Router, types, F

from bot.service.misc.misc_messages import list_posts_main
from bot.database.models.tasks_posts import TasksPosts

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

    await callback.bot.copy_message(
        chat_id=callback.from_user.id,
        from_chat_id=post.user_id,
        message_id=post.message_id
    )
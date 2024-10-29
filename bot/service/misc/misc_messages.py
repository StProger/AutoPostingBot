from aiogram import types, Bot
from apscheduler.job import Job

from bot.database.models.groups import Groups
from bot.database.models.tasks_posts import TasksPosts
from bot.database.api import delete_task
from bot.keyboards import get_menu_key, get_fast_post_choose_channel_key, get_fast_post_thread_id_key, button_menu, \
    select_time_post, lists_posts_key
from bot.service.redis_serv.user import set_msg_to_delete
from bot.settings import BOT_SCHEDULER


async def start_message(message: types.Message, bot: Bot):

    bot_info = await bot.get_me()

    await message.answer(
        text="Главное меню",
        reply_markup=get_menu_key(bot_info.username)
    )


async def choose_channel_message(
        message: types.Message,
        groups: list[Groups]
):

    await message.answer(
        text="Выберите канал для поста👇",
        reply_markup=get_fast_post_choose_channel_key(groups)
    )


async def ask_thread_id_message(
        message: types.Message
):

    await message.answer(
        text="Пост в определённую тему?",
        reply_markup=get_fast_post_thread_id_key()
    )


async def get_thread_id_message(
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


async def get_template_message(message: types.Message):

    await message.answer(
        text="Отправьте пост.",
        reply_markup=button_menu()
    )


async def get_time_public_post_message(message: types.Message):

    await message.answer(
        text="Через сколько часов опубликовать пост?",
        reply_markup=select_time_post()
    )



async def list_posts_main(message: types.Message, posts: list[TasksPosts]):

    text = "Список запланированных постов (время | канал)\n"

    for index, post in enumerate(posts, start=1):

        task: Job = BOT_SCHEDULER.get_job(post.task_id)
        if not task:
            await delete_task(task_id=post.id)
        text += f"{index}. {task.next_run_time.strftime('%Y-%m-%d %H:%M')} | {post.channel_name}\n"

    text += "Для выбора поста нажмите на его номер👇"

    await message.answer(
        text=text,
        reply_markup=lists_posts_key(posts)
    )
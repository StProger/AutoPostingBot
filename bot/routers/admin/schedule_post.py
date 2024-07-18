from datetime import datetime, timedelta, timezone

import pytz

from aiogram import Router, F, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from bot.database.api import add_task, update_task
from bot.database.models.groups import Groups
from bot.keyboards import button_menu, get_post_confirm_key
from bot.service.misc.misc_messages import choose_channel_message, ask_thread_id_message, get_template_message, \
    get_thread_id_message, get_time_public_post_message
from bot.service.redis_serv.user import get_msg_to_delete
from bot.service.tasks.post_schedule_tasks import post_schedule_task

from bot.settings import BOT_SCHEDULER


router = Router()


@router.callback_query(F.data == "plan_post")
async def choose_channel(callback: types.CallbackQuery, state: FSMContext):

    await state.set_state("plan_post:choose_channel")

    groups = Groups.select()

    await callback.message.delete()
    await choose_channel_message(callback.message, groups)


@router.callback_query(StateFilter("plan_post:choose_channel"),F.data.startswith("channel_p_"))
async def ask_thread_id(callback: types.CallbackQuery, state: FSMContext):

    await state.set_state("plan_post:thread_id")
    await callback.message.delete()

    group = Groups.get(id=int(callback.data.split("_")[-1]))

    await state.update_data(
        group_id=group.group_id,
        group_name=group.name
    )

    await ask_thread_id_message(callback.message)


@router.callback_query(StateFilter("plan_post:thread_id"), F.data == "no_thread_id")
async def get_time_post(callback: types.CallbackQuery, state: FSMContext):

    await state.set_state("plan_post:get_time_post")
    await state.update_data(
        thread_id=None,
        selected_time=0
    )
    await callback.message.delete()
    await get_time_public_post_message(callback.message)
    # await get_template_message(callback.message)


@router.callback_query(StateFilter("plan_post:thread_id"), F.data == "with_thread_id")
async def get_thread_id(callback: types.CallbackQuery, state: FSMContext):

    await state.set_state("plan_post:get_thread_id")
    await callback.message.delete()
    await get_thread_id_message(callback.message)


@router.message(StateFilter("plan_post:get_thread_id"))
async def get_time_post(message: types.Message, state: FSMContext):

    thread_id = message.text
    if not thread_id.isdigit():

        await message.answer(
            text="ID должен содержать только цифры.",
            reply_markup=button_menu()
        )

    else:

        await state.set_state("plan_post:get_time_post")
        await state.update_data(
            thread_id=int(thread_id),
            selected_time=0
        )
        try:
            await message.bot.delete_message(
                chat_id=message.chat.id,
                message_id=(await get_msg_to_delete(user_id=message.from_user.id))
            )
        except:
            pass

        await get_time_public_post_message(message)

        # await get_template_message(message)


@router.callback_query(StateFilter("plan_post:get_time_post"), F.data == "accept_time")
async def get_template_post(callback: types.CallbackQuery, state: FSMContext):

    await state.set_state("plan_post:get_post_template")

    data_state = await state.get_data()

    selected_time = data_state["selected_time"]

    if selected_time == 0:

        await callback.answer("Вы не выбрали время.")
        return

    date = (datetime.now(pytz.timezone('Europe/Moscow')) + timedelta(hours=selected_time)).strftime('%Y-%m-%d %H:%M:%S')

    await state.update_data(
        run_date=date
    )

    await callback.message.delete()
    await get_template_message(callback.message)


@router.message(StateFilter("plan_post:get_post_template"))
async def accept_fast_post(message: types.Message, state: FSMContext):

    await state.set_state("plan_post:access_post")
    data_state = await state.get_data()
    await state.update_data(
        message_post_id=message.message_id,
        reply_markup=message.reply_markup.dict() if message.reply_markup else None
    )
    await message.bot.copy_message(
        chat_id=message.chat.id,
        from_chat_id=message.chat.id,
        message_id=message.message_id,
        reply_markup=message.reply_markup.dict if message.reply_markup else None
    )

    await message.answer(
        f"""
☝️Вот так выглядит ваш пост.
    
<b>Название канала</b>: {data_state["group_name"]}
    
<b>Время публикации поста</b>: {data_state["run_date"]}
    
Запланировать пост?""",
        reply_markup=get_post_confirm_key()
    )


# Отказ от поста
@router.callback_query(StateFilter("plan_post:access_post"), F.data == "unconfirm_fp")
async def get_new_template_fast_post(callback: types.CallbackQuery, state: FSMContext):

    await state.set_state("plan_post:get_post_template")
    await callback.message.delete()
    await get_template_message(callback.message)


# Принятие поста
@router.callback_query(StateFilter("plan_post:access_post"), F.data == "confirm_fp")
async def make_plan_post(callback: types.CallbackQuery, state: FSMContext):

    data_state = await state.get_data()

    new_task: int = await add_task(
        data_state["group_name"],
        data_state["group_id"],
        data_state["thread_id"],
        data_state["message_post_id"],
        str(data_state["reply_markup"]),
        callback.from_user.id
    )

    new_post_job = BOT_SCHEDULER.add_job(
        func=post_schedule_task,
        trigger="date",
        run_date=data_state["run_date"],
        next_run_time=data_state["run_date"],
        args=(
            data_state["group_name"],
            data_state["group_id"],
            data_state["thread_id"],
            data_state["message_post_id"],
            data_state["reply_markup"],
            callback.from_user.id,
            callback.bot,
            new_task
        )
    )

    await update_task(new_task, new_post_job.id)

    await state.clear()
    await callback.message.delete()
    await callback.message.answer(
        text=f"Пост запланирован на\n{data_state['run_date']}",
        reply_markup=button_menu()
    )

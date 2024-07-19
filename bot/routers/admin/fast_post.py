from aiogram import Router, F, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

import asyncio

from bot.database.models.groups import Groups
from bot.keyboards import button_menu, get_post_confirm_key
from bot.service.misc.misc_messages import choose_channel_message, \
    ask_thread_id_message, get_template_message, get_thread_id_message
from bot.service.redis_serv.user import get_msg_to_delete
from bot.service.tasks.post_tasks import post_task

router = Router()


@router.callback_query(F.data == "make_post")
async def choose_channel(callback: types.CallbackQuery, state: FSMContext):

    await state.set_state("make_post:choose_channel")
    groups = Groups.select()

    await callback.message.delete()
    await choose_channel_message(callback.message, groups)


@router.callback_query(StateFilter("make_post:choose_channel"), F.data.startswith("channel_p_"))
async def ask_thread_id(callback: types.CallbackQuery, state: FSMContext):

    await state.set_state("make_post:thread_id")
    await callback.message.delete()

    group = Groups.get(id=int(callback.data.split("_")[-1]))

    await state.update_data(
        group_id=group.group_id,
        group_name=group.name
    )

    await ask_thread_id_message(callback.message)


@router.callback_query(StateFilter("make_post:thread_id"), F.data == "no_thread_id")
async def get_template_post(callback: types.CallbackQuery, state: FSMContext):

    await state.set_state("make_post:get_post_template")
    await state.update_data(
        thread_id=None
    )
    await callback.message.delete()
    await get_template_message(callback.message)


@router.callback_query(StateFilter("make_post:thread_id"), F.data == "with_thread_id")
async def get_thread_id(callback: types.CallbackQuery, state: FSMContext):

    await state.set_state("make_post:get_thread_id")
    await callback.message.delete()
    await get_thread_id_message(callback.message)


@router.message(StateFilter("make_post:get_thread_id"))
async def get_template_post(message: types.Message, state: FSMContext):

    await state.set_state("make_post:get_post_template")
    thread_id = message.text

    if not thread_id.isdigit():

        await message.answer(
            text="ID должен содержать только цифры.",
            reply_markup=button_menu()
        )
    else:

        await state.update_data(
            thread_id=int(thread_id)
        )
        try:
            await message.bot.delete_message(
                chat_id=message.chat.id,
                message_id=(await get_msg_to_delete(user_id=message.from_user.id))
            )
        except:
            pass

        await get_template_message(message)


@router.message(StateFilter("make_post:get_post_template"))
async def accept_fast_post(message: types.Message, state: FSMContext):

    await state.set_state("make_post:access_fast_post")
    data_state = await state.get_data()
    await state.update_data(
        message_post_id=message.message_id,
        reply_markup=message.reply_markup.model_dump() if message.reply_markup else None
    )
    await message.bot.copy_message(
        chat_id=message.chat.id,
        from_chat_id=message.chat.id,
        message_id=message.message_id,
        reply_markup=message.reply_markup.model_dump() if message.reply_markup else None
    )

    await message.answer(
        f"""
☝️Вот так выглядит ваш пост.
Название канала: {data_state["group_name"]}
Сделать пост?""",
        reply_markup=get_post_confirm_key()
    )


# Отказ от поста
@router.callback_query(StateFilter("make_post:access_fast_post"), F.data == "unconfirm_fp")
async def get_new_template_fast_post(callback: types.CallbackQuery, state: FSMContext):

    await state.set_state("make_post:get_post_template")
    await callback.message.delete()
    await get_template_message(callback.message)


@router.callback_query(StateFilter("make_post:access_fast_post"), F.data == "confirm_fp")
async def make_fast_post(callback: types.CallbackQuery, state: FSMContext):

    data_state = await state.get_data()

    asyncio.create_task(
        post_task(
            channel_name=data_state["group_name"],
            channel_id=data_state["group_id"],
            thread_id=data_state["thread_id"],
            message_id=data_state["message_post_id"],
            user_id=callback.from_user.id,
            reply_markup=data_state["reply_markup"],
            bot=callback.bot
        )
    )
    await callback.message.delete()
    # await callback.message.answer(
    #     text="Пост скоро опубликуется.",
    #     reply_markup=button_menu()
    # )
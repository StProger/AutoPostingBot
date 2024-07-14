from aiogram import Router, F, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from bot.database.models.groups import Groups
from bot.keyboards import button_menu, get_fast_post_confirm_key
from bot.service.misc.misc_messages import choose_channel_message, ask_thread_id_message, get_template_message, \
    get_thread_id_message, get_time_public_post_message

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

    await state.set_state("plan_post:get_time_post")
    thread_id = message.text

    if not thread_id.isdigit():

        await message.answer(
            text="ID должен содержать только цифры.",
            reply_markup=button_menu()
        )
    else:

        await state.update_data(
            thread_id=int(thread_id),
            selected_time=0
        )
        # try:
        #     await message.bot.delete_message(
        #         chat_id=message.chat.id,
        #         message_id=(await get_msg_to_delete(user_id=message.from_user.id))
        #     )
        # except:
        #     pass

        await get_time_public_post_message(message)

        # await get_template_message(message)


@router.callback_query(StateFilter("plan_post:get_time_post"), F.data == "accept_time")
async def get_template_post(callback: types.CallbackQuery, state: FSMContext):

    await state.set_state("plan_post:get_post_template")

    await callback.message.delete()
    await get_template_message(callback.message)


@router.message(StateFilter("plan_post:get_post_template"))
async def accept_fast_post(message: types.Message, state: FSMContext):

    await state.set_state("plan_post:access_post")

    await state.update_data(
        message_post_id=message.message_id,
        reply_markup=message.reply_markup.dict() if message.reply_markup else None
    )
    await message.bot.copy_message(
        chat_id=message.chat.id,
        from_chat_id=message.chat.id,
        message_id=message.message_id
    )

    await message.answer(
        f"""
    ☝️Вот так выглядит ваш пост.

    Запланировать пост?""",
        reply_markup=get_fast_post_confirm_key()
    )

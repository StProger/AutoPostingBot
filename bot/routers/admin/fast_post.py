from aiogram import Router, F, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from bot.database.models.groups import Groups
from bot.service.misc.misc_messages import fast_post_choose_channel, fast_post_ask_thread_id, fast_post_get_thread_id, \
    fast_post_get_template

router = Router()


@router.callback_query(F.data == "make_post")
async def choose_channel(callback: types.CallbackQuery, state: FSMContext):

    await state.set_state("make_post:choose_channel")
    groups = Groups.select()

    await callback.message.delete()
    await fast_post_choose_channel(callback.message, groups)


@router.callback_query(StateFilter("make_post:choose_channel"), F.data.startswith("channel_fp_"))
async def ask_thread_id(callback: types.CallbackQuery, state: FSMContext):

    await state.set_state("make_post:thread_id")
    await callback.message.delete()

    group = Groups.get(id=int(callback.data.split("_")[-1]))

    await state.update_data(
        group_id=group.group_id,
        group_name=group.name
    )

    await fast_post_ask_thread_id(callback.message)


@router.callback_query(StateFilter("make_post:thread_id"), F.data == "fast_post_no_thread_id")
async def get_template_post(callback: types.CallbackQuery, state: FSMContext):

    await state.set_state("make_post:get_post_template")
    await state.update_data(
        thread_id=None
    )
    await callback.message.delete()
    await fast_post_get_template(callback.message)


@router.callback_query(StateFilter("make_post:thread_id"), F.data == "fast_post_with_thread_id")
async def get_thread_id(callback: types.CallbackQuery, state: FSMContext):

    await state.set_state("make_post:get_thread_id")
    await callback.message.delete()
    await fast_post_get_thread_id(callback.message)


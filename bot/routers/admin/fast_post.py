from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from bot.database.models.groups import Groups
from bot.service.misc.misc_messages import fast_post_choose_channel

router = Router()


@router.callback_query(F.data == "make_post")
async def choose_channel(callback: types.CallbackQuery, state: FSMContext):

    await state.set_state("make_post:choose_channel")
    groups = Groups.select()

    await callback.message.delete()
    await fast_post_choose_channel(callback.message, groups)

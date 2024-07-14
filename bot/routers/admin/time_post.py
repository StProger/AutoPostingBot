from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext

from bot.keyboards import select_time_post

router = Router()


@router.callback_query(F.data.startswith('plus') | F.data.startswith('minus'))
async def change_time_post(callback: types.CallbackQuery, state: FSMContext):
    data_state = await state.get_data()

    selected_time = data_state["selected_time"]

    if callback.data.startswith('minus'):

        if selected_time == 0:

            await callback.answer("Нельзя вычесть.")
        else:

            selected_time -= 1
            await state.update_data(
                selected_time=selected_time
            )

    else:

        selected_time += 1
        await state.update_data(
            selected_time=selected_time
        )

    await callback.message.edit_reply_markup(
        reply_markup=select_time_post(selected_hours=selected_time)
    )

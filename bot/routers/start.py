from aiogram import Router, F, types
from aiogram.filters.command import CommandStart
from aiogram.fsm.context import FSMContext

from bot.service.misc.misc_messages import start_message

router = Router()


@router.message(CommandStart())
async def start_handler(message: types.Message, state: FSMContext):

    await state.clear()
    await start_message(message, message.bot)


@router.callback_query(F.data == "menu")
async def menu_callback(callback: types.CallbackQuery, state: FSMContext):

    await state.clear()
    await callback.message.delete()
    await start_message(callback.message, callback.bot)
from aiogram import Router, F, types
from aiogram.filters.command import Command, CommandObject

from bot.database.api import add_admin_to_db

router = Router()


@router.message(Command("add_admin"))
async def add_admin(message: types.Message, command: CommandObject):

    if command.args is None:

        await message.delete()
        await message.answer("Введите ID.\nПример команды /add_admin 1234567")
    elif (command.args is not None) and (not (command.args.isdigit())):

        await message.delete()
        await message.answer("ID должно содержать только цифры.\n"
                             "Пример: /add_admin 1234567")
    else:

        await add_admin_to_db(tg_id=int(command.args))
        await message.delete()
        await message.answer("Администратор добавлен✅")

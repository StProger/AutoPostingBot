from aiogram import Router, types
from aiogram.filters.command import Command, CommandObject

from bot.database.api import delete_admin_from_db

router = Router()


@router.message(Command("delete_admin"))
async def add_admin(message: types.Message, command: CommandObject):

    if command.args is None:

        await message.delete()
        await message.answer("Введите ID.\nПример команды /delete_admin 1234567")
    elif (command.args is not None) and (not (command.args.isdigit())):

        await message.delete()
        await message.answer("ID должно содержать только цифры.\n"
                             "Пример: /delete_admin 1234567")
    else:

        await delete_admin_from_db(tg_id=int(command.args))
        await message.delete()
        await message.answer("Администратор удалён✅")

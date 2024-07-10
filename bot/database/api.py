from bot.database.models.admins import Admins


async def get_admins():

    admins = Admins.select()

    return [admin.tg_id for admin in admins]


async def add_admin_to_db(tg_id: int):

    Admins.insert(tg_id=tg_id).execute()


async def delete_admin_from_db(tg_id: int):

    query = Admins.delete().where(Admins.tg_id == tg_id)
    query.execute()
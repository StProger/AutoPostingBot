from bot.database.models.admins import Admins
from bot.database.models.groups import Groups


async def get_admins():

    admins = Admins.select()

    return [admin.tg_id for admin in admins]


async def add_admin_to_db(tg_id: int):

    Admins.insert(tg_id=tg_id).execute()


async def delete_admin_from_db(tg_id: int):

    query = Admins.delete().where(Admins.tg_id == tg_id)
    query.execute()


async def add_group_to_db(group_name: str, group_id: int):

    Groups.insert(name=group_name,
                  group_id=group_id).execute()


async def delete_group_from_db(group_id: int):

    query = Groups.delete().where(Groups.group_id == group_id)
    query.execute()
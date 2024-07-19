from bot.database.models.admins import Admins
from bot.database.models.groups import Groups
from bot.database.models.tasks_posts import TasksPosts


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


async def add_task(
        channel_name,
        channel_id,
        thread_id,
        message_id,
        user_id
):

    query = TasksPosts.insert(
        channel_name=channel_name,
        channel_id=channel_id,
        thread_id=thread_id,
        message_id=message_id,
        user_id=user_id
    )
    return query.execute()


async def update_task(task_id: int, job_id: str):

    query = TasksPosts.update(task_id=job_id).where(TasksPosts.id == task_id)
    query.execute()


async def delete_task(task_id):

    query = TasksPosts.delete().where(TasksPosts.id == task_id)
    query.execute()
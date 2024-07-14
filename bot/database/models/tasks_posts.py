from peewee import *

from bot.database.engine import BaseModel


class TasksPosts(BaseModel):

    class Meta:
        db_table = 'tasks_posts'

    id = BigIntegerField(primary_key=True)

    task_id = TextField(null=False)
    channel_name = TextField(null=False)
    channel_id = BigIntegerField()
    thread_id = BigIntegerField(null=True)
    message_id = BigIntegerField()
    user_id = BigIntegerField()

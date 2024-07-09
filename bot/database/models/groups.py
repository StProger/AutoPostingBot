from peewee import *

from bot.database.engine import BaseModel


class Groups(BaseModel):

    class Meta:

        db_table = "groups"

    id = IntegerField(primary_key=True)

    group_id = BigIntegerField()

    name = TextField()

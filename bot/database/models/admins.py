from bot.database.engine import BaseModel
from peewee import *


class Admins(BaseModel):

    class Meta:

        db_table = 'admins'

    id = IntegerField(primary_key=True)

    tg_id = BigIntegerField(unique=True)

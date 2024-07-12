from aiogram import F, Router, Bot, types
from aiogram.filters import StateFilter
from aiogram.filters.chat_member_updated import \
    ChatMemberUpdatedFilter, IS_NOT_MEMBER, MEMBER, ADMINISTRATOR
from aiogram.types import ChatMemberUpdated

from bot.database.api import add_group_to_db

router = Router()
router.my_chat_member.filter(F.chat.type.in_({"group", "supergroup"}))


@router.my_chat_member(
    ChatMemberUpdatedFilter(
        member_status_changed=IS_NOT_MEMBER >> ADMINISTRATOR
    ),
    StateFilter("*")
)
async def bot_added_as_admin(event: ChatMemberUpdated):
    print("Зашёл")
    await add_group_to_db(group_name=event.chat.title, group_id=event.chat.id)
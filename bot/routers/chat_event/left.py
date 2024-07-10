from aiogram import F, Router
from aiogram.filters.chat_member_updated import \
    ChatMemberUpdatedFilter, IS_NOT_MEMBER, MEMBER, ADMINISTRATOR
from aiogram.fsm.context import FSMContext
from aiogram.types import ChatMemberUpdated

from bot.database.api import delete_group_from_db


router = Router()
router.my_chat_member.filter(F.chat.type.in_({"group", "supergroup"}))


@router.my_chat_member(
    ChatMemberUpdatedFilter(
        member_status_changed=ADMINISTRATOR >> IS_NOT_MEMBER
    )
)
async def bot_deleted_as_admin(event: ChatMemberUpdated, state: FSMContext):

    await delete_group_from_db(event.chat.id)


@router.my_chat_member(
    ChatMemberUpdatedFilter(
        member_status_changed=MEMBER >> IS_NOT_MEMBER
    )
)
async def bot_deleted_as_member(event: ChatMemberUpdated):

    await delete_group_from_db(event.chat.id)

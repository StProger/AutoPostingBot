from typing import Union

from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery


class ChatTypeFilter(BaseFilter):
    def __init__(self, chat_type: Union[str, list]):
        self.chat_type = chat_type

    async def __call__(self, update: CallbackQuery | Message) -> bool:
        if isinstance(self.chat_type, str):

            if isinstance(update, Message):
                return update.chat.type == self.chat_type
            else:
                return update.message.chat.type == self.chat_type
        else:
            if isinstance(update, Message):
                return update.chat.type in self.chat_type
            else:
                return update.message.chat.type in self.chat_type

from bot.service.redis_serv import redis_pool


async def set_msg_to_delete(user_id: int, message_id: int) -> None:
    """ Установка сообщения на удаление (пользователю) """
    await redis_pool.set(f"{user_id}:msg:id", message_id)


async def get_msg_to_delete(user_id: int) -> int:
    """ Получение сообщения, которое надо удалить у пользователя """
    return await redis_pool.get(f"{user_id}:msg:id")

from fastapi import HTTPException

from ..settings import AppConfig


async def get_client(user_id: str, client_id: str):
    client = await AppConfig.client_dao.get_client(user_id, client_id)
    if client:
        return client
    else:
        raise HTTPException(status_code=404, detail="Client not found")

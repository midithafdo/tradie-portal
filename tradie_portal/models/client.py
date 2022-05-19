import datetime

from pydantic import BaseModel


class Client(BaseModel):
    id: str
    name: str
    contact_no: str
    tradie_id: str
    create_dt: datetime.datetime

import datetime
from typing import List, Optional

from pydantic import BaseModel


class Note(BaseModel):
    id: str
    create_dt: datetime.datetime
    job_id: str
    tradie_id: str
    description: str


class NotesResponse(BaseModel):
    count: int
    jobs: Optional[List[Note]]

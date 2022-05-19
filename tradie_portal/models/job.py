import datetime
from enum import Enum
from pydantic import BaseModel
from typing import List, Optional


class JobStatuses(str, Enum):
    SCHEDULED = "scheduled"
    ACTIVE = "active"
    INVOICING = "invoicing"
    TO_PRICED = "to-priced"
    COMPLETED = "completed"


class Job(BaseModel):
    id: str
    tradie_id: str
    status: JobStatuses
    create_dt: datetime.datetime
    client_id: str
    note_ids: Optional[List[str]]


class JobsResponse(BaseModel):
    count: int
    jobs: Optional[List[Job]]

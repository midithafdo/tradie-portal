from dataclasses import dataclass
from enum import Enum
from pydantic import BaseModel
from typing import List, Optional

from fastapi import Depends

from tradie_portal.models.job import JobStatuses
from utils.helpers import string_param


class JobsSortEnum(str, Enum):
    ID_ASC = "id"
    ID_DESC = "-id"
    CREATED_ASC = "created"
    CREATED_DESC = "-created"


@dataclass
class SortParams:
    sort: Optional[List[str]] = Depends(
        string_param("sort", multi=True, enum=JobsSortEnum, default=JobsSortEnum.CREATED_ASC.value)
    )


@dataclass
class JobFilterParams:
    job_id: Optional[List[str]] = Depends(string_param("job_id", multi=True))
    status: Optional[List[str]] = Depends(string_param("status", multi=True, enum=JobStatuses))
    client_id: Optional[List[str]] = Depends(string_param("client_id", multi=True))


class JobUpdate(BaseModel):
    status: JobStatuses

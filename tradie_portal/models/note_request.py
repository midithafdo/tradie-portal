from pydantic import BaseModel


class CreateNote(BaseModel):
    description: str

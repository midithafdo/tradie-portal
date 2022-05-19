import uuid
from datetime import datetime

from fastapi import HTTPException

from tradie_portal.models.note_request import CreateNote
from tradie_portal.models.note import Note, NotesResponse
from tradie_portal.models.shared import PaginationParams
from ..settings import AppConfig


async def create_note(user_id: str, job_id: str, source_note: CreateNote):
    job = await AppConfig.job_dao.get_job(user_id, job_id)
    if job:
        # TODO: Need to replace this with a proper ID generator
        note_id = str(uuid.uuid4())
        note = Note(
            id=note_id,
            create_dt=datetime.utcnow(),
            job_id=job_id,
            tradie_id=user_id,
            description=source_note.description
        )
        is_created = await AppConfig.note_dao.create_note(note_id, note)
        if not is_created:
            raise HTTPException(status_code=400, detail="Could not create Note")
    else:
        raise HTTPException(status_code=404, detail="Job not found")


async def get_notes(user_id: str, job_id: str, pagination: PaginationParams):
    count, notes = await AppConfig.note_dao.search_notes(user_id, job_id, pagination)
    return NotesResponse(
        count=count,
        jobs=notes
    )


async def update_note(user_id: str, note_id: str, note_update: CreateNote):
    note = await AppConfig.note_dao.get_note(user_id, note_id)
    if note:
        note.description = note_update.description
        is_updated = await AppConfig.note_dao.update_note(note_id, note)
        if not is_updated:
            raise HTTPException(status_code=400, detail="Could not update Note")
    else:
        raise HTTPException(status_code=404, detail="Note not found")

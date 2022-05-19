from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import HTMLResponse

from tradie_portal.models.job import Job, JobsResponse
from tradie_portal.models.job_request import JobFilterParams, JobUpdate, SortParams
from tradie_portal.models.client import Client
from tradie_portal.models.note import NotesResponse
from tradie_portal.models.note_request import CreateNote
from tradie_portal.models.shared import PaginationParams
from utils.auth_mock import create_access_token, Token, get_current_active_user

from ..services import job as JobService
from ..services import note as NoteService
from ..services import client as ClientService

router = APIRouter()


@router.get(
    path="/jobs",
    response_model=JobsResponse,
    summary="Retrieve list of jobs for the User",
)
async def get_jobs(
        filter_params: JobFilterParams = Depends(),
        pagination: PaginationParams = Depends(),
        sort: SortParams = Depends(),
        current_user_id: str = Depends(get_current_active_user)
):
    return await JobService.search_job(current_user_id, filter_params, pagination, sort)


@router.get(
    path="/jobs/{job_id}",
    response_model=Job,
    summary="Retrieve a job",
)
async def get_job(
        job_id: str,
        current_user_id: str = Depends(get_current_active_user)
):
    return await JobService.get_job(current_user_id, job_id)


@router.put(
    path="/jobs/{job_id}",
    response_class=HTMLResponse,
    summary="Update job",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def update_job_data(
        job_id: str,
        job_update: JobUpdate,
        current_user_id: str = Depends(get_current_active_user)
):
    await JobService.update_job(current_user_id, job_id, job_update)


@router.post(
    path="/notes/{job_id}",
    response_class=HTMLResponse,
    summary="Create note for a job",
    status_code=status.HTTP_201_CREATED,
)
async def crate_note(
        job_id: str,
        note: CreateNote,
        current_user_id: str = Depends(get_current_active_user)
):
    await NoteService.create_note(current_user_id, job_id, note)


@router.get(
    path="/notes/{job_id}",
    response_model=NotesResponse,
    summary="Retrieve list of notes for a Job",
)
async def get_notes(
        job_id: str,
        pagination: PaginationParams = Depends(),
        current_user_id: str = Depends(get_current_active_user)
):
    return await NoteService.get_notes(current_user_id, job_id, pagination)


@router.put(
    path="/notes/{note_id}",
    response_class=HTMLResponse,
    summary="Update Note",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def update_note_data(
        note_id: str,
        note: CreateNote,
        current_user_id: str = Depends(get_current_active_user)
):
    await NoteService.update_note(current_user_id, note_id, note)


@router.get(
    path="/clients/{client_id}",
    response_model=Client,
    summary="Retrieve a client",
)
async def get_client(
        client_id: str,
        current_user_id: str = Depends(get_current_active_user)
):
    return await ClientService.get_client(current_user_id, client_id)


@router.get(
    "/token",
    response_model=Token,
    summary="Mock endpoint to get a JWT token for Auth",
)
async def login_for_access_token(user_id: str):
    access_token = create_access_token(user_id)

    return {"access_token": access_token, "token_type": "bearer"}

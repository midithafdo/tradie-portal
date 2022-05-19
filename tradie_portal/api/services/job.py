from fastapi import HTTPException

from tradie_portal.models.job import JobsResponse
from tradie_portal.models.job_request import JobFilterParams, JobUpdate, SortParams
from tradie_portal.models.shared import PaginationParams

from ..settings import AppConfig


async def search_job(user_id: str, filter_params: JobFilterParams, pagination: PaginationParams, sort: SortParams):
    count, jobs = await AppConfig.job_dao.search_jobs(user_id, filter_params, pagination, sort)
    return JobsResponse(
        count=count,
        jobs=jobs
    )


async def get_job(user_id: str, job_id: str):
    job = await AppConfig.job_dao.get_job(user_id, job_id)
    if job:
        return job
    else:
        raise HTTPException(status_code=404, detail="Job not found")


async def update_job(user_id: str, job_id: str, job_update: JobUpdate):
    job = await AppConfig.job_dao.get_job(user_id, job_id)
    if job:
        job.status = job_update.status
        is_updated = await AppConfig.job_dao.update_job(job_id, job)
        if not is_updated:
            raise HTTPException(status_code=400, detail="Could not update Job")
    else:
        raise HTTPException(status_code=404, detail="Job not found")

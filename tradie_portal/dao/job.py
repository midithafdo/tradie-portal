import logging
from typing import List
from elasticsearch import AsyncElasticsearch

from tradie_portal.models.job import Job
from tradie_portal.models.job_request import JobFilterParams, SortParams
from tradie_portal.models.shared import PaginationParams
from .shared import _get_pagination_params

log = logging.getLogger(__name__)

SORT_PARAMS_ES_MAPPING = {
    "id": {"id": {"order": "asc"}},
    "-id": {"id": {"order": "desc"}},
    "created": {"create_dt": {"order": "asc"}},
    "-created": {"create_dt": {"order": "desc"}},
}


def _get_sort_param(sort: SortParams) -> dict:
    sort_search_list = [SORT_PARAMS_ES_MAPPING[sort_list_item] for sort_list_item in sort.sort]

    sort_list = sort.sort

    if not sort_list:
        return {}
    return {"sort": sort_search_list}


def _get_job_search_filters(user_id: str, filter_params: JobFilterParams) -> List[dict]:
    filters = [
        {"term": {"tradie_id": user_id}}
    ]

    if filter_params.job_id:
        filters.append({"terms": {"_id": filter_params.job_id}})

    if filter_params.status:
        filters.append({"terms": {"status": filter_params.status}})

    if filter_params.client_id:
        filters.append({"terms": {"client_id": filter_params.client_id}})

    return filters


def build_job_search_query(user_id, filter_params: JobFilterParams, pagination: PaginationParams, sort: SortParams):
    search_query: dict
    filters = []
    if filter_params:
        filters += _get_job_search_filters(user_id, filter_params)

    search_query = {"query": {"bool": {
        "filter": filters
    }}}

    if pagination:
        search_query.update(**_get_pagination_params(pagination))
    if sort:
        search_query.update(**_get_sort_param(sort))

    log.debug("Job search query: %s", search_query)

    return search_query


class JobDAO:
    def __init__(self, es_client: AsyncElasticsearch, index: str):
        self.es_client = es_client
        self.index = index

    async def search_jobs(self, user_id: str, filter_params: JobFilterParams, pagination: PaginationParams,
                          sort: SortParams):
        search_query = build_job_search_query(user_id, filter_params, pagination, sort)
        response = await self.es_client.search(index=self.index, body=search_query)

        return response["hits"]["total"]["value"], [
            Job.parse_obj(hit["_source"]) for hit in response["hits"]["hits"]
        ]

    async def get_job(self, user_id: str, job_id: str):
        search_query = {
            "query": {"bool": {"filter": [{"term": {"tradie_id": user_id}}, {"term": {"_id": job_id}}]}}}
        response = await self.es_client.search(index=self.index, body=search_query)

        if response["hits"]["total"]["value"] > 0:
            return Job.parse_obj(response["hits"]["hits"][0]["_source"])
        return None

    async def update_job(
            self, job_id: str, updated_job: Job,
    ) -> bool:
        try:
            await self.es_client.update(
                self.index,
                refresh="wait_for",
                id=job_id,
                body={"doc": dict(updated_job)},
            )
            return True
        except:
            return False

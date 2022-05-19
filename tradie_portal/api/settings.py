from elasticsearch import AsyncElasticsearch

from tradie_portal.dao.job import JobDAO
from tradie_portal.dao.note import NoteDAO
from tradie_portal.dao.client import ClientDAO


class AppConfig:
    es_client: AsyncElasticsearch
    job_dao: JobDAO
    note_dao: NoteDAO
    client_dao: ClientDAO


def setup_config(settings: dict):
    es_client = AsyncElasticsearch(hosts=settings["es_host"])

    AppConfig.job_dao = JobDAO(
        es_client=es_client,
        index=settings["job_index"]
    )
    AppConfig.note_dao = NoteDAO(
        es_client=es_client,
        index=settings["note_index"]
    )
    AppConfig.client_dao = ClientDAO(
        es_client=es_client,
        index=settings["client_index"]
    )

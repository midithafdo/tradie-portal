import logging

from elasticsearch import AsyncElasticsearch

from tradie_portal.models.note import Note
from tradie_portal.models.shared import PaginationParams
from .shared import _get_pagination_params

log = logging.getLogger(__name__)


class NoteDAO:
    def __init__(self, es_client: AsyncElasticsearch, index: str):
        self.es_client = es_client
        self.index = index

    async def create_note(
            self, note_id: str, note: Note,
    ) -> bool:
        try:
            await self.es_client.create(
                self.index,
                refresh="wait_for",
                id=note_id,
                body=note.dict()
            )
            return True
        except:
            return False

    async def search_notes(self, user_id: str, job_id: str, pagination: PaginationParams):
        search_query = {"query": {"bool": {"filter": [{"term": {"tradie_id": user_id}}, {"term": {"job_id": job_id}}]}}}
        if pagination:
            search_query.update(**_get_pagination_params(pagination))

        log.debug("Note search query: %s", search_query)

        response = await self.es_client.search(index=self.index, body=search_query)

        return response["hits"]["total"]["value"], [
            Note.parse_obj(hit["_source"]) for hit in response["hits"]["hits"]
        ]

    async def get_note(self, user_id: str, note_id: str):
        search_query = {"query": {"bool": {"filter": [{"term": {"tradie_id": user_id}}, {"term": {"_id": note_id}}]}}}
        response = await self.es_client.search(index=self.index, body=search_query)

        if response["hits"]["total"]["value"] > 0:
            return Note.parse_obj(response["hits"]["hits"][0]["_source"])
        return None

    async def update_note(
            self, note_id: str, updated_note: Note,
    ) -> bool:
        try:
            await self.es_client.update(
                self.index,
                refresh="wait_for",
                id=note_id,
                body={"doc": updated_note.dict()},
            )
            return True
        except:

            return False

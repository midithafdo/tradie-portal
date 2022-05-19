from elasticsearch import AsyncElasticsearch

from tradie_portal.models.client import Client


class ClientDAO:
    def __init__(self, es_client: AsyncElasticsearch, index: str):
        self.es_client = es_client
        self.index = index

    async def get_client(self, user_id: str, client_id: str):
        search_query = {"query": {"bool": {"filter": [{"term": {"tradie_id": user_id}}, {"term": {"_id": client_id}}]}}}
        response = await self.es_client.search(index=self.index, body=search_query)

        if response["hits"]["total"]["value"] > 0:
            return Client.parse_obj(response["hits"]["hits"][0]["_source"])
        return None

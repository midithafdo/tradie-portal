# Tradie Portal Backend

Tradie Portal Backend provides a Public API for the `tradie-portal-ui`(front-end).
This project uses FastAPI(Python API Framework) and Elasticsearch as it's primary data store.


## API Authorization
A mock end-point(to retrieve a Bearer Token) has been added to the api for testing the endpoints.

### GET /token
Retrieve a JWT token for the given `user_id`

Query params:
```
user_id
```

Responses:
```
200: Successful Response
```

## Jobs

### GET /jobs
Retrieve list of jobs for the User

Query params:
```
job_id
status
client_id
offset
limit
sort
```

Responses:
```
200: Successful Response
401: Authorization required
```

### GET /jobs/<job_id>
Retrieve a job

Path params:
```
job_id
```

Responses:
```
200: Successful Response
401: Authorization required
```

### PUT /jobs/<job_id>
Update job

Path params:
```
job_id
```

Request body:
```
status: String
```

Responses:
```
204: Successful Response
404: Job not found
400: Bad request
401: Authorization required
```


## Notes

### POST /notes/<job_id>
Create note for a job

Path params:
```
job_id
```

Request body:
```
description: String
```

Responses:
```
201: Successful Response
404: Job not found
400: Bad request
401: Authorization required
```

### GET /notes/<job_id>
Retrieve list of notes for a Job

Path params:
```
job_id
```

Query params:
```
offset
limit
```

Responses:
```
200: Successful Response
401: Authorization required
```

### PUT /notes/<note_id>
Update Note

Path params:
```
note_id
```

Request body:
```
description: String
```

Responses:
```
204: Successful Response
404: Note not found
400: Bad request
401: Authorization required
```

## Clients
### GET /clients/<client_id>
Retrieve a client

Path params:
```
client_id
```

Responses:
```
200: Successful Response
404: Client not found
401: Authorization required
```

## Setting up development environment

Install dependencies using `pip`.

```
> pip install -r requirements/base.txt
```

Sample `docker-compose-example.yaml` is included in project root to create a local `docker-compose.yaml` file.
```
> docker-compose build # build project
> docker-compose up elasticsearch # Start Elasticsearch
> docker-compose up api # Start API
```

Open API docs will be available upon starting the API
`BASE_URL/openapi.json`

### Setting up Elasticsearch Indices
Use the mapping files in `/tradie_portal/dao/mappings/` to create the indices. More details can be found in Elasticsearch docs.

[Elasticsearch Docs](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-create-index.html)

### Unit Tests

`TBA`

### Integration Tests

`TBA`


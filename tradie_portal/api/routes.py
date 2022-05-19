from fastapi import FastAPI

from .v1 import api_router as v1_router


def set_router(app: FastAPI):
    app.include_router(v1_router.resolve_routes())

from fastapi import APIRouter

from .routes import router as tradie_portal_router


def resolve_routes():
    router = APIRouter()

    router.include_router(tradie_portal_router, prefix="/tradie-portal", tags=["tradie-portal"])

    return router

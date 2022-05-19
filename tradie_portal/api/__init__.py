import logging
import uvicorn  # ASGI server
from fastapi import FastAPI

from .routes import set_router
from .settings import setup_config

log = logging.getLogger(__name__)


def start_app(options:dict):
    try:
        app = configure_app(options)
        uvicorn.run(app, host="0.0.0.0", port=options["api_port"], access_log=False)
    except Exception:
        log.exception("Unrecoverable exception encountered. Exiting.")


def configure_app(options:dict):
    setup_config(options)
    app = construct_api(options)

    return app


def construct_api(options: dict):
    app = FastAPI(openapi_url=options["openapi_url"])
    set_router(app)

    @app.get("/status")
    async def status():
        return "OK"

    return app

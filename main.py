import click
import logging

log = logging.getLogger(__name__)


@click.group()
def main():
    pass


@click.command()
@click.option("--es-host", required=True, help="ES Hosts")
@click.option("--job-index", required=True, help="Job ES index")
@click.option("--note-index", required=True, help="Note ES index")
@click.option("--client-index", required=True, help="Client ES index")
@click.option("--api-port", "-p", default=8080, help="Port to serve API on (default=8080)")
@click.option("--openapi-url", default="/openapi.json", help="Open API URL (default=/openapi.json)")
def api(**options):
    from tradie_portal.api import start_app

    start_app(options)


main.add_command(api)


if __name__ == "__main__":
    error = None
    try:
        main(auto_envvar_prefix="notifications_backend".upper())
    except (KeyboardInterrupt, SystemExit) as e:
        log.info("Interrupted by %(interrupt)s", {"interrupt": type(e).__name__})
    except Exception as e:
        log.exception("Unrecoverable exception encountered. Exiting.")
        error = e

    log.info("Shutting down...")

    if error:
        exit(error)

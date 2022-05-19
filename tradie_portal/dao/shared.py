from tradie_portal.models.shared import PaginationParams


def _get_pagination_params(pagination: PaginationParams) -> dict:
    return {
        "from": pagination.offset,
        "size": pagination.limit,
    }

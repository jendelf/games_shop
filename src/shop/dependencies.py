from fastapi import Query
from .schemas import PageParams

def get_pagination_params(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100)
) -> PageParams:
    return PageParams(page=page, page_size=page_size)
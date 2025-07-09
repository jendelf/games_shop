from fastapi import Query
from schemas import PaginationParams

def get_pagination_params(limit: int = Query(20, ge=0, le=100, description="Number of elements on a page"),
                          offset: int = Query(0, ge=0, description="Shift for pagination"),
                           sort_by: str | None = Query(None),
                            search: str| None = Query(None) ) -> PaginationParams:
    return PaginationParams(limit=limit, offset=offset, sort_by=sort_by, search=search)
from typing import Annotated

from fastapi import Query, Depends
from pydantic import BaseModel


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(None, ge=1)]
    page_size: Annotated[int | None, Query(None, ge=1, lt=20)]


PaginationDep = Annotated[PaginationParams, Depends()]

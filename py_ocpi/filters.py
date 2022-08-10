from datetime import datetime

from fastapi import Query


def pagination_filters(
    date_from: datetime = Query(default=None),
    date_to: datetime = Query(default=datetime.now()),
    offset: int = Query(default=0),
    limit: int = Query(default=50),
):
    return {
        'date_from': date_from,
        'date_to': date_to,
        'offset': offset,
        'limit': limit,
    }

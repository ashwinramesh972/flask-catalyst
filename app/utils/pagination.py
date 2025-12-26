from flask import request
from typing import Type, List
from .response import success

def paginate(query, schema_class: Type):
    """
    Paginate any SQLAlchemy query with Pydantic schema
    Usage:
        return paginate(User.query, UserOut)
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    per_page = min(per_page, 100)  # prevent abuse

    paginated = query.paginate(page=page, per_page=per_page, error_out=False)

    # Convert each item to Pydantic model
    items = [schema_class.from_orm(item) for item in paginated.items]

    pagination_info = {
        "page": page,
        "per_page": per_page,
        "total": paginated.total,
        "pages": paginated.pages,
        "has_next": paginated.has_next,
        "has_prev": paginated.has_prev,
        "next_page": page + 1 if paginated.has_next else None,
        "prev_page": page - 1 if paginated.has_prev else None,
    }

    return success(
        data={
            "items": [item.model_dump() for item in items],
            "pagination": pagination_info
        },
        message="Data fetched successfully"
    )
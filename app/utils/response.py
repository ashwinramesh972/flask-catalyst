from flask import jsonify
from typing import Any, Dict, Optional

def success(
    data: Any = None,
    message: str = "Success",
    status_code: int = 200
) -> tuple:
    """Standard success response"""
    response = {
        "success": True,
        "message": message,
        "data": data or {}
    }
    return jsonify(response), status_code


def error(
    message: str = "An error occurred",
    status_code: int = 400,
    errors: Optional[Dict] = None
) -> tuple:
    """Standard error response"""
    response = {
        "success": False,
        "message": message,
        "errors": errors or {}
    }
    return jsonify(response), status_code


def paginated_response(query_result, pagination_info: dict) -> tuple:
    """For paginated endpoints"""
    return success(
        data={
            "items": [item.to_dict() for item in query_result.items],
            "pagination": pagination_info
        },
        message="Data fetched successfully"
    )
from flask import jsonify
from datetime import datetime

def api_response(status: str, data: dict, message: str = "", code: int = 200):
    response = {
        "status": status.lower(),  # "success" or "error"
        "message": message,
        "data": data or {},
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "code": code
    }
    return jsonify(response), code

# Shortcuts — easy to use
def success(data: dict = None, message: str = "Success", code: int = 200):
    return api_response("success", data or {}, message, code)

def error(data: dict = None, message: str = "An error occurred", code: int = 400):
    return api_response("error", data or {}, message, code)
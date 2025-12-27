import json
from datetime import datetime
from flask import has_request_context, request, g
from pathlib import Path
from pprint import pformat 


BASE_DIR = Path(__file__).resolve().parent.parent.parent
DEBUG_LOG_DIR = BASE_DIR / "instance" / "logs" / "debug"
DEBUG_LOG_DIR.mkdir(parents=True, exist_ok=True)

def debug_log(label: str, data):
    """
    Log any data for debugging — pretty-printed, with context.
    Usage:
        debug_log("Admin users", rows)
        debug_log("Request JSON", request.get_json())
        debug_log("JWT Identity", get_jwt_identity())
    """
    timestamp = datetime.utcnow().isoformat() + "Z"


    context = {}
    if has_request_context():
        context.update({
            "method": request.method if request else None,
            "path": request.path if request else None,
            "user_id": getattr(g, "user_id", "anonymous"),
            "ip": request.remote_addr if request else "unknown"
        })

    if isinstance(data, (list, dict, tuple)):
        pretty_data = pformat(data, indent=2, width=120)
    else:
        try:
            pretty_data = pformat(data.to_dict() if hasattr(data, 'to_dict') else str(data))
        except:
            pretty_data = repr(data)

    today = datetime.utcnow().strftime("%Y-%m-%d")
    log_file = DEBUG_LOG_DIR / f"{today}.log"

    entry = (
        f"[{timestamp}] DEBUG: {label}\n"
        f"Context: {json.dumps(context, ensure_ascii=False)}\n"
        f"Data:\n{pretty_data}\n"
        f"{'─' * 80}\n"
    )

    try:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(entry)
    except Exception as e:
        print(f"Failed to write debug log: {e}")




'''
debug_log("Your label/message here", your_data_here)

eg:
from app.utils.debug_logger import debug_log

debug_log("username", username)
'''
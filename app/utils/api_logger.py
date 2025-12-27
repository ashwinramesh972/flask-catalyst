import os
from datetime import datetime
from flask import request, has_request_context, g
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent  
INSTANCE_DIR = BASE_DIR / "instance"
LOG_DIR = INSTANCE_DIR / "logs" / "api_calls"


LOG_DIR.mkdir(parents=True, exist_ok=True)

def log_api_call(status_code: int, duration_ms: float):
    if not has_request_context():
        return

    today = datetime.utcnow().strftime("%Y-%m-%d")
    log_file = LOG_DIR / f"{today}.log"  

    user_id = getattr(g, 'user_id', 'anonymous')
    user_type = getattr(g, 'user_type', 'unknown')

    log_entry = (
        f"[{datetime.utcnow().isoformat()}Z] "
        f"{request.method} {request.path} → {status_code}\n"
        f"{{\n"
        f'  "user_id": "{user_id}",\n'
        f'  "user_type": "{user_type}",\n'
        f'  "duration_ms": {duration_ms:.2f},\n'
        f'  "ip": "{request.remote_addr}",\n'
        f'  "status": {status_code},\n'
        f'  "method": "{request.method}"\n'
        f"}}\n"
        f"────────────────────────────────────────────────────────────\n"
    )

    try:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(log_entry)
    except Exception as e:
        print(f"Failed to write API log: {e}")  



"""
from flask import current_app as app

# Info level (normal operations)
app.logger.info("User logged in successfully")

# Debug level (for development only)
app.logger.debug(f"Received data: {data}")

# Warning level
app.logger.warning("User tried invalid password 3 times")

# Error level
app.logger.error("Database connection failed")

# Critical level
app.logger.critical("Server is on fire!")


app.logger.info(f"User {user.id} ({user.username}) uploaded file {filename}")

app.logger.debug(f"JWT payload: {payload}")

app.logger.error(f"Upload failed for user {user_id}: {str(e)}")



"""
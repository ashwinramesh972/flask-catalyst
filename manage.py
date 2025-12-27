# python manage.py create_app "app_name"
import sys
from pathlib import Path
import argparse

PROJECT_ROOT = Path(__file__).parent
MODULES_DIR = PROJECT_ROOT / "app" / "modules"
API_INIT = PROJECT_ROOT / "app" / "api" / "__init__.py"


def create_app(module_name: str):
    if not module_name.isidentifier():
        print(f"❌ '{module_name}' is not a valid Python identifier")
        return

    module_path = MODULES_DIR / module_name

    if module_path.exists():
        print(f"❌ Module '{module_name}' already exists")
        return

    # ─────────────────────────────────────────────
    # 1. Create folder
    # ─────────────────────────────────────────────
    module_path.mkdir(parents=True)
    print(f"✅ Created app/modules/{module_name}")

    files = {
        "__init__.py": f"""from .routes import {module_name}_bp

__all__ = ["{module_name}_bp"]
""",

        "routes.py": f"""from flask import Blueprint
from .controllers import index

{module_name}_bp = Blueprint(
    "{module_name}",
    __name__,
    url_prefix="/{module_name}"
)

{module_name}_bp.route("", methods=["GET"])(index)
""",

        "controllers.py": f"""from flask import jsonify

def index():
    return jsonify({{"message": "Welcome to {module_name} module"}})
""",

        "models.py": f"""# {module_name.capitalize()} models
# Example:
# class {module_name.capitalize()}(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
pass
""",

        "schemas.py": f"""from pydantic import BaseModel

class {module_name.capitalize()}Out(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
"""
    }

    for filename, content in files.items():
        (module_path / filename).write_text(content)
        print(f"   • Created {filename}")

    # ─────────────────────────────────────────────
    # 2. Auto-register in api/__init__.py
    # ─────────────────────────────────────────────
    if not API_INIT.exists():
        print("❌ app/api/__init__.py not found")
        return

    lines = API_INIT.read_text().splitlines()

    import_line = f"from app.modules.{module_name} import {module_name}_bp"
    register_line = f"api_bp.register_blueprint({module_name}_bp)"

    # Insert import after last module import
    last_import = max(
        (i for i, l in enumerate(lines) if l.startswith("from app.modules.")),
        default=-1
    )

    if import_line not in lines:
        lines.insert(last_import + 1, import_line)

    # Insert register after last blueprint register
    last_register = max(
        (i for i, l in enumerate(lines) if "register_blueprint" in l),
        default=len(lines) - 1
    )

    if register_line not in lines:
        lines.insert(last_register + 1, register_line)

    API_INIT.write_text("\n".join(lines) + "\n")

    print(f" Registered {module_name}_bp in app/api/__init__.py")
    print(f"\n App '{module_name}' created successfully!")


# ─────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flask Catalyst Manager")
    parser.add_argument("command", choices=["create_app"])
    parser.add_argument("name", help="App name")

    args = parser.parse_args()

    if args.command == "create_app":
        create_app(args.name.lower())

import os
import secrets


BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    # Para manter sessões após reinícios, configure SECRET_KEY no ambiente.
    SECRET_KEY = os.environ.get("SECRET_KEY") or secrets.token_hex(32)
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///" + os.path.join(BASE_DIR, "instance", "database.db"),
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
    MAX_CONTENT_LENGTH = 4 * 1024 * 1024

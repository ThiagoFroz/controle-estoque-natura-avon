import os
import sys


path = "/home/thifroz/controle-estoque-natura-avon"

if path not in sys.path:
    sys.path.insert(0, path)

os.environ.setdefault("SECRET_KEY", "troque-esta-chave-no-pythonanywhere")

from app import app as application  # noqa: E402

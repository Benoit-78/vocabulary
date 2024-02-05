import os
import sys

REPO_NAME = 'vocabulary'
REPO_DIR = os.getcwd().split(REPO_NAME)[0] + REPO_NAME
sys.path.append(REPO_DIR)

from src.routers.user import user_router
from src.routers.interro import interro_router
from src.routers.guest import guest_router
from src.routers.database import database_router
from src.routers.dashboard import dashboard_router

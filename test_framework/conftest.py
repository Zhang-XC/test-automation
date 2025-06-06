import os
import uuid

import pytest

from backend_service.app import app
from common.database import init_db, get_db
from common.settings import FILE_PATH


@pytest.fixture(scope='session', autouse=True)
def cleanup_db():
    if os.path.exists(FILE_PATH["DATABASE"]):
        os.remove(FILE_PATH["DATABASE"])
    
    user_id = str(uuid.uuid4())

    init_db()

    with app.app_context():
        db = get_db()
        db.execute(
            "INSERT INTO users (user_id, username, password) VALUES (?, ?, ?)",
            [user_id, "testuser", "testpassword"]
        )
        db.commit()
        db.close()
    
    yield


@pytest.fixture(scope="session", autouse=True)
def cleanup_extract_yaml():
    with open(FILE_PATH['EXTRACT'], 'w') as f:
        f.truncate()
    yield
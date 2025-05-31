import os

import pytest

from common.database import init_db
from common.settings import FILE_PATH


@pytest.fixture(scope='session', autouse=True)
def cleanup_db():
    if os.path.exists(FILE_PATH["DATABASE"]):
        os.remove(FILE_PATH["DATABASE"])
    
    db = init_db()
    db.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        ["testuser", "testpassword"]
    )
    db.close()

    yield
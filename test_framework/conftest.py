import os

import pytest

from common.database import init_db, get_db
from common.settings import FILE_PATH


@pytest.fixture(scope='session', autouse=True)
def cleanup_db():
    if os.path.exists(FILE_PATH["DATABASE"]):
        os.remove(FILE_PATH["DATABASE"])
    
    init_db()
    db = get_db()
    db.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        ["testuser", "testpassword"]
    )
    db.commit()
    db.close()
    yield


@pytest.fixture(scope="session", autouse=True)
def cleanup_extract_yaml():
    with open(FILE_PATH['EXTRACT'], 'w') as f:
        f.truncate()
    yield
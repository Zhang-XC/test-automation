import sqlite3

from flask import g
from common.settings import FILE_PATH


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(FILE_PATH["DATABASE"])
        g.db.execute("PRAGMA foreign_keys = ON")
        g.db.row_factory = sqlite3.Row
    return g.db


def init_db():
    db = sqlite3.connect(FILE_PATH["DATABASE"])
    with open(FILE_PATH["SCHEMA"], 'r') as f:
        db.executescript(f.read())
    return db
import os
import sqlite3

from common.settings import FILE_PATH


def get_db():
    db = sqlite3.connect(FILE_PATH["DATABASE"])
    db.execute("PRAGMA foreign_keys = ON")
    db.row_factory = sqlite3.Row
    return db


def init_db():
    db = sqlite3.connect(FILE_PATH["DATABASE"])
    with open(FILE_PATH["SCHEMA"], 'r') as f:
        db.executescript(f.read())
import os
import sys


DIR_BASE = os.path.dirname(os.path.dirname(__file__))
sys.path.append(DIR_BASE)

DIR_REPORT = os.path.join(DIR_BASE, "report", "temp")

URL_HOST = "https://127.0.0.1:8888"

FILE_PATH = {
    "DATABASE": os.path.join(DIR_BASE, "database", "ecommerce.db"),
    "SCHEMA": os.path.join(DIR_BASE, "database", "schema.sql"),
    "EXTRACT": os.path.join(DIR_BASE, "test_framework", "data", "extracted.yaml"),
    "JUNIT_XML": os.path.join(DIR_BASE, "report", "results.xml"),
    "ENV_XML": os.path.join(DIR_BASE, "environment.xml"),
}
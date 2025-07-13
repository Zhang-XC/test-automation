import os
import sys
import logging


DIR_BASE = os.path.dirname(os.path.dirname(__file__))
sys.path.append(DIR_BASE)

DIR_REPORT = os.path.join(DIR_BASE, "report", "temp")
DIR_TESTCASE = os.path.join(DIR_BASE, "test_framework", "data")

URL_HOST = "http://0.0.0.0:8888"

API_TIMEOUT = 30

LOG_LEVEL = logging.DEBUG
STREAM_LEVEL = logging.WARNING

FILE_PATH = {
    "DATABASE": os.path.join(DIR_BASE, "backend_service", "database", "ecommerce.db"),
    "SCHEMA": os.path.join(DIR_BASE, "backend_service", "database", "schema.sql"),
    "EXTRACT": os.path.join(DIR_BASE, "test_framework", "data", "extracted.yaml"),
    "JUNIT_XML": os.path.join(DIR_BASE, "report", "results.xml"),
    "ENV_XML": os.path.join(DIR_BASE, "environment.xml"),
    "LOG": os.path.join(DIR_BASE, "logs"),
}
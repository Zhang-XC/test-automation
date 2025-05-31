import os
import sys


DIR_BASE = os.path.dirname(os.path.dirname(__file__))
sys.path.append(DIR_BASE)

FILE_PATH = {
    "DATABASE": os.path.join(DIR_BASE, "database/ecommerce.db"),
    "SCHEMA": os.path.join(DIR_BASE, "database/schema.sql"),
    "EXTRACT": os.path.join(DIR_BASE, "test_framework/data/extracted.yaml"),
}
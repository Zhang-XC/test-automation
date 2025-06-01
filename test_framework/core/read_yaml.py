import os
import json

import yaml

from test_framework.core.utils import Utils


def load_testcase(file: str):
    testcases = []
    with open(file, 'r') as f:
        data = yaml.safe_load(f)
    if isinstance(data, dict):
        data = [data]
    for item in data:
        common = item.get("common")
        for tc in item.get("testcases"):
            testcases.append({**common, **tc})
    return testcases


def resolve_placeholder(data: dict):
    str_data = json.dumps(data)
    
    for _ in range(str_data.count("${")):
        if "}" in str_data:
            start = str_data.index("$")
            end = str_data.index("}") + 1
            
            placeholder = str_data[start:end]
            func_name = str_data[start + 2:str_data.index("(")]
            params = str_data[str_data.index("(") + 1:str_data.index(")")]
            
            parsed_data = getattr(Utils, func_name)(*params.split(","))
            parsed_data = str(parsed_data)
            
            str_data = str_data.replace(placeholder, parsed_data)

    return json.loads(str_data)


def write_yaml(file: str, data: dict):
    if os.path.isfile(file):
        with open(file, "r") as f:
            existing_data = yaml.safe_load(f) or []
    else:
        existing_data = []
    existing_data.append(data)

    with open(file, "w") as f:
        yaml.safe_dump(existing_data, f)
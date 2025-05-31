import yaml


def load_testcase(file):
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


def resolve_placeholder():
    pass
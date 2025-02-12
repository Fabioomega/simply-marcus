import json
from pathlib import Path


class Environment:

    def __init__(self, path: str):
        with open(Path(path), encoding="utf-8") as file:
            self.env = json.load(file)

    def get(self, name, default=None):
        return self.env.get(name, default)

    def __getitem__(self, item):
        return self.env[item]

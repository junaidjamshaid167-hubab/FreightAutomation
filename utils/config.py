import json
from pathlib import Path


class Config:

    def __init__(self):
        self.file = Path("config/settings.json")

        with open(self.file, "r") as f:
            self.data = json.load(f)

    def get(self, key):
        return self.data.get(key)

    def set(self, key, value):
        self.data[key] = value

        with open(self.file, "w") as f:
            json.dump(self.data, f, indent=4)
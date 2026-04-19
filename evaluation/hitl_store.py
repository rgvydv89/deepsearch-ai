import json
import os


class HITLStore:
    def __init__(self, file_path="hitl_data.json"):
        self.file_path = file_path

    def save(self, data):
        existing = []

        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r") as f:
                    existing = json.load(f)
            except:
                existing = []

        existing.append(data)

        with open(self.file_path, "w") as f:
            json.dump(existing, f, indent=2)

    def load(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as f:
                return json.load(f)
        return []

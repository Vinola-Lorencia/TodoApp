import json
import os
class Storage:
    def __init__(self, filepath= "data/tasks.json"):
        self.filepath = filepath

    def load_tasks(self):
        if not os.path.exists(self.filepath):
            return []
        with open(self.filepath, "r") as file:
            return json.load(file)

    def save_tasks(self, tasks):
        with open(self.filepath, "w") as file:
            json.dump(tasks, file, indent=4)
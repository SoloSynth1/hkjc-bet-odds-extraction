import json
import os

from mergedeep import merge

class ComboWriter:

    def __init__(self, filepath):
        self.filepath = filepath
        self.previous_state = self.read_file()

    def read_file(self):
        if not os.path.exists(self.filepath):
            with open(self.filepath, 'w') as f:
                f.write('{}')
        with open(self.filepath, 'r') as f:
            previous_state = json.loads(f.read())
        return previous_state

    def write(self, json_obj):
        merge(self.previous_state, json_obj)
        with open(self.filepath, 'w') as f:
            f.write(json.dumps(self.previous_state))

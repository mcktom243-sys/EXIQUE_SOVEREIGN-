import pickle
import os

class Memory:
    def __init__(self, filename="tommy_memory.pkl"):
        self.path = os.path.expanduser(f"~/exique_package/vault/{filename}")
        self.data = {}
        if os.path.exists(self.path):
            self.load()

    def store(self, key, value):
        self.data[key] = value
        with open(self.path, 'wb') as f:
            pickle.dump(self.data, f)

    def load(self):
        try:
            with open(self.path, 'rb') as f:
                self.data = pickle.load(f)
        except EOFError:
            self.data = {}

    def retrieve(self, key):
        return self.data.get(key)


import pickle
import os

class Memory:
    def __init__(self):
        self.vault_path = os.path.expanduser("~/exique_package/vault/vault.pkl")
        self.data = {}

    def load_from_vault(self):
        if os.path.exists(self.vault_path):
            with open(self.vault_path, 'rb') as f:
                self.data = pickle.load(f)
            return True
        return False

    def save_to_vault(self):
        with open(self.vault_path, 'wb') as f:
            pickle.dump(self.data, f)

    def retrieve(self, key):
        return self.data.get(key, "Unknown")

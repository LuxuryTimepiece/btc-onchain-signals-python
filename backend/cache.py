class Cache:
    def __init__(self):
        self.data = {"price": 0.0, "active_addresses": 0}

    def set(self, data):
        self.data = data

    def get(self):
        return self.data
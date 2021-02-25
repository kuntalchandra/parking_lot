class Merchant:
    def __init__(self):
        self.name = None
        self.registered_at = None

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    @property
    def registered_at(self):
        return self._registered_at

    @registered_at.setter
    def registered_at(self, registered_at: str):
        self._registered_at = registered_at

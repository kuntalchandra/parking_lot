class ParkingLot:
    def __init__(self):
        self.id = None
        self.name = None
        self.area = None
        self.pin_code = None
        self.is_available = 0
        self.start_date = None
        self.slot_count = 0

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id: str):
        self._id = id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    @property
    def area(self):
        return self._area

    @area.setter
    def area(self, area: str):
        self._area = area

    @property
    def pin_code(self):
        return self._pin_code

    @pin_code.setter
    def pin_code(self, pin_code: str):
        self._pin_code = pin_code

    @property
    def is_available(self):
        return self._is_available

    @is_available.setter
    def is_available(self, is_available: int):
        self._is_available = is_available

    @property
    def start_date(self):
        return self._start_date

    @start_date.setter
    def start_date(self, start_date: str):
        self._start_date = start_date

    @property
    def slot_count(self):
        return self._slot_count

    @slot_count.setter
    def slot_count(self, slot_count: int):
        self._slot_count = slot_count

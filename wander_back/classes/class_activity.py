import datetime as dt

class Activity:
    def __init__(self, title: str, start_time: dt.time, end_time: dt.time, location: str, cost: int, notes: str):
        self._id = 0
        self._title = title
        self._start_time = start_time
        self._end_time = end_time
        self._location = location
        self._cost = cost
        self._notes = notes

    def __json__(self):
        return {
            'id': self._id, 
            'title': self._title,
            'start_time': self._start_time.strftime('%H:%M'),
            'end_time': self._end_time.strftime('%H:%M'),
            'location': self._location,
            'cost': float(self._cost),
            'notes': self._notes
        }

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self, value):
        if value is None:
            raise ValueError("Title not provided")

        self._title = value

    @property
    def start_time(self):
        return self._start_time
    
    @start_time.setter
    def start_time(self, value):
        if value is None:
            raise ValueError("Start time not provided")

        self._start_time = value
    
    @property
    def end_time(self):
        return self._end_time
    
    @end_time.setter
    def end_time(self, value):
        if value is None:
            raise ValueError("End time not provided")

        self._end_time = value
    
    @property
    def location(self):
        return self._location
    
    @location.setter
    def location(self, value):
        if value is None:
            raise ValueError("Location time not provided")

        self._location = value
    
    @property
    def cost(self):
        return self._cost
    
    @cost.setter
    def cost(self, value):
        if value is None:
            raise ValueError("Cost time not provided")

        self._cost = value
    
    @property
    def notes(self):
        return self._notes
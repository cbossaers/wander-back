class Day:
    def __init__(self, description: str, activities):
        self._id = 0
        self._description = description
        self._budget = 0
        self._activities = activities

        self.calculate_budget()

    def calculate_budget(self):
        self._budget = sum(activity.cost for activity in self.activities)
    
    def __json__(self):
        return {
            'id': self._id,
            'description': self._description,
            'budget': float(self._budget),
            'activities': [activity.__json__() for activity in self._activities]
        }

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def description(self):
        return self._description
    
    @description.setter
    def description(self, value):
        if value is None:
            raise ValueError("Description not provided")

        self._description = value
    
    @property
    def budget(self):
        return self._budget
    
    @budget.setter
    def budget(self, value):
        if value is None:
            raise ValueError("Budget not provided")

        self._bugdget = value
    
    @property
    def activities(self):
        return self._activities

    @activities.setter
    def activities(self, value):
        if value is None:
            raise ValueError("Activities not provided")

        if not isinstance(value, list):
            raise ValueError("Activities must be a list")

        if len(value) == 0:
            raise ValueError("Activities cannot be an empty list")

        self._activities = value
        self.calculate_budget()
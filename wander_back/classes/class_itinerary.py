from ..logic.validator import Validator as v


class Itinerary:
    def __init__(self, author: str, city: str, country: str, description: str, period: str, currency: str, tags, pictures, days):
        self._id = 0
        self._author = author
        self._city = city
        self._country = country
        self._duration = 0
        self._description = description
        self._period = period
        self._budget = 0
        self._currency = currency
        self._tags = tags
        self._pictures = pictures
        self._days = days

        self.calculate_budget()
        self.calculate_duration()

    def calculate_budget(self):
        self._budget = sum(day.budget for day in self.days)

    def calculate_duration(self):
        self._duration = len(self.days)

    def __json__(self):
        return {
            'id': self._id,
            'author': self._author,
            'city': self._city,
            'country': self._country,
            'duration': self._duration,
            'description': self._description,
            'period': self._period,
            'budget': float(self._budget),
            'currency': self._currency,
            'tags': self._tags,
            'pictures': self._pictures,
            'days': [day.__json__() for day in self._days]
        }

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        if value is None:
            raise ValueError("Author not provided")

        try:
            author = v.author_exists(value)
        except Exception as error:
            raise error

        self._author = author

    @property
    def city(self):
        return self._city

    @city.setter
    def city(self, value):
        if value is None:
            raise ValueError("City not provided")

        self._city = value

    @property
    def country(self):
        return self._country

    @country.setter
    def country(self, value):
        if value is None:
            raise ValueError("Country not provided")

        self._country = value

    @property
    def duration(self):
        return self._duration

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        if value is None:
            raise ValueError("Description not provided")

        self._description = value

    @property
    def currency(self):
        return self._currency

    @currency.setter
    def currency(self, value):
        if value is None:
            raise ValueError("Currency not provided")

        self._currency = value

    @property
    def period(self):
        return self._period

    @period.setter
    def period(self, value):
        if value is None:
            raise ValueError("Period not provided")

        try:
            period = v.period_is_valid(value)
        except Exception as error:
            raise error

        self._period = period

    @property
    def tags(self):
        return self._tags

    @tags.setter
    def tags(self, value):
        if value is None:
            raise ValueError("Tags not provided")

        if not isinstance(value, list):
            raise ValueError("Tags must be a list")

        if len(value) == 0:
            raise ValueError("Tags cannot be an empty list")

        self._tags = value

    @property
    def budget(self):
        return self._budget

    @budget.setter
    def budget(self, value):
        if value is None:
            raise ValueError("Budget not provided")

        self._budget = value

    @property
    def pictures(self):
        return self._pictures

    @pictures.setter
    def pictures(self, value):
        if value is None:
            raise ValueError("Pictures not provided")

        if not isinstance(value, list):
            raise ValueError("Pictures must be a list")

        if len(value) == 0:
            raise ValueError("Pictures cannot be an empty list")

        self._pictures = value

    @property
    def days(self):
        return self._days

    @days.setter
    def days(self, value):
        if value is None:
            raise ValueError("Days not provided")

        if not isinstance(value, list):
            raise ValueError("Days must be a list")

        if len(value) == 0:
            raise ValueError("Days cannot be an empty list")

        self._days = value
        self.calculate_duration()
        self.calculate_budget()

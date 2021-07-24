from . import record


# A human being
class Person(record.HistoricalRecord):

    def __init__(self, name, dob, gender):
        super(Person, self).__init__()
        self._name = name
        self._dob = dob
        self._gender = gender

    @property
    def Name(self):
        return self._name

    @Name.setter
    def Name(self, val):
        self._name = val

    @property
    def DateOfBirth(self):
        return self._dob

    @DateOfBirth.setter
    def DateOfBirth(self, val):
        self._dob = val

    @property
    def Gender(self):
        return self._gender

    @Gender.setter
    def Gender(self, val):
        self._gender = val

    def __repr__(self):
        return 'Name: {name} Dob: {dob} Gender: {gender}'. \
            format(name=self.Name, dob=self.DateOfBirth, gender=self.Gender)

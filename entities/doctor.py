from . import person


class Doctor(person.Person):
    def __init__(self, name=None, dob=None, gender=None, title=None):
        super(Doctor, self).__init__(name, dob, gender)
        self._title = title

    @property
    def Title(self):
        return self._title

    @Title.setter
    def Title(self, val):
        self._title = val

    def __repr__(self):
        return '{name} {title}'.format(title=self.Title, name=self.Name)

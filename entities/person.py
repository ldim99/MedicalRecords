class Person(object):
    def __init__(self, name, dob):
        self._name = name
        self._dob = dob

    @property
    def Name(self):
        return self._name

    @Name.setter
    def Name(self, val):
        self._name = val

    @property
    def Dob(self):
        return self._dob

    @Dob.setter
    def Dob(self, val):
        self,_dob = val
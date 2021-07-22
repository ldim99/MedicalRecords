import uuid


# a human being
class Person(object):

    def __init__(self, name, dob, gender, height, weight, doctorId):
        self._id = str(uuid.uuid4())
        self._name = name
        self._dob = dob
        self._gender = gender
        self._height = height
        self._weight = weight
        self._doc_id = doctorId

    @property
    def Id(self):
        return self._id

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
        self, _dob = val

    @property
    def Gender(self):
        return self._gender

    @Gender.setter
    def Gender(self, val):
        self._gender = val

    @property
    def Height(self):
        return self._height

    @Height.setter
    def Height(self, val):
        self._height = val

    @property
    def Weight(self):
        return self._weight

    @Weight.setter
    def Weight(self, val):
        self._weight = val

    @property
    def DoctorId(self):
        return self._doc_id

    @DoctorId.setter
    def DoctorId(self, val):
        self._doc_id = val

    def toDict(self):
        return dict((k, getattr(self, k)) for k in dir(self.__class__) if k[0].isupper())

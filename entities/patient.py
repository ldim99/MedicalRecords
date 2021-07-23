from . import person


class Patient(person.Person):
    def __init__(self, name=None, dob=None, gender=None, height=None, weight=None, doctor_id=None):
        super(Patient, self).__init__(name, dob, gender)
        self._doctorId = doctor_id
        self._height = height
        self._weight = weight
        self._preconditions = []
        self._allergies = []
        self._medications = []

    @property
    def Indexes(self):
        return ['Id','Name']

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
        return self._doctorId

    @DoctorId.setter
    def DoctorId(self, val):
        self._doctorId = val

    @property
    def Preconditions(self):
        return self._preconditions

    @Preconditions.setter
    def Preconditions(self, val):
        self._preconditions = val

    @property
    def Allergies(self):
        return self._allergies

    @Allergies.setter
    def Allergies(self, val):
        self._allergies = val

    @property
    def Medications(self):
        return self._medications

    @Medications.setter
    def Medications(self, val):
        self._medications = val

    def __repr__(self):
        return '{person} \n' \
               'Preconditions: {preconditions}\n' \
               'Allergies: {allergies}\n' \
               'Medications : {medications}'.format(person=super(Patient, self).__repr__(),
                                                    preconditions=','.join(self._preconditions),
                                                    allergies=','.join(self._allergies),
                                                    medications=','.join(self._medications))

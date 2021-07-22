from . import person


class Patient(person.Person):
    def __init__(self, registration_date, doctor_id):
        super(Patient, self).__init__()
        self._registartion_date = registration_date
        self._doctorId = doctor_id
        self._preconditions = []
        self._allergies = []
        self._medications = []

        @property
        def Preconditions(self):
            return self._preconditions

        @property
        def Allergies(self):
            return self._allergies

        @property
        def Medications(self):
            return self._medications

        @property
        def DoctorId(self):
            return self._doctorId


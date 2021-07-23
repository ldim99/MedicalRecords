import uuid
import datetime
import bisect
import json


# Record with a particular creation time
class HistoricalRecord(object):
    def __init__(self, id=None, creationTime=None):
        self._id = id or str(uuid.uuid4())
        self._creation_time = creationTime or datetime.datetime.utcnow()

    @property
    def Id(self):
        return self._id

    @Id.setter
    def Id(self, val):
        self._id = val

    @property
    def Indexes(self):
        return ['Id']

    @property
    def CreationTime(self):
        return self._creation_time

    @CreationTime.setter
    def CreationTime(self, val):
        self._creation_time = val

    def __lt__(self, other):
        return self.CreationTime < other.CreationTime

    def toDict(self):
        return dict(
            (k, getattr(self, k)) for k, v in
            vars(self.__class__).items() if isinstance(v, property) and v.fset is not None if k[0].isupper())

    def fromDict(self, d):
        for k, v in d.items():
            setattr(self, k, v)

    def toJSON(self):
        d = self.toDict()
        for k, v in d.items():
            if isinstance(v, (datetime.datetime, datetime.date)):
                d[k] = v.isoformat()
        return json.dumps(d)

    @classmethod
    def fromJSON(cls, jsonText):
        d = json.loads(jsonText)
        for k, v in d.items():
            if 'Time' in k:
                d[k] = datetime.datetime.fromisoformat(v)
            elif 'Date' in k:
                d[k] = datetime.datetime.fromisoformat(v).date()
        r = cls()
        r.fromDict(d)
        return r


# Records for a given patient
class PatientRecord(HistoricalRecord):
    def __init__(self, patientId):
        super(PatientRecord, self).__init__()
        self._patientId = patientId

    @property
    def Indexes(self):
        return ['Id','PatientId']

    @property
    def PatientId(self):
        return self._patientId

    @PatientId.setter
    def PatientId(self, val):
        self._patientId = val


# Record of patient's visit with  diagnostic and treatment information
class PatientVisit(PatientRecord):
    def __init__(self, patientId):
        super(PatientVisit, self).__init__(patientId)
        self._height = None
        self._weight = None
        self._bloodPressure = None
        self._diagnosis = None
        self._treatment = None
        self._notes = ''

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
    def BloodPressure(self):
        return self._bloodPressure

    @BloodPressure.setter
    def BloodPressure(self, val):
        self._bloodPressure = val

    @property
    def Diagnosis(self):
        return self._diagnosis

    @Diagnosis.setter
    def Diagnosis(self, val):
        self._diagnosis = val

    @property
    def Treatment(self):
        return self._treatment

    @Treatment.setter
    def Treatment(self, val):
        self._treatment = val

    @property
    def Notes(self):
        return self._notes

    @Notes.setter
    def Notes(self, val):
        self._notes = val

    @property
    def BMI(self):
        return 703 * self.Weight / pow(self.Height, 2)

    def __repr__(self):
        return 'Date: {date}\n' \
               'Height {height} in, Weight {weight} lbs, Blood Pressure {blooodPessure}, BMI={bmi:.2f}\n' \
               'Diagnosis: {diagnosis}\n' \
               'Treatment: {treatment}\n' \
               'Notes: {notes}'.format(date=self.CreationTime.date(),
                                       height=self.Height,
                                       weight=self.Weight,
                                       blooodPessure='/'.join(map(str, self.BloodPressure)),
                                       bmi=self.BMI,
                                       diagnosis=self.Diagnosis,
                                       treatment=self.Treatment,
                                       notes=self.Notes)


# Patient's history record
class PatientHistory(PatientRecord):
    def __init__(self, patientId):
        super(PatientHistory, self).__init__(patientId)
        self._visits = []

    @property
    def Visits(self):
        return list(self._visits)

    def addVisit(self, visit):
        bisect.insort_left(self._visits, visit)

    def getVisits(self, start=None, end=None):
        if start is None:
            start = self._visits[0].CreationTime
        if end is None:
            end = self._visits[-1].CreationTime

        s = bisect.bisect_left(self._visits, HistoricalRecord(self.Id, creationTime=start))
        e = bisect.bisect_right(self._visits, HistoricalRecord(self.Id, creationTime=end))
        if 0 <= s <= len(self._visits) and 0 <= e <= len(self._visits):
            return self._visits[s:e]
        return []

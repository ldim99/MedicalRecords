import datetime
import bisect
import json

# Record with creation timestamp
import pprint


class HistoricalRecord(object):
    def __init__(self, id=None, creationTime=None):
        self._id = id
        self._creation_time = creationTime or datetime.datetime.utcnow()

    @property
    def Id(self):
        return self._id

    @Id.setter
    def Id(self, val):
        self._id = val

    @property
    def CreationTime(self):
        return self._creation_time

    @CreationTime.setter
    def CreationTime(self, val):
        self._creation_time = val

    def __lt__(self, other):
        return self.CreationTime < other.CreationTime

    def toDict(self):
        return dict((k, getattr(self, k)) for k in dir(self.__class__) if k[0].isupper())

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


# Patient's visit record representing diagnostic and treatment
class PatientVisit(HistoricalRecord):
    def __init__(self, patientId):
        super(PatientVisit, self).__init__(patientId)
        self._diagnosis = None
        self._treatment = None
        self._notes = ''

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

    def __repr__(self):
        return 'Date: {date}, ' \
               'Diagnosis: {diagnosis}, ' \
               'Treatment: {treatment}, ' \
               'Notes: {notes}'.format(date=self.CreationTime.date(),
                                       diagnosis=self.Diagnosis,
                                       treatment=self.Treatment,
                                       notes=self.Notes)


# Patient's history
class PatientHistory(HistoricalRecord):
    def __init__(self, patientId):
        super(PatientHistory, self).__init__(patientId)
        self._visits = []

    @property
    def Visits(self):
        return list(self._visits)

    def addVisit(self, visit):
        bisect.insort_left(self._visits, visit)

    def getVisits(self, cutoffTime):
        i = bisect.bisect_right(self._visits, HistoricalRecord(self.Id, creationTime=cutoffTime))
        if i:
            return self._visits[0:i]
        return []

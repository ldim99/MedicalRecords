import uuid
import datetime


class HistoricalRecord(object):
    def __init__(self, patientId):
        self._id = str(uuid.uuid4())
        self._creation_time = datetime.datetime.utcnow()

    @property
    def CreationTime(self):
        return self._creation_time


class Visit(HistoricalRecord):
    def __init__(self, patientId):
        super(Visit, self).__init__()
        self._id = patientId
        self._diagnosis = None
        self._treatment = None
        self._notes = ''


class PatientsHistory(object):
    def __init__(self, patientId):
        self._patientId = patientId
        self._visits = []
from unittest import TestCase

import datetime
from entities import record


class RecordsTest(TestCase):
    def test_creation(self):
        patientId = id(self)
        history = record.PatientHistory(patientId)

        visit = record.PatientVisit(patientId)
        visit.CreationTime = datetime.datetime.utcnow() - datetime.timedelta(days=1)
        visit.Weight = 60
        visit.Height = 80
        visit.BloodPressure = [120, 80]
        visit.HeartRate = 80
        visit.Diagnosis = 'Headaches'
        visit.Treatment = 'Tylenol'
        visit.Notes = 'Wooden head'
        history.addVisit(visit)

        history1 = record.PatientHistory.fromJSON(history.toJSON())
        self.assertEqual(str(history.toDict()), str(history1.toDict()))

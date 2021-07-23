from unittest import TestCase

import datetime
from entities import patient


class PatientTest(TestCase):
    def test_creation(self):
        p = patient.Patient('Buratino', datetime.date(2010, 1, 1), 'M', 60, 30, 0)
        self.assertEqual(p.Name, 'Buratino')

    def test_repr(self):
        p = patient.Patient('Buratino', datetime.date(2010, 1, 1), 'M', 60, 30, 0)
        self.assertTrue(p.Name in str(p))

        p1 = patient.Patient.fromJSON(p.toJSON())
        self.assertEqual(p.toDict(), p1.toDict())

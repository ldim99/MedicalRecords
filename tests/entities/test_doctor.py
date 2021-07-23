from unittest import TestCase

import datetime
from entities import doctor


class DoctorTest(TestCase):
    def test_creation(self):
        d = doctor.Doctor('Dolittle',datetime.date(1920,5,1),'M','Dr')
        self.assertEqual(d.Name, 'Dolittle')
        self.assertEqual(d.Title, 'Dr')

    def test_repr(self):
        d = doctor.Doctor('Dolittle',datetime.date(1920,5,1),'M','Dr')
        self.assertTrue(d.Name in str(d))



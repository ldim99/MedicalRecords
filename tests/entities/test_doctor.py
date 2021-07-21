from unittest import TestCase

import datetime
from entities import doctor


class TestDoctor(TestCase):
    def test_name(self):
        d = doctor.Doctor('Dolittle',datetime.date(1920,5,1))
        self.assertEqual(d.Name, 'Dolittle')

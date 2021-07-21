from unittest import TestCase

from entities import doctor


class TestDoctor(TestCase):
    def test_name(self):
        d = doctor.Doctor('Dolittle')
        self.assertEqual(d.Name, 'Dolittle')

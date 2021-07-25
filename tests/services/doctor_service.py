from unittest import TestCase
import datetime
from entities import patient, doctor
from services import service_gateway, entity_service, doctors_service, reporting_service


class DoctorServiceTest(TestCase):
    def test_DoctorAPI(self):
        es = entity_service.EntityService(entity_service.DictionaryBackingStore())
        service_gateway.Registry.registerService(es)
        ds = service_gateway.Registry.lookupService('DoctorsService')

        d = doctor.Doctor('Dolittle', datetime.date(1920, 5, 1), 'M', 'MD')
        ctx = service_gateway.InvocationContext(d.Id)
        es.store(ctx, d)

        d1 = ds.findDoctor(ctx, d.Name)
        self.assertEqual(d, d1)

        p = patient.Patient('Buratino', datetime.date(2010, 1, 1), 'M', 60, 30, d.Id)
        p.Preconditions = ['Made of wood']
        p.Allergies = ['Water']
        p.Medications = ['Read a book twice a day']

        ds.createPatient(ctx, p)

        p1 = ds.findPatient(ctx, p.Id)
        self.assertEqual(p, p1)

        p1.Allergies.append('Milk')
        ds.updatePatient(ctx, p1)

        p2 = ds.findPatient(ctx, p.Id)
        self.assertIn('Milk', p2.Allergies)

from unittest import TestCase
import datetime
from entities import patient, doctor
from services import service_gateway, entity_service, doctors_service, patients_service


class TestPatientService(TestCase):
    def testPatientAPI(self):
        es = entity_service.EntityService(entity_service.DictionaryBackingStore())
        service_gateway.Registry.registerService(es)
        ds = service_gateway.Registry.lookupService('DoctorsService')
        ps = service_gateway.Registry.lookupService('PatientsService')

        d = doctor.Doctor('Dolittle', datetime.date(1920, 5, 1), 'M', 'MD')
        p = patient.Patient('Buratino', datetime.date(2010, 1, 1), 'M', 60, 30, d.Id)
        p.Preconditions = ['Made of wood']
        p.Allergies = ['Water']
        p.Medications = ['Read a book twice a day']

        dctx = service_gateway.InvocationContext(d.Id)
        pctx = service_gateway.InvocationContext(p.Id)
        ds.createPatient(dctx, p)

        p1 = ds.findPatient(dctx, p.Id)
        p2 = ps.findPatient(pctx, p.Name)
        self.assertEqual(p1, p2)

        p2.Allergies.append('Milk')
        ps.updatePatient(pctx, p2)

        p3 = ps.findPatient(pctx, p.Name)
        self.assertIn('Milk', p3.Allergies)







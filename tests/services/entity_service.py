from unittest import TestCase
import datetime
from entities import patient, doctor, record
from services import entity_service, service_gateway, doctors_service, patients_service


# Tests for entity service API
class EntityServiceTest(TestCase):
    def setUp(self):
        self.bs = entity_service.DictionaryBackingStore()
        self.es = entity_service.EntityService(self.bs)
        service_gateway.Registry.registerService(self.es)

    def test_lookup(self):
        p = patient.Patient('Buratino', datetime.date(2010, 1, 1), 'M', 60, 30, 0)
        d = doctor.Doctor('Dolittle', datetime.date(1920, 5, 1), 'M', 'Dr')

        ctx = service_gateway.InvocationContext(d.Id)

        self.es.store(ctx, d)
        self.es.store(ctx, p)

        p1 = self.es.lookup(ctx, 'Patient', 'Id', p.Id)
        self.assertEqual(p, p1)
        d1 = self.es.lookup(ctx, 'Doctor', 'Id', d.Id)
        self.assertEqual(d, d1)

    def test_store(self):
        d = doctor.Doctor('Dolittle', datetime.date(1920, 5, 1), 'M', 'Dr')
        p = patient.Patient('Buratino', datetime.date(2010, 1, 1), 'M', 60, 30, d.Id)

        ctx = service_gateway.InvocationContext(d.Id)

        self.es.store(ctx, d)
        self.es.store(ctx, p)

        history = record.PatientHistory(p.Id)

        visit = record.PatientVisit(p.Id)
        visit.Weight = 60
        visit.Height = 80
        visit.HeartRate = 75
        visit.BloodPressure = (80, 120)
        visit.Diagnosis = 'Headaches'
        visit.Treatment = 'Tyleon'
        visit.Notes = 'Wooden head'
        history.addVisit(visit)

        ds = service_gateway.Registry.lookupService('DoctorsService')
        ds.updatePatientHistory(ctx, history)
        h1 = ds.findPatientHistory(ctx, p.Id)

        self.assertEqual(history.getVisits(), h1.getVisits())

        json1 = self.bs.toJSON()
        self.bs.fromJSON(json1)
        json2 = self.bs.toJSON()
        self.assertEqual(json1, json2)

    def test_Load(self):
        with open('../data/store.json') as f:
            json = f.read()

        self.bs.fromJSON(json)

        ds = service_gateway.Registry.lookupService('DoctorsService')
        ps = service_gateway.Registry.lookupService('PatientsService')

        dctx = service_gateway.InvocationContext(id(self))
        d = ds.findDoctor(dctx, 'Dolittle')
        self.assertIsNotNone(d)

        dctx = service_gateway.InvocationContext(d.Id)

        p1 = ps.findPatient(dctx, 'Buratino')
        self.assertIsNotNone(p1)
        p2 = ps.findPatient(dctx, 'Buratino')
        self.assertIsNotNone(p2)

        hist = ds.findPatientHistory(dctx, p1.Id)
        self.assertIsNotNone(hist)

from unittest import TestCase
import datetime
from entities import patient, doctor, record
from services import entity_service,  service_gateway, doctors_service

class TestEntityService(TestCase):
      def testLookup(self):
          es = entity_service.EntityService(entity_service.DictionaryBackingStore())
          service_gateway.Registry.registerService(es)

          p = patient.Patient('Buratino', datetime.date(2010, 1, 1), 'M', 60, 30, 0)
          d = doctor.Doctor('Dolittle',datetime.date(1920,5,1),'M','Dr')

          ctx = service_gateway.InvocationContext(d.Id)

          es.store(ctx, d)
          es.store(ctx, p)

          p1 = es.lookup(ctx, 'Patient', 'Id', p.Id)
          self.assertEqual(p, p1)
          d1 = es.lookup(ctx, 'Doctor', 'Id', d.Id)
          self.assertEqual(d, d1)

      def testStore(self):
          es = entity_service.EntityService(entity_service.DictionaryBackingStore())
          service_gateway.Registry.registerService(es)

          d = doctor.Doctor('Dolittle',datetime.date(1920,5,1),'M','Dr')
          p = patient.Patient('Buratino', datetime.date(2010, 1, 1), 'M', 60, 30, d.Id)

          ctx = service_gateway.InvocationContext(d.Id)

          es.store(ctx, d)
          es.store(ctx, p)

          history = record.PatientHistory(p.Id)

          visit = record.PatientVisit(p.Id)
          visit.Weight = 60
          visit.Height = 80
          visit.BloodPressure = (80, 120)
          visit.Diagnosis = 'Headaches'
          visit.Treatment = 'Tyleon'
          visit.Notes = 'Wooden head'
          history.addVisit(visit)

          ds = service_gateway.Registry.lookupService('DoctorsService')
          ds.updatePatientHistory(ctx, history)
          h1 = ds.findPatientHistory(ctx, p.Id)

          self.assertEqual(history.getVisits(), h1.getVisits())




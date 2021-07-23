from unittest import TestCase
import datetime
from entities import patient, doctor
from services import entity_service,  service_gateway

class TestEntityService(TestCase):
      def testCreate(self):
          es = entity_service.EntityService(entity_service.DictionaryBackingStore())

          p = patient.Patient('Buratino', datetime.date(2010, 1, 1), 'M', 60, 30, 0)
          d = doctor.Doctor('Dolittle',datetime.date(1920,5,1),'M','Dr')

          ctx = service_gateway.InvocationContext(d.Id)

          es.store(ctx, d)
          es.store(ctx, p)

          p1 = es.lookup(ctx, 'Patient', 'Id', p.Id)
          self.assertEqual(p, p1)
          d1 = es.lookup(ctx, 'Doctor', 'Id', d.Id)
          self.assertEqual(d, d1)
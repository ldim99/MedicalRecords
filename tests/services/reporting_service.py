from unittest import TestCase
import datetime
from entities import patient, doctor, record
from services import service_gateway, entity_service, doctors_service, reporting_service

class TestReportingService(TestCase):
    def testPatientSummary(self):
        es = entity_service.EntityService(entity_service.DictionaryBackingStore())
        service_gateway.Registry.registerService(es)
        ds = service_gateway.Registry.lookupService('DoctorsService')

        d = doctor.Doctor('Dolittle', datetime.date(1920, 5, 1), 'M', 'MD')

        p1 = patient.Patient('Buratino', datetime.date(2010, 1, 1), 'M', 60, 30, d.Id)
        p1.Preconditions = ['Made of wood']
        p1.Allergies = ['Water']
        p1.Medications = ['Read a book twice a day']

        p2 = patient.Patient('Giuseppe ', datetime.date(1940, 1, 1), 'M', 100, 160, d.Id)
        p2.Preconditions = ['Drunk']
        p2.Allergies = ['Salad']
        p2.Medications = ['Drink juice and water']

        ctx = service_gateway.InvocationContext(d.Id)

        es.store(ctx, d)
        es.store(ctx, p1)
        es.store(ctx, p2)

        history1 = record.PatientHistory(p1.Id)

        visit = record.PatientVisit(p1.Id)
        visit.CreationTime = datetime.datetime.utcnow() - datetime.timedelta(days=1)
        visit.Weight = 60
        visit.Height = 80
        visit.BloodPressure = (120, 80)
        visit.Diagnosis = 'Headaches'
        visit.Treatment = 'Tyleon'
        visit.Notes = 'Wooden head'
        history1.addVisit(visit)

        ds.updatePatientHistory(ctx, history1)

        history2 = record.PatientHistory(p2.Id)

        visit = record.PatientVisit(p2.Id)
        visit.Weight = 65
        visit.Height = 81
        visit.BloodPressure = (115, 75)
        visit.Diagnosis = 'Red Nose'
        visit.Treatment = 'Milk'
        visit.Notes = 'Too much drinking'
        history2.addVisit(visit)

        ds.updatePatientHistory(ctx, history2)

        rs = service_gateway.Registry.lookupService('ReportingService')
        s1 = rs.patientHealthSummary(ctx, p1.Id, datetime.datetime.utcnow() - datetime.timedelta(weeks=52),
                                     datetime.datetime.utcnow())

        s2 = rs.patientHealthSummary(ctx, p2.Id, datetime.datetime.utcnow() - datetime.timedelta(weeks=52),
                                     datetime.datetime.utcnow())
        print(s1, '\n')
        print(s2)

        self.assertIsNotNone(s1)
        self.assertIsNotNone(s2)

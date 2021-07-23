from unittest import TestCase
import datetime
from entities import patient, doctor, record
from services import service_gateway, entity_service, doctors_service, reporting_service


class TestReportingService(TestCase):
    def testPatientSummary(self):
        es = service_gateway.Registry.lookupService('EntityService')

        d = doctor.Doctor('Dolittle',datetime.date(1920,5,1),'M','MD')
        p = patient.Patient('Buratino', datetime.date(2010, 1, 1), 'M', 60, 30, d.Id)
        p.Preconditions = ['Made of wood']
        p.Allergies = ['Water']
        p.Medications = ['Read a book twice a day']

        ctx = service_gateway.InvocationContext(d.Id)

        es.store(ctx, d)
        es.store(ctx, p)

        history = record.PatientHistory(p.Id)

        visit = record.PatientVisit(p.Id)
        visit.CreationTime = datetime.datetime.utcnow()-datetime.timedelta(days=1)
        visit.Diagnosis = 'Headaches'
        visit.Treatment = 'Tyleon'
        visit.Notes = 'Wooden head'
        history.addVisit(visit)

        visit = record.PatientVisit(p.Id)
        visit.Diagnosis = 'Enlarged Nose'
        visit.Treatment = 'Balm'
        visit.Notes = 'Too much lying'
        history.addVisit(visit)

        ds = service_gateway.Registry.lookupService('DoctorsService')
        ds.updatePatientHistory(ctx, history)

        history = ds.findPatientHistory(ctx, p.Id)
        self.assertIsNotNone(history)

        rs = service_gateway.Registry.lookupService('ReportingService')
        s = rs.patientHealthSummary(ctx, p.Id, datetime.datetime.utcnow())
        print(s)
        self.assertIsNotNone(s)

import pprint

import services.service_gateway
from . import service_gateway


class ReportingService(services.service_gateway.Service):

    def __init__(self):
        super(ReportingService, self).__init__('Reporting service for patients & doctors')

    def patientHealthSummary(self, ctx, patientId, date):
        es = service_gateway.Registry.lookupService('EntityService')
        patient = es.lookup(ctx, 'Patient', 'Id', patientId)
        if patient and ctx.UserId in (patientId, patient.DoctorId):
            doctor = es.lookup(ctx, 'Doctor', 'Id', patient.DoctorId)
            history = es.lookup(ctx, 'PatientHistory', 'Id', patientId)
            return self._generateSummary(patient, doctor, history, date)

    def _generateSummary(self, patient, doctor, history, date):
        return '{patientInfo}\n' \
               'Doctor: {doctorInfo}\n' \
               '{visits}'.format(patientInfo=patient,
                                 doctorInfo=doctor,
                                 visits='\n'.join(map(str, history.getVisits(date))))


service_gateway.Registry.registerService(ReportingService())

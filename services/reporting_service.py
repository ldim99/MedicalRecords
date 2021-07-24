import statistics

import services.service_gateway
from . import service_gateway


class ReportingService(services.service_gateway.Service):

    def __init__(self):
        super(ReportingService, self).__init__('Reporting service for patients & doctors')

    def patientHealthSummary(self, ctx, patientId, start, end):
        es = service_gateway.Registry.lookupService('EntityService')
        patient = es.lookup(ctx, 'Patient', 'Id', patientId)
        if patient and ctx.UserId in (patientId, patient.DoctorId):
            doctor = es.lookup(ctx, 'Doctor', 'Id', patient.DoctorId)
            history = es.lookup(ctx, 'PatientHistory', 'PatientId', patientId)
            return self._generateSummary(patient, doctor, history, start, end)

    def _generateSummary(self, patient, doctor, history, start, end):
        visits = history.getVisits(start, end) if history else []
        bloodPressures = list(zip(*[v.BloodPressure for v in visits]))

        meanBP = (statistics.mean(bloodPressures[0]), statistics.mean(bloodPressures[1])) if bloodPressures else []
        medianBP = (
        statistics.median(bloodPressures[0]), statistics.median(bloodPressures[1])) if bloodPressures else []
        maxBP = (max(bloodPressures[0]), max(bloodPressures[1])) if bloodPressures else []

        return '{patientInfo}\n' \
               'Doctor: {doctorInfo}\n' \
               'Blood Pressure: mean: {meanBP} median: {medianBP} max: {maxBP}\n' \
               '{visits}'.format(patientInfo=patient,
                                 doctorInfo=doctor,
                                 meanBP='/'.join(map(str, meanBP)), medianBP='/'.join(map(str, medianBP)),
                                 maxBP='/'.join(map(str, maxBP)),
                                 visits='\n'.join(map(str, visits)))


service_gateway.Registry.registerService(ReportingService())

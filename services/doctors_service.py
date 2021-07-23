import services.service_gateway
from . import service_gateway


# Provide CRU operations for doctors
class DoctorsService(services.service_gateway.Service):

    def __init__(self):
        super(DoctorsService, self).__init__('Informational service for doctors')

    def createPatient(self, ctx, patient):
        if patient and patient.DoctorId == ctx.UserId:
            es = service_gateway.Registry.lookupService('EntityService')
            es.store('Patient', patient)

    def findPatient(self, ctx, patientId):
        es = service_gateway.Registry.lookupService('EntityService')
        patient = es.lookup(ctx, 'Patient', 'Id', patientId)
        if patient and patient.DoctorId == ctx.UserId:
            return patient
        return None

    def updatePatient(self, ctx, patient):
        es = service_gateway.Registry.lookupService('EntityService')
        cur_patient = es.lookup(ctx, 'Patient', 'Id', patient.Id)
        if cur_patient.DoctorId == ctx.UserId:
            es.store('Patient', patient)

    def findPatientHistory(self, ctx, patientId):
        patient = self.findPatient(ctx, patientId)
        if patient and patient.DoctorId == ctx.UserId:
            es = service_gateway.Registry.lookupService('EntityService')
            history = es.lookup(ctx, 'PatientHistory', 'PatientId', patientId)
            return history
        return None

    def updatePatientHistory(self, ctx, history):
        patient = self.findPatient(ctx, history.PatientId)
        if patient and patient.DoctorId == ctx.UserId:
            es = service_gateway.Registry.lookupService('EntityService')
            es.store(ctx, history)


service_gateway.Registry.registerService(DoctorsService())

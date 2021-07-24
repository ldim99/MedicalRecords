import services.service_gateway
from . import service_gateway


# A set of CRUD operations for patients
class PatientsService(services.service_gateway.Service):

    def __init__(self):
        super(PatientsService, self).__init__('Informational service for patients')

    def findPatient(self, ctx, patientName):
        es = service_gateway.Registry.lookupService('EntityService')
        patient = es.lookup(ctx, 'Patient', 'Name', patientName)
        if ctx.UserId in (patient.Id, patient.DoctorId):
            return patient
        return None

    def updatePatient(self, ctx, patient):
        if ctx.UserId in (patient.Id, patient.DoctorId):
            es = service_gateway.Registry.lookupService('EntityService')
            es.store(ctx, patient)

    def findPatientHistory(self, ctx, patientId):
        if ctx.UserId == patientId:
            es = service_gateway.Registry.lookupService('EntityService')
            history = es.lookup(ctx, 'PatientHistory', 'PatientId', patientId)
            return history


service_gateway.Registry.registerService(PatientsService())

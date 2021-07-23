import services.service_gateway
from . import service_gateway


class PatientsService(services.service_gateway.Service):

    def __init__(self):
        super(PatientsService,self).__init__('Informational service for patients')

    def findPatient(self, ctx, patientName):
        es = service_gateway.Registry.lookupService('EntityService')
        patient = es.lookup('Patient', 'Name', patientName)
        if ctx.UserId == patient.Id:
           return patient
        return None

    def updatePatient(self, ctx, patient):
        if ctx.UserId == patient.Id:
            es = service_gateway.Registry.lookupService('EntityService')
            es.update('Patient', patient)

    def findPatientHistory(self, ctx, patientId):
        if ctx.UserId != patientId:
            return None
        es = service_gateway.Registry.lookupService('EnitityService')
        history = es.lookup('PatientHistory', 'Id', patientId)
        return history


service_gateway.Registry.registerService(PatientsService())

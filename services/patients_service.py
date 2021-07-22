import services.service_gateway
from . import service_gateway


class PatientsService(services.service_gateway.Service):
    def findPatient(self, patientName):
        es = service_gateway.Registry.lookupService('EntityService')
        patient = es.lookup('Patient', patientName)
        return patient

    def updatePatient(self, patient):
        es = service_gateway.Registry.lookupService('EntityService')
        es.update('Patient', patient)

    def findPatientsHistory(self, patientId):
        ps = service_gateway.Registry.lookupService('EnitityService')
        record = ps.lookup('PatientsHistory', patientId)
        return record


service_gateway.Registry.registerService(PatientsService())

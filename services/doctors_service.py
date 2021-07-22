import services.service_gateway
from . import service_gateway


class DoctorsService(services.service_gateway.Service):

    def findPatient(self, doctorId, patientName):
        ps = service_gateway.Registry.lookupService('EntityService')
        patient = ps.lookup('Patient', patientName)
        if patient and patient.DoctorId == doctorId:
            return patient
        else:
            return None

    def updatePatient(self, doctorId, patient):
        ps = service_gateway.Registry.lookupService('EntityService')
        if patient.DoctorId == doctorId:
            ps.update('Patient', patient)

    def findPatientsHistory(self, doctorId, patientId):
        patient = self.findPatient(patientId)
        if patient and patient.DoctorId == doctorId:
            ps = service_gateway.Registry.lookupService('EntityService')
            history = ps.lookup('PatientsHistory', patientId)
            return history
        else:
            return None

    def updatePatientsHistory(self, doctorId, patientId, history):
        ps = service_gateway.Registry.lookupService('EntityService')
        patient = self.findPatient(patientId)
        if patient and patient.DoctorId == doctorId:
            ps.update('PatientsHistory', history)


service_gateway.Registry.registerService(DoctorsService())

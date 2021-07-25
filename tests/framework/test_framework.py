import logging
import sys
import getpass
import datetime
from entities import record
from services import service_gateway, entity_service, doctors_service, patients_service, reporting_service

root = logging.getLogger()
handler = logging.StreamHandler(sys.stdout)
root.addHandler(handler)

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# Looking up required services
es = service_gateway.Registry.lookupService('EntityService')
ds = service_gateway.Registry.lookupService('DoctorsService')
ps = service_gateway.Registry.lookupService('PatientsService')

with open('../data/store.json') as f:
    json = f.read()

log.info('Initializing json store from %s', f.name)
es.BackingStore.fromJSON(json)

# Current user's security context to find specific doctor
ctx = service_gateway.InvocationContext(getpass.getuser())

drName = 'Dolittle'
log.info('Looking up doctor %s ...', drName)

d = ds.findDoctor(ctx, 'Dolittle')
log.info('Found doctor:  %s', d)

# Doctor's security context
dctx = service_gateway.InvocationContext(d.Id)

pName = 'Buratino'
log.info('Looking up patient %s ...', pName)

p = ps.findPatient(dctx, pName)
log.info('Found patient: %s', p)

log.info('Generating summary for %s for the last 12 months..,', pName)
rs = service_gateway.Registry.lookupService('ReportingService')
s = rs.patientHealthSummary(dctx, p.Id, datetime.datetime.utcnow() - datetime.timedelta(weeks=52),
                            datetime.datetime.utcnow())
log.info('\nExisting medical records and visits for %s:\n\n%s', pName, s)

history = es.lookup(ctx, 'PatientHistory', 'PatientId', p.Id)

# Creating new visit
visit = record.PatientVisit(p.Id)
visit.CreationTime = datetime.datetime.utcnow() - datetime.timedelta(days=1)
visit.Weight = 79
visit.Height = 82
visit.BloodPressure = (140, 90)
visit.HeartRate = 99
visit.Diagnosis = 'Extreme Happiness'
visit.Treatment = 'Icecream'
visit.Notes = 'Sprinkles on top'
history.addVisit(visit)

log.info('Creating new visit for today')
ds.updatePatientHistory(ctx, history)

# generating health and visit summary for the lsat 12 months
s = rs.patientHealthSummary(dctx, p.Id, datetime.datetime.utcnow() - datetime.timedelta(weeks=52),
                            datetime.datetime.utcnow())
log.info('\nUpdated medical records and visits for %s:\n\n%s', pName, s)

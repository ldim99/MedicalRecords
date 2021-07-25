## Medical Records Manager

Overall goal of this project is to provide programmatic interface for patients and doctors to view and manage medical
records, history of visits and generate reports with patient summaries, doctors diagnostic and treatment information and
aggregate health records

Project implemented as a set of microservices and entity classes representing doctors, patients and visit records.
Patient records include basic patient information - name, date of birth, gender, height and weight as well as their
pre-existing conditions, allergies and medications. Visit records include doctor notes, diagnosis, prescriptions as well
as measures taken during the visit - height, weight, blood pressure and heart rate

Project implemented as a group of externally facing microservices with common registration and lookup interface:

Patient Service:

- browse patients information and medical history
- update patients information

Doctor Services:

- browse patients information and medical history
- update patients information and medical history

Reporting Service:

- generates patient health summary with historical metrics - BMI, blood pressure, heart rate for a given range of dates
- list historical visits with corresponding metrics

An implicit level of doctor/patient isolaton is guranteed when patients and doctors will only be able to browse and edit
information that is relevant to them

### System Design:

      Web/Mobile Client -> Load Balancer -> Web Server (Front End UI)
                                         -> HTTP REST API -> Microservice Registry -> Microservices -> Cache -> Backing Store
                                                                \                                                   /
                                                                 \ _____________ This implementation _____________ /

Doctors and patients are using mobile app/web browser to establish secure (SSL) HTTP connection with a Web Server which
authenticates clients and generates front end representation. A load balancer such as NGINX or HAProxy handles client
requests for routing to the pool of HTTP Web servers and also for rate limiting/DDOS prevention

Once logged-in patients should be able to browse and update their personal information while doctors sholud be able to
browse their patients personal information as well as being able to create and update their records and history of
visits

All service invocations performed via REST API and handled by reverse proxy such as NGINX with a pool of HTTP REST
endpoints. In order to separate client-facing REST API from service implementation an API-gateway serves as registry and
invocation router for all external and inter-service calls. API gateway also serves as security enforcement, load
balancing and rate limiting mechanism. Services get registered and resolved via service registry which should support
service health checks and de-registration via heartbeating mechanism

Depending on the number of clients system can be distributed geographically with closest datacenters handling traffic
for a given region

An object cache such as Radis or Memcached can be used to for state sharing between various sevices. An asynchronous
persistence to a backing NoSQL store such as Cassandra or MongoDB. A SQL database such as Postgres or SQL Server can
also be used however it will require a more rigid table schema to be defined with object-relational mapping which
typically results in higher maintenance costs.

### Data Model:

     A backing store perisits data model which is present as entity object model at runtime
     (inheritance indicated by arrows from children on the top toward ancestors on the bottom)

     Patient, Doctor       PatientVisit   PatientHistory
           \                    \           /
            Person              PatientRecord
              \                     /
                  HistoricalRecord

### Service Model:

     All services are fully decoupled and communicate with each other with the help of service gatweay which supports registration 
     and lookup operations.
     Service gateway captures invocation context containing invoking client id (either patients or doctors user id) and makes it avaiiable in each service request
     Invocation context is also getting passed for inter-service invocations enabling permission enforement throught invocaiton chain.   
     Service Gateway servers as  extension point for load balancing and scaling allowing for dynamic increase in the number of individual service instances

     Entity service provides CRUD operations on entities such Doctors, Patients and PatiensVisits by delegating storage and retrival to the backing store that its preconfigured with 
     Entity service ensures that Locking is performed at the entity level to avoid concurrent modifications during updates

     Doctor and Patient services perfom find, lookup and modications operations on behalf of doctors and patiens respectively while ensureing proper access control

     Reporting Service generates reports which include patient records, visit history, diagnostic and treatment information and historical health summaries 
     such as blood pressue, heart rate and BMI. Reporting service also ensures that only patient and his/her doctor are able to generate reports for a given patient

                        Reporting Service
                              |
     Patient Service ---- Service Gateway ---- Doctor Service
                              |
                         Entity Service  
                              |
                         Backing Store

### Project Outline:

Top level directories:

/entities - class definitions for Patient, Doctor, PatientVisit and PatientHistory

/services - service definitions for Patients, Doctors, Reporting and Entity services as well as ServiceGateway

/tests - unit and integration tests for entities and services as well as same data store in json format /data/store.json

## Sample Usage:

Various usages examples provided as part of the following unittests tests:

/tests/services/doctor_service.py - doctors creation and lookup by name - patients creation and update by a given doctor

/tests/services/patient_service.py - patients creation and lookup by id and name

/tests/services/entity_service.py - doctor and patient store and lookup, serialization into json and sample store load
from ../data/store.json

/tests/services/reporting_service.py - patients health summary generation for a given date range such as last 12 months

/tests/framework/test_framework.py - integration test demonstrating initialization and framework usage
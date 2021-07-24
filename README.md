##Medical Records Manager

Overall goal of this project is to provide interface for patients and doctors to be able manage medical records and history of visits as well as being able to generate reports

Project implemented as a set of microservices and entity classes represnting  doctors, patients and visit records
Patient records include basic patient information - name, date of birth, gender, height and weight as well as their pre-existing conditions, allergies and midications
Visit records include doctor notes, diagnosis and prescriptions as well as measures taken during the visit - height, weight, blood pressure and heart rate

Project implemented as a group of microservices with common registration and lookup interface:

1. Patient Service *:
  - browse patients information and medical history
  - update patients information

2. Doctor Services *:
   - browse patients information and medical history
   - update patients information and medical history

3. Reporting Service *:
   - generates patient health summary with historical metrics - BMI, blood pressure, heart rate for a given range of dates
   = list historical visits with corresponding metrics

* An implicit level of doctor/patient isolaton is guranteed when patients and doctors will only be able to browse and edit information that is relevant to them

###System Design:

  Web/Mobile Client -> Load Balancer -> Web Server (Front End UI)
                                     -> HTTP REST API -> Microservice Registry -> Microservices -> Cache -> Backing Store
                                                            \                                                   /
                                                             \ _____________ This implementation _____________ /

 Doctors and patients are using mobile/web browser to establish secure (SSL) connection with Web Server
 Web Server provides login screen and authenticates clients
 Once logged in clients are able to browse and update relevant information according to the specification by issuing HTTP requests to the web server
 Web Server lookups up corresponding services from the registry , invokes them , formats results and returns them back to clients

 In order to handle large number of http clients a load balancer is needed to route requests to the available web server / http REST endpoint
 Depending on the number of clients system can be distributed geographically with closest datacenters handling traffic for a given region

 An object cache such as Radis can be used to cache and share entities between various microsevices
 An asynchronous persistence to a backing NoSql store such as Cassandra or MongoDB hover
 A SQL store such as Postgres SQL can also be used however it will require object-relational mapping with higher maintenance costs

 ###Data Model:

     (inheritance indicated by arrows from children on the top toward ancestors on the bottom)

     Patient, Doctor       PatientVisit   PatientHistory
           \                    \           /
            Person              PatientRecord
              \                   /
                HistoricalRecord

###Service Model:

     All services as well as external REST endpoints are fully decoupled from each other and able to communicate with help of service gatweay
     which performs registration and resolution on behalf of services . Service Gateway is also an extension point allowing for load balancing and scaling

                        Reporting Service
                              |
     Patient Service ---- Service Gateway ---- Doctor Service
                              |
                         Entity Service
                              |
                         Backing Store


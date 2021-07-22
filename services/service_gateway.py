

class Registry(object):
    _services = {}

    @classmethod
    def registerService(cls, service):
        cls._services[service.Id] = service

    @classmethod
    def lookupService(cls, serviceId):
        return cls._services.get(serviceId)


class Service(object):
    def __init__(self):
        self._id = self.__class__

    @property
    def Id(self):
        return self._id
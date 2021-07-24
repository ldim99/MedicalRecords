class Registry(object):
    _services = {}

    @classmethod
    def registerService(cls, service):
        cls._services[service.Id] = service

    @classmethod
    def lookupService(cls, serviceId):
        return cls._services.get(serviceId)


class Service(object):
    def __init__(self, description):
        self._id = self.__class__.__name__
        self._description = description

    @property
    def Id(self):
        return self._id

    @property
    def Description(self):
        return self._id


class InvocationContext(object):
    def __init__(self, userId):
        self._user_id = userId

    @property
    def UserId(self):
        return self._user_id

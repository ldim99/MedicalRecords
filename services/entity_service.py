import services.service_gateway
from . import service_gateway
from collections import defaultdict


class EntityService(services.service_gateway.Service):
    _entitiesByName = defaultdict(dict)

    def lookupByName(self, entityClass, entityName):
        return self._entitiesByName[entityClass].get(entityName)

    def lookupById(self, entityClass, entityId):
        return self._entitiesById[entityClass].get(entityId)

    def store(self, entity):
        self._entitiesById[entity.__class__.__name__] = entity


service_gateway.Registry.registerService(EntityService())

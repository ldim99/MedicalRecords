import services.service_gateway
from . import service_gateway
from collections import defaultdict


class EntityService(services.service_gateway.Service):

    def __init__(self, backingStore):
        super(EntityService, self).__init__('Entity lookup service')
        self._backingStore = backingStore

    def lookup(self, ctx, entityClass, lookupType, entityKey):
        if lookupType == 'Id':
            return self._backingStore.lookupById(entityClass, entityKey)
        elif lookupType == 'Name':
            return self._backingStore.lookupByName(entityClass, entityKey)
        return None

    def store(self, ctx, entity):
        self._backingStore.store(entity.__class__.__name__, entity)


class BackingStore(object):
    def lookupByName(self, entityType, enitityName):
        raise NotImplemented()

    def lookupById(self, entityType, enitityId):
        raise NotImplemented()

    def store(self, entityType, enitity):
        raise NotImplemented()


class DictionaryBackingStore(BackingStore):
    _entitiesById = defaultdict(dict)
    _entitiesByName = defaultdict(dict)

    def DictionaryBackingStore(self, content=None):
        pass

    def lookupById(self, entityType, enitityId):
        return self._entitiesById[entityType].get(enitityId)

    def lookupByName(self, entityType, enitityName):
        return self._entitiesByName[entityType].get(enitityName)

    def store(self, entityType, entity):
        self._entitiesById[entityType][entity.Id] = entity
        if hasattr(entity,'Name'):
           self._entitiesByName[entityType][entity.Name] = entity


service_gateway.Registry.registerService(EntityService(DictionaryBackingStore()))

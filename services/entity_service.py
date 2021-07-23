import services.service_gateway
from . import service_gateway
from collections import defaultdict
from functools import partial

class EntityService(services.service_gateway.Service):

    def __init__(self, backingStore):
        super(EntityService, self).__init__('Entity lookup service')
        self._backingStore = backingStore

    def lookup(self, ctx, entityClass, index, entityKey):
        return self._backingStore.lookupByIndex(entityClass, index, entityKey)

    def store(self, ctx, entity):
        self._backingStore.store(entity.__class__.__name__, entity)


class BackingStore(object):

    def lookupByIndex(self, entityType, index, enitityId):
        raise NotImplemented()

    def store(self, entityType, enitity):
        raise NotImplemented()


class DictionaryBackingStore(BackingStore):
    _entitiesByIndex = defaultdict(partial(defaultdict,dict))

    def DictionaryBackingStore(self, content=None):
        pass

    def lookupByIndex(self, entityType, index, enitityId):
        return self._entitiesByIndex[entityType].get(index).get(enitityId)

    def store(self, entityType, entity):
        indexes = entity.Indexes
        for index in indexes:
            self._entitiesByIndex[entityType][index][getattr(entity, index)] = entity


service_gateway.Registry.registerService(EntityService(DictionaryBackingStore()))

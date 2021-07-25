import services.service_gateway
from entities import record
from . import service_gateway
from collections import defaultdict
from functools import partial
import json


# Entity persistance and lookup service with pluggable backing store
class EntityService(services.service_gateway.Service):

    def __init__(self, backingStore):
        super(EntityService, self).__init__('Entity lookup service')
        self._backingStore = backingStore

    @property
    def BackingStore(self):
        return self._backingStore

    def lookup(self, ctx, entityClass, index, entityKey):
        return self._backingStore.lookupByIndex(entityClass, index, entityKey)

    def store(self, ctx, entity):
        self._backingStore.store(entity.__class__.__name__, entity)


# Pluggable backing store API
class BackingStore(object):

    def lookupByIndex(self, entityType, index, enitityId):
        raise NotImplemented()

    def store(self, entityType, enitity):
        raise NotImplemented()


# Backing store implementation based on nested dictionaries
class DictionaryBackingStore(BackingStore):
    _entitiesByIndex = defaultdict(partial(defaultdict, dict))

    def lookupByIndex(self, entityType, index, enitityId):
        return self._entitiesByIndex[entityType].get(index).get(enitityId)

    def store(self, entityType, entity):
        indexes = entity.Indexes
        for index in indexes:
            self._entitiesByIndex[entityType][index][getattr(entity, index)] = entity

    def toJSON(self):
        class RecordEncoder(json.JSONEncoder):
            def default(self, o):
                return o.toDict()

        return json.dumps(self._entitiesByIndex, cls=RecordEncoder)

    def fromJSON(self, jsonIn):
        from pydoc import locate
        def object_hook(obj):
            if '__type__' in obj:
                obj = record.HistoricalRecord.fromDict(obj)
            return obj

        d = json.loads(jsonIn, object_hook=object_hook)
        self._entitiesByIndex.clear()

        for k, v in d.items():
            self._entitiesByIndex[k].update(v)


class RedisBackingStore(BackingStore):
    pass


class CassandraBackingStore(BackingStore):
    pass


service_gateway.Registry.registerService(EntityService(DictionaryBackingStore()))

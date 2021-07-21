import datetime

class HistoricalRecord(object):
    def __init__(self):
        self._creation_time = datetime.datetime.utcnow()
        self._history = {}

    @property
    def CreationTime(self):
        return self._creation_time


class Record(HistoricalRecord):

    pass

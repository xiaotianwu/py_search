import uuid

class IORequest:
    '''it's for KV file'''
    __slots__ = ['type', 'fileName', 'key', 'result',
                 'id', 'retCode', 'finishEvent']

    def __init__(self, requestType, fileName, key):
        self.type = requestType
        self.fileName = fileName
        self.key = key
        self.result = None
        self.id = str(uuid.uuid4())
        self.retCode = 0 # TODO use enum to replace it
        self.finishEvent = None

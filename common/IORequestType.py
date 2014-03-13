import uuid

class IORequest:
    '''it's for KV file'''
    def __init__(self, requestType, fileName,
                 key, fileType = 'UncompressIndex'):
        self.type = requestType
        self.fileName = fileName
        self.key = key
        self.result = None
        self.Id = str(uuid.uuid4())
        self.retCode = 0 # TODO use enum to replace it
        self.finishEvent = None
        self.fileType = fileType

import uuid

class IORequest:
    def __init__(self, requestType, fileName):
        self.type = requestType
        self.fileName = fileName
        self.result = None
        self.finishEvent = None
        self.Id = str(uuid.uuid4())
        self.retCode = 0 # TODO use enum to replace it

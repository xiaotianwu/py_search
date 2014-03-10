class IORequest:
    def __init__(self, requestId, requestType, fileName):
        self.Id = requestId
        self.Type = requestType
        self.fileName = fileName
        self.result = None
        self.retCode = 0 # TODO use enum to replace it

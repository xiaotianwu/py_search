class IORequest:
    def __init__(self, requestType, fileName):
        self.Type = requestType
        self.fileName = fileName
        self.result = None
        self.retCode = 0 # TODO use enum to replace it
        self.Id = None

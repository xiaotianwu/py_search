from common.IORequestType import IORequest

class PlainFileIORequest(IORequest):
    def __init__(self, requestId, requestType, fileName, offset, length):
        IORequest.__init__(self, requestId, requestType, fileName)
        self.offset = offset
        self.length = length

class PlainFileWriter:
    def Write(self, data, name):
        with open(name, 'w') as outputFile:
            outputFile.write(data)

class PlainFileReader:
    def __init__(self):
        self._fileName = None
        self._fileDesc = None

    def Open(self, name):
        self._fileName = name
        self._fileDesc = open(name, 'r')

    def ReadAll(self):
        self._fileDesc.seek(0, 0)
        return self._fileDesc.read()

    def Read(self, offset, length):
        self._fileDesc.seek(offset, 0)
        if length == -1:
            return self._fileDesc.read()
        else:
            return self._fileDesc.read(length)

    def DoRequest(self, ioRequest):
        if not isinstance(ioRequest, PlainFileIORequest):
            raise Exception('not PlainFileIORequest type')
        return self.Read(ioRequest.offset, ioRequest.length)

    def Close(self):
        del self._fileDesc
        self._fileDesc = None
        self._fileName = None

from threading import RLock

from common.Common import Locking
from common.IORequestType import IORequest

class PlainFileIORequest(IORequest):
    def __init__(self, requestType, fileName, offset, length):
        IORequest.__init__(self, requestType, fileName)
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
        self._fileLock = RLock()

    def Open(self, name):
        self._fileName = name
        self._fileDesc = open(name, 'r')

    def ReadAll(self):
        with Locking(self._fileLock):
            self._fileDesc.seek(0, 0)
            data = self._fileDesc.read()
        return data

    def Read(self, offset, length):
        with Locking(self._fileLock):
            self._fileDesc.seek(offset, 0)
            if length == -1:
                data = self._fileDesc.read()
            else:
                data = self._fileDesc.read(length)
        return data

    def DoRequest(self, ioRequest):
        if not isinstance(ioRequest, PlainFileIORequest):
            raise Exception('not PlainFileIORequest type')
        if ioRequest.Type == 'READ':
            return self.Read(ioRequest.offset, ioRequest.length)
        elif ioRequest.Type == 'READALL':
            return self.ReadAll()
        else:
            raise Exception('unsupported request type ' + ioRequest.Type)

    def Close(self):
        del self._fileDesc
        self._fileDesc = None
        self._fileName = None

#!/usr/bin/python

import os

from PlainFile import *

if __name__ == '__main__':
    request = PlainFileIORequest(1, 'READ', 'test', 0, -1)
    assert request.Id == 1
    assert request.Type == 'READ'
    assert request.fileName == 'test'
    assert request.offset == 0
    assert request.length == -1

    writer = PlainFileWriter()
    fileContent = 'abcde'
    writer.Write(fileContent, 'test')
    reader = PlainFileReader()
    reader.Open('test')
    assert reader.ReadAll() == fileContent
    assert reader.Read(1, -1) == fileContent[1:]
    reader.Close()

    os.remove('test')

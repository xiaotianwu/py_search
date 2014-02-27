#!/usr/bin/python

from TermIdMapping import TermIdMappingHandler as handler

if __name__ == '__main__':
    inputFile = 'terms.txt'
    outputFile = '../index_chunk/termIdMapping'
    handler.build_termid_mapping(inputFile, outputFile)
    mapping = handler.read_termid_mapping(outputFile)
    print(mapping)

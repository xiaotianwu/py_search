#!/usr/bin/python

from Common import DirHandler

print DirHandler.get_all_files('.', recursive = True)

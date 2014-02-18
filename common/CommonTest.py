#!/usr/bin/python

from Common import DirHandler
from Common import UrlFileNameConverter

print DirHandler.get_all_files('.', recursive = False)
print DirHandler.get_all_files('.', recursive = True)

print UrlFileNameConverter.url_to_filename('http://www.facebook.com')
print UrlFileNameConverter.filename_to_url('http:^^facebook.com')
print UrlFileNameConverter.filename_to_url('/usr/bin/http:^^facebook.com')

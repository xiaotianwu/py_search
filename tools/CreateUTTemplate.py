#!/usr/bin/python

import os
import sys

def CreateUTCode(utName):
    code =\
'''#!/usr/bin/python
import unittest

class %s(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
''' % utName
    return code

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'please input the test class Name'
    else:
        testClassName = sys.argv[1]
        testFileName = testClassName + '.py'
        print 'create ut file:', testFileName
        with open(testFileName, 'w') as testFile:
            testFile.write(CreateUTCode(testClassName))
        command = 'chmod +x %s' % testFileName
        print command
        os.system(command)

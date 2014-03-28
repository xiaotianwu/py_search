import logging
import logging.config
import os
import os.path
import threading

from Common import Locking


loggingFile = os.environ['PY_SEARCH_ROOT'] + '/config/Logger.conf'
assert os.path.exists(loggingFile) == True 
logging.config.fileConfig(loggingFile)

class Logger:
    __loggers = {}
    __loggersLock = threading.RLock()
    
    @staticmethod
    def Get(name):
        with Locking(Logger.__loggersLock):
            if name not in Logger.__loggers:
                Logger.__loggers[name] = logging.getLogger(name)
        return Logger.__loggers[name]


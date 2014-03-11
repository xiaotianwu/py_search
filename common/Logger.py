import logging
import logging.config
import os
import os.path
import threading

class Logger:
    __loggers = {}
    __loggersLock = threading.RLock()
    __init = False
    __loggingFile = os.environ['PY_SEARCH_ROOT'] + '/config/Logger.conf'
    
    @staticmethod
    def Get(name):
        Logger.__loggersLock.acquire()
        if Logger.__init == False:
            assert os.path.exists(Logger.__loggingFile) == True 
            logging.config.fileConfig(Logger.__loggingFile)
            Logger.__init = True
        if name not in Logger.__loggers:
            Logger.__loggers[name] = logging.getLogger(name)
        Logger.__loggersLock.release()
        return Logger.__loggers[name]

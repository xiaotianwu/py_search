import logging
import logging.config
import threading

class Logger:
    __loggers = {}
    __loggersLock = threading.RLock()
    __init = False
    
    @staticmethod
    def get(name):
        Logger.__loggersLock.acquire()
        if Logger.__init == False:
            logging.config.fileConfig('Logging.conf')
            Logger.__init = True
        if name in Logger.__loggers:
            return Logger.__loggers[name]
        else:
            Logger.__loggers[name] = logging.getLogger(name)
            return Logger.__loggers[name]
        Logger.__loggersLock.release()

from __future__ import annotations
from typing_extensions import Self
from typing import cast
import threading

#logger imports
from .loggerMessageDecorators import LoggerMessageDecorator, SimpleLogger
from .writeLogMessage import WriteLogMessage
from .logLevelEnum import LoglevelEnum
from .logConstants import LogConstants
from .loggerException import LoggerException

class Logger:

    # singleton instance
    __instance : Logger|None = None

    # thread safe lock
    __lock : threading.Lock = threading.Lock()

    # logger decorator
    __loggerMessageDecorator : LoggerMessageDecorator|None = SimpleLogger()

    # write logs strategy
    __writeLoggerStrategy : WriteLogMessage|None = None

    # enable-disable logger
    _isloggerenable: bool = False

    # logger enable globally
    _isgloballoggerenable : bool = True

    #function name for which logger is called
    _funcname: str|None = None
    
    # include log level and function parameter
    __includefunctionname = True
    __includeloglevel = True

    # get logger instance
    def __new__(cls, writeLoggerStrategy :WriteLogMessage , loggerDecorator: LoggerMessageDecorator = SimpleLogger(), includefunctionname : bool = True, includeloglevel : bool = True, isgloballoggerenable: bool = True) -> Self:
        if cls.__instance==None:
            with cls.__lock:
                if cls.__instance==None:
                    cls.__instance = super().__new__(cls)
                    cls.__loggerMessageDecorator = loggerDecorator
                    cls.__includefunctionname = includefunctionname
                    cls.__includeloglevel = includeloglevel
                    cls.__writeLoggerStrategy = writeLoggerStrategy
                    cls._isgloballoggerenable = isgloballoggerenable
        return cast(Self, cls.__instance)
    
    @staticmethod
    def log(msg: str, level: LoglevelEnum | None = None):
        # get logger instance
        loggerinstance = Logger.__instance
        # check if it is none if yes then raise Exception
        if loggerinstance==None:
            raise LoggerException("Logger has not been initialized. Call initLogger() before using it.")
        # see if logger decorator is passed or not if instance is intialized then it is passed for sure
        if loggerinstance.__loggerMessageDecorator:
            # see if is logger enabled or not
            if loggerinstance._isloggerenable:
                # create a json object for getting logging details
                loggerjson : dict[str, str] = {}
                loggerjson[LogConstants.LOG_MESSAGE] = msg
                # include the loglevel in the log
                if loggerinstance.__includeloglevel:
                    if level==None:
                        raise LoggerException("Set includeLogLevel to false, or include the log level in log message.")
                    loggerjson[LogConstants.LOG_LEVEL] = level.value
                # include the function name in the log
                if loggerinstance.__includefunctionname:
                    if loggerinstance._funcname==None:
                        raise LoggerException("funcName is required. Please provide a valid function name.")
                    loggerjson[LogConstants.LOG_FUNCTION_NAME] = loggerinstance._funcname
                # send it logger decorator
                loggerjson = loggerinstance.__loggerMessageDecorator.getLog(loggerjson=loggerjson)
                #write the log
                if loggerinstance.__writeLoggerStrategy==None:
                    raise LoggerException("writeLoggerStrategy must not be None. Please provide a valid log writing strategy.")
                loggerinstance.__writeLoggerStrategy.writelog(loggerjson)



# test it
# implement docker strategy
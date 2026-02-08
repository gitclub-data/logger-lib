from __future__ import annotations
from typing_extensions import Self
from typing import cast
import threading

#logger imports
from .loggerMessageDecorators import LoggerMessageDecorator, SimpleLogger
from .writeLogMessage import WriteLogMessage
from .logLevelEnum import LoglevelEnum
from .logConstants import LogConstants
from .loggerException import LoggerException, LoggerExceptionMessageConstant

class Logger:
    """
    Thread-safe Singleton Logger that serves as the central entry point for
    application-wide logging.

    This logger supports configurable log levels, global and function-level
    enable/disable flags, and optional inclusion of function names and log
    levels in log messages.

    The logger uses the Strategy pattern to determine where logs are written
    (e.g., console, file, external service) and the Decorator pattern to
    control which metadata is included in each log message.

    Attributes:
        _instance (Logger | None):
            Private singleton instance of the Logger.

        __lock (threading.Lock):
            Lock used to ensure thread-safe singleton initialization.

        __loggerMessageDecorator (LoggerMessageDecorator):
            Determines which parameters (such as timestamp, function name,
            and log level) are included when constructing log messages.

        __writeLoggerStrategy (WriteLogMessage):
            Strategy responsible for writing log messages and determining
            their destination.

        _isfunctionlevel_enable (dict):
            Controls whether logging is enabled for the current function or
            execution context.

        _isGlobalLoggerEnabled (bool):
            Controls whether logging is enabled globally across the application.

        _thread_functionname (dict):
            current function thread id and attached functionname with it.

        __includeFunctionName (bool):
            Global flag indicating whether function names should be included
            in log messages.

        __includeLogLevel (bool):
            Global flag indicating whether log levels should be included
            in log messages.
    """

    # singleton instance
    _instance : Logger|None = None

    # thread safe lock
    __lock : threading.Lock = threading.Lock()

    # logger decorator
    __loggerMessageDecorator : LoggerMessageDecorator|None = SimpleLogger()

    # write logs strategy
    __writeLoggerStrategy : WriteLogMessage|None = None

    # thread-level-function-name
    _thread_functionname : dict = {} # threadid : functionid

    # function-level logger
    _isfunctionlevel_enable : dict = {} # function_entry : enable_disable

    # logger enable globally
    _isgloballoggerenable : bool = True

    # include log level and function parameter
    __includefunctionname = True
    __includeloglevel = True

    # get logger instance
    def __new__(cls, writeLoggerStrategy :WriteLogMessage, loggerDecorator: LoggerMessageDecorator = SimpleLogger(), 
                includefunctionname : bool = True, 
                includeloglevel : bool = True, isgloballoggerenable: bool = True) -> Self:
        if cls._instance==None:
            with cls.__lock:
                if cls._instance==None:
                    cls._instance = super().__new__(cls)
                    cls.__loggerMessageDecorator = loggerDecorator
                    cls.__includefunctionname = includefunctionname
                    cls.__includeloglevel = includeloglevel
                    cls.__writeLoggerStrategy = writeLoggerStrategy
                    cls._isgloballoggerenable = isgloballoggerenable
        return cast(Self, cls._instance)     

    @classmethod
    def log(cls, msg: str, level: LoglevelEnum | None = None):
        """
            Logs a message with the specified log level.

            This method evaluates the current logging configuration (global and
            function-level settings) to determine:
            - Whether the log should be written or ignored
            - Which metadata should be included in the log message
            - Where the log should be written based on the configured write strategy

            Args:
                msg (str):
                    The log message provided by the caller.

                level (LogLevelEnum):
                    The severity level of the log message.
        """
        loggerinstance = cls._instance
        
        thread_id = threading.get_ident()
        # check if it is none if yes then raise Exception
        if loggerinstance==None:
            raise LoggerException(LoggerExceptionMessageConstant.LOGGER_INSTANTIATION_EXCEPTION)
        
        # see if logger decorator is passed or not if instance is intialized then it is passed for sure
        if cls.__loggerMessageDecorator:

            # check if global logger enabled or not
            if cls._isgloballoggerenable:
            
                # get the function id
                if thread_id not in cls._thread_functionname:
                    raise LoggerException(LoggerExceptionMessageConstant.LOGGER_DECORATOR_REQUIRED)
                functionid = cls._thread_functionname[thread_id]
                
                # checking if function id is present to tell the function level logger enabled or not
                if functionid not in cls._isfunctionlevel_enable:
                    raise LoggerException(LoggerExceptionMessageConstant.LOGGER_FUNCTION_ID_IS_MISSING)
                
                # checking if function level log is enabled or not
                if cls._isfunctionlevel_enable[functionid]:    
                    # create a json object for getting logging details
                    loggerjson : dict[str, str] = {}
                    loggerjson[LogConstants.LOG_MESSAGE] = msg
                    
                    # include the loglevel in the log
                    if cls.__includeloglevel:
                        if level==None:
                            raise LoggerException(LoggerExceptionMessageConstant.LOGGER_INCLUDE_LOG_LEVEL_EXCEPTION)
                        loggerjson[LogConstants.LOG_LEVEL] = level.value
                    
                    # include the function name in the log
                    if cls.__includefunctionname:
                        if thread_id not in cls._thread_functionname:
                            raise LoggerException(LoggerExceptionMessageConstant.LOGGER_INCLUDE_LOG_FUNCTION_NAME_EXCEPTION)
                        loggerjson[LogConstants.LOG_FUNCTION_NAME] = functionid
                    
                    # send it logger decorator
                    loggerjson = cls.__loggerMessageDecorator.getLog(loggerjson=loggerjson)
                    
                    #write the log
                    if cls.__writeLoggerStrategy==None:
                        raise LoggerException(LoggerExceptionMessageConstant.WRITING_LOG_STRATEGY_NOT_PROVIDED_EXCEPTION)
                    
                    cls.__writeLoggerStrategy.writelog(loggerjson)

# test it
# implement docker strategy
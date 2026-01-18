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
        __instance (Logger | None):
            Private singleton instance of the Logger.

        __lock (threading.Lock):
            Lock used to ensure thread-safe singleton initialization.

        __loggerMessageDecorator (LoggerMessageDecorator):
            Determines which parameters (such as timestamp, function name,
            and log level) are included when constructing log messages.

        __writeLoggerStrategy (WriteLogMessage):
            Strategy responsible for writing log messages and determining
            their destination.

        _isLoggerEnabled (bool):
            Controls whether logging is enabled for the current function or
            execution context.

        _isGlobalLoggerEnabled (bool):
            Controls whether logging is enabled globally across the application.

        _funcName (str | None):
            Name of the function for which the log message is being generated.

        __includeFunctionName (bool):
            Global flag indicating whether function names should be included
            in log messages.

        __includeLogLevel (bool):
            Global flag indicating whether log levels should be included
            in log messages.
    """

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
                    if cls._isgloballoggerenable:
                        cls._isloggerenable = True
        return cast(Self, cls.__instance)

    @classmethod
    def _setUpDefaultValues(cls):
        cls.__instance = None
        cls.__loggerMessageDecorator = SimpleLogger()
        cls.__writeLoggerStrategy = None
        cls._isloggerenable = False
        cls._isgloballoggerenable = True
        cls._funcname = None
        cls.__includefunctionname = True
        cls.__includeloglevel = True

    @staticmethod
    def log(msg: str, level: LoglevelEnum | None = None):
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
        # get logger instance
        loggerinstance = Logger.__instance
        # check if it is none if yes then raise Exception
        if loggerinstance==None:
            raise LoggerException(LoggerExceptionMessageConstant.LOGGER_INSTANTIATION_EXCEPTION)
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
                        raise LoggerException(LoggerExceptionMessageConstant.LOGGER_INCLUDE_LOG_LEVEL_EXCEPTION)
                    loggerjson[LogConstants.LOG_LEVEL] = level.value
                # include the function name in the log
                if loggerinstance.__includefunctionname:
                    if loggerinstance._funcname==None:
                        raise LoggerException(LoggerExceptionMessageConstant.LOGGER_INCLUDE_LOG_FUNCTION_NAME_EXCEPTION)
                    loggerjson[LogConstants.LOG_FUNCTION_NAME] = loggerinstance._funcname
                # send it logger decorator
                loggerjson = loggerinstance.__loggerMessageDecorator.getLog(loggerjson=loggerjson)
                #write the log
                if loggerinstance.__writeLoggerStrategy==None:
                    raise LoggerException(LoggerExceptionMessageConstant.WRITING_LOG_STRATEGY_NOT_PROVIDED_EXCEPTION)
                loggerinstance.__writeLoggerStrategy.writelog(loggerjson)

# test it
# implement docker strategy
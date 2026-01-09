from typing import Protocol
from datetime import datetime, timezone
from typing import override

from .logConstants import LogConstants

class LoggerMessageDecorator(Protocol):
    def getLog(self, loggerjson: dict[str, str]) -> dict[str, str]:
        ...

class SimpleLogger(LoggerMessageDecorator):

    def __init__(self, additionallogger: LoggerMessageDecorator|None = None) -> None:
        super().__init__()
        self.__additionallogger : LoggerMessageDecorator|None = additionallogger

    @override
    def getLog(self, loggerjson: dict[str, str]) -> dict[str, str]:
        if self.__additionallogger is None:
            return loggerjson
        return self.__additionallogger.getLog(loggerjson)

class LoggerWithTimeStamp(LoggerMessageDecorator):

    def __init__(self, localtimezone : timezone = timezone.utc, additionallogger: LoggerMessageDecorator|None = None) -> None:
        super().__init__()
        self.__additionallogger : LoggerMessageDecorator|None = additionallogger
        self.__localtimezone = localtimezone
    
    @override
    def getLog(self, loggerjson: dict[str, str]) -> dict[str, str]:
        loggerjson[LogConstants.LOG_TIMESTAMP] = str(datetime.now(self.__localtimezone))
        if self.__additionallogger is None:
            return loggerjson
        return self.__additionallogger.getLog(loggerjson)
    
class LoggerWithServiceName(LoggerMessageDecorator):

    def __init__(self, serviceName : str, additionallogger: LoggerMessageDecorator|None = None) -> None:
        super().__init__()
        self.__additionallogger : LoggerMessageDecorator|None = additionallogger
        self.__serviceName : str = serviceName
    
    @override
    def getLog(self, loggerjson: dict[str, str]) -> dict[str, str]:
        loggerjson[LogConstants.LOG_SERVICE_NAME] = self.__serviceName
        if self.__additionallogger is None:
            return loggerjson
        return self.__additionallogger.getLog(loggerjson)
    

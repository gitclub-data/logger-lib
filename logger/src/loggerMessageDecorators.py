from typing import Protocol
from datetime import datetime, timezone, tzinfo
from typing import override

from .logConstants import LogConstants

class LoggerMessageDecorator(Protocol):
    """
        Interface responsible for processing a JSON object.

        This interface accepts a dic structure, enriches it by adding
        the required parameters, and returns the updated dic.
    """
    def getLog(self, loggerjson: dict[str, str]) -> dict[str, str]:
        """
            Abstract method for processing a log message dictionary.

            Subclasses must implement this method to enrich the provided dictionary
            with the required log parameters and return the updated log message.

            Args:
                loggerjson (dict[str, str]):
                    Dictionary representing the log message to be processed.

            Returns:
                str: Updated logger dictionary containing the required log parameters.
        """
        ...

class SimpleLogger(LoggerMessageDecorator):
    """
        Concrete implementation of the LoggerMessageDecorator interface.

        This implementation returns the provided logger JSON as-is and serves as
        the base decorator in the logging system. Its primary purpose is to act
        as a foundation for extending log message construction by allowing
        additional decorators to add more parameters to the log message.

        Attributes:
            __additionalLogger (LoggerMessageDecorator):
                Reference to another LoggerMessageDecorator instance, enabling
                chaining of decorators to incrementally add parameters to the
                logger JSON.
    """

    def __init__(self, additionallogger: LoggerMessageDecorator|None = None) -> None:
        super().__init__()
        self.__additionallogger : LoggerMessageDecorator|None = additionallogger

    @override
    def getLog(self, loggerjson: dict[str, str]) -> dict[str, str]:
        """
            Implements the `get_log` method, optionally passing the logger dictionary
            to the next decorator to add more parameters. If no further decorator is
            provided, it simply returns the current logger dictionary.

            Args:
                loggerjson (dict[str, str]):
                    Dictionary representing the log message to be processed.

            Returns:
                dict[str, str]: Updated logger dictionary containing the required log parameters.
        """
        if self.__additionallogger is None:
            return loggerjson
        return self.__additionallogger.getLog(loggerjson)

class LoggerWithTimeStamp(LoggerMessageDecorator):
    """
        Concrete implementation of the LoggerMessageDecorator interface.

        This class implements the `get_log` method by adding a timestamp parameter
        to the logger JSON and passing it to the next decorator, if provided, to
        add additional parameters.

        Attributes:
            __additionalLogger (LoggerMessageDecorator):
                Reference to another LoggerMessageDecorator instance, enabling
                chaining of decorators to incrementally add parameters to the
                logger JSON.

            __localTimezone (timezone):
                Timezone used for the timestamp in the logger JSON, representing
                the user's desired local time.
    """

    def __init__(self, localtimezone : tzinfo = timezone.utc, additionallogger: LoggerMessageDecorator|None = None) -> None:
        super().__init__()
        self.__additionallogger : LoggerMessageDecorator|None = additionallogger
        self.__localtimezone = localtimezone
    
    @override
    def getLog(self, loggerjson: dict[str, str]) -> dict[str, str]:
        """
            Implements the `get_log` method by adding a timestamp to the logger dictionary
            and optionally passing it to the next decorator to include additional parameters.
            If no further decorator is provided, the current logger dictionary is returned as-is.

            Args:
                loggerjson (dict[str, str]):
                    Dictionary representing the log message to be processed.

            Returns:
                dict[str, str]: Updated logger dictionary containing the required log parameters.
        """
        loggerjson[LogConstants.LOG_TIMESTAMP] = str(datetime.now(self.__localtimezone))
        if self.__additionallogger is None:
            return loggerjson
        return self.__additionallogger.getLog(loggerjson)
    
class LoggerWithServiceName(LoggerMessageDecorator):
    """
        Concrete implementation of the LoggerMessageDecorator interface.

        This class implements the `get_log` method by adding a `serviceName` parameter
        to the logger JSON and passing it to the next decorator, if provided, to
        add additional parameters.

        Attributes:
            __additionalLogger (LoggerMessageDecorator):
                Reference to another LoggerMessageDecorator instance, enabling
                chaining of decorators to incrementally add parameters to the
                logger JSON.

            __serviceName (str):
                Name of the service provided by the caller, used to identify
                which service is generating the log.
    """
    def __init__(self, serviceName : str, additionallogger: LoggerMessageDecorator|None = None) -> None:
        super().__init__()
        self.__additionallogger : LoggerMessageDecorator|None = additionallogger
        self.__serviceName : str = serviceName
    
    @override
    def getLog(self, loggerjson: dict[str, str]) -> dict[str, str]:
        """
            Implements the `get_log` method by adding the servicename to the logger dictionary
            and optionally passing it to the next decorator to include additional parameters.
            If no further decorator is provided, the current logger dictionary is returned as-is.

            Args:
                loggerjson (dict[str, str]):
                    Dictionary representing the log message to be processed.

            Returns:
                dict[str, str]: Updated logger dictionary containing the required log parameters.
        """
        loggerjson[LogConstants.LOG_SERVICE_NAME] = self.__serviceName
        if self.__additionallogger is None:
            return loggerjson
        return self.__additionallogger.getLog(loggerjson)
    

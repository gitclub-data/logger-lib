from typing import Final

class LoggerException(Exception):
    """
        Custom exception class for the logger module.

        This exception can be raised for errors related to logging operations,
        such as configuration issues, invalid log data, or other logging-specific failures.
    """
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class LoggerExceptionMessageConstant:
    """
        Provides a centralized collection of exception message constants used by LoggerException.
    """
    LOGGER_INSTANTIATION_EXCEPTION: Final = "Logger has not been initialized. Call initLogger() before using it."
    LOGGER_INCLUDE_LOG_LEVEL_EXCEPTION: Final = "Set includeLogLevel to false, or include the log level in log message."
    LOGGER_INCLUDE_LOG_FUNCTION_NAME_EXCEPTION: Final = "funcName is required. Please attach a valid function name."
    WRITING_LOG_STRATEGY_NOT_PROVIDED_EXCEPTION: Final = "writeLoggerStrategy must not be None. Please provide a valid log writing strategy."
    LOGGER_FUNCTION_ID_IS_MISSING : Final = "functionid must be needed to determine if the function is enabled or disabled for logging."
    LOGGER_DECORATOR_REQUIRED : Final = "gaurav logger Decorator is required to attach to use the log function."



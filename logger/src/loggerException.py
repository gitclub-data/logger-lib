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
    LOGGER_INCLUDE_LOG_FUNCTION_NAME_EXCEPTION: Final = "funcName is required. Please provide a valid function name."
    WRITING_LOG_STRATEGY_NOT_PROVIDED_EXCEPTION: Final = "writeLoggerStrategy must not be None. Please provide a valid log writing strategy."



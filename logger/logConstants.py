from typing import Final

class LogConstants:
    """
        Defines logging-related constants used to identify the type of log entry.

        These constants represent standard keys used across the logging system
        to describe log metadata and content.

        Attributes:
            LOG_SERVICE_NAME: Name of the service generating the log.
            LOG_FUNCTION_NAME: Name of the function where the log was created.
            LOG_TIMESTAMP: Timestamp when the log was generated.
            LOG_LEVEL: Severity level of the log.
            LOG_MESSAGE: Actual log message content.
    """
    LOG_SERVICE_NAME: Final = 'servicename'
    LOG_FUNCTION_NAME: Final = 'function_name' 
    LOG_TIMESTAMP : Final = 'timestamp'
    LOG_LEVEL: Final = 'level'
    LOG_MESSAGE: Final = 'message'    
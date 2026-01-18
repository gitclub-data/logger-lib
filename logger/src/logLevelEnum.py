from enum import Enum

# logger enum
class LoglevelEnum(Enum):
    """
        Defines constants representing the severity levels of logs.

        These levels are used to classify log messages based on their importance
        and urgency.

        Attributes:
            DEBUG: Detailed information for diagnosing issues.
            INFO: General information about application flow.
            WARNING: Indication of a potential issue.
            ERROR: Error events that may allow the application to continue running.
            CRITICAL: Severe errors indicating the application may be unable to continue.
    """
    DEBUG = 'DEBUG'
    INFO = 'INFO'
    ERROR = 'ERROR'
    WARNING = 'WARNING'
    CRITICAL = 'CRITICAL'
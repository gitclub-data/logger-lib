class LoggerException(Exception):
    """
        Custom exception class for the logger module.

        This exception can be raised for errors related to logging operations,
        such as configuration issues, invalid log data, or other logging-specific failures.
    """
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

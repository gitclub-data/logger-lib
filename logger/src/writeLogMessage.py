from typing import Protocol, override
from collections import deque
import threading

from .logConstants import LogConstants
import atexit

class WriteLogMessage(Protocol):
    """
        Defines an interface for writing logs to a storage backend.

        Implementations of this interface are responsible for persisting log
        records to a specific storage mechanism (e.g., file system, database,
        or remote logging service).
    """
    def writelog(self, loggerjson: dict[str, str]) -> None:
        """
            Persists a log record to the underlying storage.

            The implementation of this method is responsible for writing the
            provided log data to the configured storage backend.

            Args:
                logger_json (dict[str, str]): Dictionary containing log metadata
                    and the actual log message.
        """
        ...

class FileWriterLog(WriteLogMessage):
    """
        Synchronous file-based implementation of the log writer interface.

        This implementation persists log records directly to the file system
        in a synchronous manner. While it provides reliable log storage, it may
        negatively impact application performance due to blocking I/O.

        This implementation is best suited for applications with low log volume
        or scenarios where log reliability is more important than performance.

        Attributes:
            __logfilepath (str): File path provided by the user where logs should be stored.
            __logconstant (list[str]): Sequence of log fields defining the order in which
                log data is written to the file.
            __lock (threading.Lock): Lock to ensure thread-safe writing when multiple
                threads attempt to write to the same file simultaneously.
    """
    def __init__(self, logfilepath: str) -> None:
        super().__init__()
        self.__logfilepath : str = logfilepath
        self.__logsequence : list[str] = [LogConstants.LOG_SERVICE_NAME, LogConstants.LOG_FUNCTION_NAME, LogConstants.LOG_TIMESTAMP, LogConstants.LOG_LEVEL, LogConstants.LOG_MESSAGE]
        self.__lock = threading.Lock()
    
    @override
    def writelog(self, loggerjson: dict[str, str])-> None:
        """
            Persist a log record to the file storage at the configured file path.

            This method formats the provided `logger_json` using the internal
            log sequence and attempts to write it to the file specified by `__logfilepath`.
            Thread safety is ensured using an internal lock to prevent concurrent
            write conflicts when multiple threads attempt to log simultaneously.

            If an I/O error occurs during writing, it is caught and printed
            to standard output instead of raising an exception, allowing
            the application to continue running.

            Args:
                logger_json (dict[str, str]): Dictionary containing log metadata
                    and the actual log message.
        """
        message = self.__preparemsg(loggerjson)
        with self.__lock:
            try:
                with open(self.__logfilepath, "a") as logfile: 
                    logfile.write(message)
            except Exception as e:
                print(f"[FileWriterLog] Failed to write log: {e}")

    
    def __preparemsg(self, loggerjson: dict[str, str]) -> str:
        """
            Prepare a formatted log string from the provided log dictionary.

            This method uses `logger_json` and the internal `__logsequence` to
            construct the log string in the correct order for writing to the file.

            Args:
                logger_json (dict[str, str]): Dictionary containing log metadata
                    and the actual log message.

            Returns:
                str: Formatted log string ready to be written to the log file.
        """
        parts = [loggerjson[key] for key in self.__logsequence if key in loggerjson]
        message = ' || '.join(parts) + '\n'
        return message

# give logs in a queue to user to use themself any why they want
class WriteLogsInQueue(WriteLogMessage):
    """
        Synchronous implementation of the log writer interface using a user-provided queue.

        This implementation writes log records into a queue supplied by the user.
        The user can then consume the queue to transfer logs into any storage
        mechanism according to their own implementation.

        Attributes:
            __logqueue (deque[dict[str, str]]): User-provided queue to store log records.
            __lock (threading.Lock): Lock to ensure thread-safe writing when multiple
                threads attempt to write to the same queue simultaneously.

        Note:
            Be mindful of memory constraints, as the queue stores logs in memory
            before they are processed.
    """
    def __init__(self, logqueue : deque[dict[str, str]]) -> None:
        super().__init__()
        self.__logqueue : deque[dict[str, str]] = logqueue
        self.__lock = threading.Lock()
    
    @override
    def writelog(self, loggerjson: dict[str, str]) -> None:
        with self.__lock:
            self.__logqueue.append(loggerjson)


class AsyncFileWriterLog(WriteLogMessage):
    """
        Asynchronous file-based implementation of the log writer interface.

        This implementation persists log records to the file system asynchronously
        using an internal queue. Log entries are added to the queue and processed
        by a background daemon thread, allowing the application to continue
        without blocking on I/O operations. 
        
        While this improves performance,users should be aware of memory constraints 
        since the queue temporarily stores logs before writing them to disk.

        Attributes:
            __logfilepath (str): File path provided by the user where logs should be stored.
            __logconstant (list[str]): Sequence of log fields defining the order in which
                log data is written to the file.
            __logdeque (deque[dict[str, str]]): Internal queue storing logs before they
                are written to the file.
            _stop_daemon_work (bool): Flag indicating that the daemon thread should
                stop processing logs (used during flushing at exit).
            __condition (threading.Condition): Condition variable used for locking
                and waiting when the queue is empty to reduce resource usage.
            __process_log_thread (threading.Thread): Daemon thread that continuously
                processes logs from the queue as they arrive.
    """
    def __init__(self, logfilepath: str) -> None:
        super().__init__()
        self.__logfilepath : str = logfilepath
        self.__logsequence : list[str] = [LogConstants.LOG_SERVICE_NAME, LogConstants.LOG_FUNCTION_NAME, LogConstants.LOG_TIMESTAMP, LogConstants.LOG_LEVEL, LogConstants.LOG_MESSAGE]
        self.__logdeque = deque()

        self.__stop_daemon_work : bool = False
        atexit.register(self.__flush_and_exit)

        self.__condition = threading.Condition()
        self.__process_log_thread = threading.Thread(target=self.__processlog, daemon=True)
        self.__process_log_thread.start()
        
    @override
    def writelog(self, loggerjson: dict[str, str])-> None:
        """
            Writes the logs in the queue and notify the deamon thread to process the incoming logs.
            
            Args:
                logger_json (dict[str, str]): Dictionary containing log metadata and the actual log message.
        """
        with self.__condition:
            self.__logdeque.append(loggerjson)
            self.__condition.notify()  # wake up the thread

    def __processlog(self) -> None:
        """
            Waits for notification using the internal condition variable and writes
            queued log records to the file.

            This method is typically run by a background thread that continuously
            processes logs from the internal queue as they become available.
        """
        while True:
            with self.__condition:
                while not self.__logdeque and not self.__stop_daemon_work:
                    self.__condition.wait(timeout=5)  # wait until a log is added
                if self.__stop_daemon_work:
                    return
            self.__writeloginactualfile()
            
    def __writeloginactualfile(self) -> None:
        """
            Collects logs from the internal queue and uses the `prepare_log_string`
            method to format them before writing to the file.

            This method ensures that all queued log records are processed in order
            and written to the file according to the defined log sequence.
        """
        logs_to_write = []
        with self.__condition:
            while self.__logdeque:
                log_json = self.__logdeque.popleft()
                logs_to_write.append(log_json)
        
        messages : list[str] = [self.__preparemsg(log_json) for log_json in logs_to_write]
        self.__write_to_file(messages)

    def __write_to_file(self, messages: list[str]) -> None:
        """
            Writes log records to the file and prints an error message if an I/O error occurs.

            This method attempts to persist the log entry to the configured file path.
            If an IOError or file access error occurs, it is caught and printed to
            the standard output to prevent the application from crashing.
        """
        try:
            with open(self.__logfilepath, "a") as logfile:
                logfile.writelines(messages)
        except Exception as e:
            print(f"[AsyncFileWriterLog] Failed to write log: {e}")

    def __flush_and_exit(self):
        """
            Flushes any remaining log records from the queue to the file upon application exit.

            This method ensures that all logs stored in the internal queue are written
            to the file before the application terminates, preventing data loss.
        """
        with self.__condition:
            self.__stop_daemon_work = True
            self.__condition.notify_all()

        while self.__logdeque:
            self.__writeloginactualfile()

    def __preparemsg(self, loggerjson: dict[str, str]) -> str:
        """
            Prepare a formatted log string from the provided log dictionary.

            This method uses `logger_json` and the internal `__logsequence` to
            construct the log string in the correct order for writing to the file.

            Args:
                logger_json (dict[str, str]): Dictionary containing log metadata
                    and the actual log message.

            Returns:
                str: Formatted log string ready to be written to the log file.
        """
        parts = [loggerjson[key] for key in self.__logsequence if key in loggerjson]
        message = ' || '.join(parts) + '\n'
        return message
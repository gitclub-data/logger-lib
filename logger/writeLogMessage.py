from typing import Protocol, override
from collections import deque
import threading

from .logConstants import LogConstants
import atexit

class WriteLogMessage(Protocol):
    def writelog(self, loggerjson: dict[str, str]) -> None:
        ...

class FileWriterLog(WriteLogMessage):
    def __init__(self, logfilepath: str) -> None:
        super().__init__()
        self.__logfilepath = logfilepath
        self.__logsequence = [LogConstants.LOG_SERVICE_NAME, LogConstants.LOG_FUNCTION_NAME, LogConstants.LOG_TIMESTAMP, LogConstants.LOG_LEVEL, LogConstants.LOG_MESSAGE]
        self.__lock = threading.Lock()
    
    @override
    def writelog(self, loggerjson: dict[str, str])-> None:
        # Open file in append mode 
        message = self.__preparemsg(loggerjson)
        with self.__lock:
            with open(self.__logfilepath, "a") as logfile: 
                logfile.write(message)
    
    def __preparemsg(self, loggerjson: dict[str, str]) -> str:
        parts = [loggerjson[key] for key in self.__logsequence if key in loggerjson]
        message = ' || '.join(parts) + '\n'
        return message

# give logs in a queue to user to use themself any why they want
class WriteLogsInQueue(WriteLogMessage):
    def __init__(self, logqueue : deque[dict[str, str]]) -> None:
        super().__init__()
        self.__logqueue : deque[dict[str, str]] = logqueue
        self.__lock = threading.Lock()
    
    @override
    def writelog(self, loggerjson: dict[str, str]) -> None:
        with self.__lock:
            self.__logqueue.append(loggerjson)


class AsyncFileWriterLog(WriteLogMessage):
    def __init__(self, logfilepath: str) -> None:
        super().__init__()
        self.__logfilepath = logfilepath
        self.__logsequence = [LogConstants.LOG_SERVICE_NAME, LogConstants.LOG_FUNCTION_NAME, LogConstants.LOG_TIMESTAMP, LogConstants.LOG_LEVEL, LogConstants.LOG_MESSAGE]
        self.__logdeque = deque()

        self.stop_daemon_work = False
        atexit.register(self.__flush_and_exit)

        self.__condition = threading.Condition()
        self.__process_log_thread = threading.Thread(target=self.__processlog, daemon=True)
        self.__process_log_thread.start()
        
    @override
    def writelog(self, loggerjson: dict[str, str])-> None:
        # Open file in append mode 
        with self.__condition:
            self.__logdeque.append(loggerjson)
            self.__condition.notify()  # wake up the thread

    def __processlog(self):
        while True:
            with self.__condition:
                while not self.__logdeque and not self.stop_daemon_work:
                    self.__condition.wait(timeout=1)  # wait until a log is added
                if self.stop_daemon_work:
                    return
            self.__writeloginactualfile()
            
    def __writeloginactualfile(self) -> None:
        logs_to_write = []
        with self.__condition:
            while self.__logdeque:
                log_json = self.__logdeque.popleft()
                logs_to_write.append(log_json)
        
        messages : list[str] = [self.__preparemsg(log_json) for log_json in logs_to_write]
        self.__write_to_file(messages)

    def __write_to_file(self, messages: list[str]) -> None:
        try:
            with open(self.__logfilepath, "a") as logfile:
                logfile.writelines(messages)
        except Exception as e:
            print(f"[AsyncFileWriterLog] Failed to write log: {e}")

    def __flush_and_exit(self):
        with self.__condition:
            self.stop_daemon_work = True
            self.__condition.notify_all()

        while self.__logdeque:
            self.__writeloginactualfile()

    def __preparemsg(self, loggerjson: dict[str, str]) -> str:
        parts = [loggerjson[key] for key in self.__logsequence if key in loggerjson]
        message = ' || '.join(parts) + '\n'
        return message
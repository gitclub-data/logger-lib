import os
import time
import pytest

from collections import deque
from logger.src.writeLogMessage import WriteLogMessage, FileWriterLog, WriteLogsInQueue, AsyncFileWriterLog
from logger.src.logConstants import LogConstants
from logger.src.logLevelEnum import LoglevelEnum

from unittest.mock import patch

class TestWriteLogMessageFileWriteLogMessage:

    def setup_method(self):
        self.file_path = 'file.txt'
        self.fileWriteLogger : WriteLogMessage = FileWriterLog(self.file_path)
        self.loggerjson = { LogConstants.LOG_SERVICE_NAME : 'Service1',
                      LogConstants.LOG_FUNCTION_NAME : 'function1',
                      LogConstants.LOG_TIMESTAMP: '2026-01-29 12:02:41.641322+00:00',
                      LogConstants.LOG_LEVEL : LoglevelEnum.DEBUG.value,
                      LogConstants.LOG_MESSAGE: 'log message found' }

    def test_preparemsg_returns_correct_msg_sequence(self):
        message = self.fileWriteLogger._FileWriterLog__preparemsg(self.loggerjson)
        real_message = f"Service1 || function1 || 2026-01-29 12:02:41.641322+00:00 || {LoglevelEnum.DEBUG.value} || log message found\n"
        assert message == real_message
    
    def test_writelog_write_into_correct_file_path(self):

        message = f"Service1 || function1 || 2026-01-29 12:02:41.641322+00:00 || {LoglevelEnum.DEBUG.value} || log message found\n"
        with patch.object(self.fileWriteLogger, '_FileWriterLog__preparemsg',
                          return_value = message):
            self.fileWriteLogger.writelog(self.loggerjson)
        assert os.path.exists(self.file_path)
        
        with open(self.file_path, 'r') as f:
            file_content = f.read()
        
        assert file_content==message

    def teardown_method(self):
        if os.path.exists(self.file_path):
            os.remove(self.file_path)
            
class TestWriteLogMessageWriteLogsInQueue:
    def setup_method(self):
        self.deque = deque([])
        self.fileWriteLogger : WriteLogMessage = WriteLogsInQueue(self.deque)
        self.loggerjson = { LogConstants.LOG_SERVICE_NAME : 'Service1',
                      LogConstants.LOG_FUNCTION_NAME : 'function1',
                      LogConstants.LOG_TIMESTAMP: '2026-01-29 12:02:41.641322+00:00',
                      LogConstants.LOG_LEVEL : LoglevelEnum.DEBUG.value,
                      LogConstants.LOG_MESSAGE: 'log message found' }
    
    def test_writelog_write_into_correct_file_path(self):
        self.fileWriteLogger.writelog(self.loggerjson)
        assert self.loggerjson in self.deque
    
class TestWriteLogMessageAsyncFileWriterLog:
    def setup_method(self):
        self.file_path = 'file.txt'
        self.fileWriteLogger : WriteLogMessage = AsyncFileWriterLog(self.file_path)
        self.loggerjson = { LogConstants.LOG_SERVICE_NAME : 'Service1',
                      LogConstants.LOG_FUNCTION_NAME : 'function1',
                      LogConstants.LOG_TIMESTAMP: '2026-01-29 12:02:41.641322+00:00',
                      LogConstants.LOG_LEVEL : LoglevelEnum.DEBUG.value,
                      LogConstants.LOG_MESSAGE: 'log message found' }
    
    def test_preparemsg_returns_correct_msg_sequence(self):
        message = self.fileWriteLogger._AsyncFileWriterLog__preparemsg(self.loggerjson)
        real_message = f"Service1 || function1 || 2026-01-29 12:02:41.641322+00:00 || {LoglevelEnum.DEBUG.value} || log message found\n"
        assert message == real_message
    
    @pytest.mark.xfail(reason="This test can be failed becasue the multiple assertion in it depends upon the multithreading env and sleep duration of the machine")
    def test_writelog_write_into_correct_file_path(self):
        message = f"Service1 || function1 || 2026-01-29 12:02:41.641322+00:00 || {LoglevelEnum.DEBUG.value} || log message found\n"
        with patch.object(self.fileWriteLogger, '_AsyncFileWriterLog__preparemsg',
                          return_value = message):
            self.fileWriteLogger.writelog(self.loggerjson)
        assert self.loggerjson in self.fileWriteLogger._AsyncFileWriterLog__logdeque
        time.sleep(1)
        assert os.path.exists(self.file_path)
        with open(self.file_path, 'r') as f:
            file_content = f.read()
        assert file_content==message

    def teardown_method(self):
        if os.path.exists(self.file_path):
            os.remove(self.file_path)
    

    

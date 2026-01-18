from unittest.mock import patch
from src.logger import Logger
import pytest
import threading
from src.loggerException import LoggerException, LoggerExceptionMessageConstant
from src.logLevelEnum import LoglevelEnum
from src.logConstants import LogConstants

class TestLogger:

    def setup_method(self):
        Logger._setUpDefaultValues()

    def test_LoggerInitialization(self):
        with patch("src.writeLogMessage.FileWriterLog") as MockFileWriterLog:
            mock_writer_log = MockFileWriterLog.return_value 
            
        with patch("src.writeLogMessage.FileWriterLog") as MockFileWriterLog:
            new_mock_writer_log = MockFileWriterLog.return_value 

        logger = Logger(mock_writer_log)
        newlogger = Logger(new_mock_writer_log)
        
        assert logger is newlogger
        
    def test_logger_singleton_thread_safety(self): 
        instances = []
        with patch("src.writeLogMessage.FileWriterLog") as MockFileWriterLog:
            write_strategy = MockFileWriterLog.return_value 

        def create():
            instances.append(Logger(write_strategy))

        threads = [threading.Thread(target=create) for _ in range(20)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert all(inst is instances[0] for inst in instances)
    

    def test_logger_init_only_first_time(self):
        with patch("src.writeLogMessage.FileWriterLog") as MockFileWriterLog:
            write_strategy = MockFileWriterLog.return_value 

        with patch("src.writeLogMessage.FileWriterLog") as MockFileWriterLog:
            other_strategy = MockFileWriterLog.return_value 

        logger1 = Logger(write_strategy, includeloglevel=False)
        logger2 = Logger(other_strategy, includeloglevel=True)

        assert logger1 is logger2

    def test_log_before_init_raises(self):
        with pytest.raises(LoggerException) as logException:
            Logger.log("hello")
        
        assert LoggerExceptionMessageConstant.LOGGER_INSTANTIATION_EXCEPTION in str(logException.value)
    
    def test_log_does_not_happen_if_global_logger_disabled(self):
        # Create a mock write strategy
        with patch("src.writeLogMessage.FileWriterLog") as MockFileWriterLog:
            mock_write_strategy = MockFileWriterLog.return_value 

        # Initialize the logger with global logging disabled
        logger = Logger(
            writeLoggerStrategy=mock_write_strategy,
            includefunctionname=False,
            includeloglevel=False,
            isgloballoggerenable=False
        )

        # Attempt to log a message
        Logger.log("This should not be logged")

        # Assert that writelog was never called
        mock_write_strategy.writelog.assert_not_called()
    
    def test_if_log_level_is_true_and_not_provide_log_level_exception(self):
        # Create a mock write strategy
        with patch("src.writeLogMessage.FileWriterLog") as MockFileWriterLog:
            mock_write_strategy = MockFileWriterLog.return_value 

        with pytest.raises(LoggerException) as logException:
            # Initialize the logger with global logging disabled
            logger = Logger(
                writeLoggerStrategy=mock_write_strategy,
                includeloglevel = True,
                includefunctionname = False
            )

            # Attempt to log a message
            Logger.log("This should not be logged")
        
        assert LoggerExceptionMessageConstant.LOGGER_INCLUDE_LOG_LEVEL_EXCEPTION in str(logException.value)

    def test_if_function_level_is_true_and_not_provide_function_level_exception(self):
        # Create a mock write strategy
        with patch("src.writeLogMessage.FileWriterLog") as MockFileWriterLog:
            mock_write_strategy = MockFileWriterLog.return_value 

        with pytest.raises(LoggerException) as logException:
            # Initialize the logger with global logging disabled
            logger = Logger(
                writeLoggerStrategy=mock_write_strategy,
                includeloglevel = False,
                includefunctionname=True,
            )

            # Attempt to log a message
            Logger.log("This should not be logged")
        
        assert LoggerExceptionMessageConstant.LOGGER_INCLUDE_LOG_FUNCTION_NAME_EXCEPTION in str(logException.value)

    def test_sending_logger_json_to_coresponding_strategy_function_to_write_logs(self):

        # Create a mock write strategy
        with patch("src.writeLogMessage.FileWriterLog") as MockFileWriterLog:
            mock_write_strategy = MockFileWriterLog.return_value 

        logger = Logger(
            writeLoggerStrategy=mock_write_strategy,
        )

        message = "This should not be logged"
        function_name = "function_name_one"
        logger._funcname = function_name

        logger_json = {LogConstants.LOG_LEVEL: LoglevelEnum.DEBUG.value, LogConstants.LOG_MESSAGE: message, LogConstants.LOG_FUNCTION_NAME: function_name}
        Logger.log(message, LoglevelEnum.DEBUG)
        
        mock_write_strategy.writelog.assert_called_once_with(logger_json)

        




        
        

        

        



    


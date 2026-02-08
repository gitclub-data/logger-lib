from unittest.mock import patch
from logger import Logger
import pytest
import threading
from logger.src.loggerException import LoggerException, LoggerExceptionMessageConstant
from logger.src.logLevelEnum import LoglevelEnum
from logger.src.logConstants import LogConstants
from logger.src.loggerMessageDecorators import SimpleLogger

class TestLogger:

    def setup_method(self):
        Logger._instance = None
        Logger._thread_functionname = {}
        Logger._isfunctionlevel_enable = {}
        Logger._isgloballoggerenable = True
        Logger._Logger__loggerMessageDecorator = SimpleLogger()
        Logger._Logger__writeLoggerStrategy = None
        Logger._Logger__includefunctionname = True
        Logger._Logger__includeloglevel = True

    def test_LoggerInitialization(self):
        with patch("logger.src.writeLogMessage.FileWriterLog") as MockFileWriterLog:
            mock_writer_log = MockFileWriterLog.return_value 
            
        with patch("logger.src.writeLogMessage.FileWriterLog") as MockFileWriterLog:
            new_mock_writer_log = MockFileWriterLog.return_value 

        logger = Logger(mock_writer_log)
        newlogger = Logger(new_mock_writer_log)
        
        assert logger is newlogger
        
    def test_logger_singleton_thread_safety(self): 
        instances = []
        with patch("logger.src.writeLogMessage.FileWriterLog") as MockFileWriterLog:
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
        with patch("logger.src.writeLogMessage.FileWriterLog") as MockFileWriterLog:
            write_strategy = MockFileWriterLog.return_value 

        with patch("logger.src.writeLogMessage.FileWriterLog") as MockFileWriterLog:
            other_strategy = MockFileWriterLog.return_value 

        logger1 = Logger(write_strategy, includeloglevel=False)
        logger2 = Logger(other_strategy, includeloglevel=True)

        assert logger1 is logger2

    def test_log_before_init_raises(self):
        with pytest.raises(LoggerException) as logException:
            Logger.log("This should raise an exception.")
        
        assert LoggerExceptionMessageConstant.LOGGER_INSTANTIATION_EXCEPTION in str(logException.value)

    def test_log_does_not_happen_if_global_logger_disabled(self):
        # Create a mock write strategy
        with patch("logger.src.writeLogMessage.FileWriterLog") as MockFileWriterLog:
            mock_write_strategy = MockFileWriterLog.return_value 

        # Initialize the logger with global logging disabled
        logger = Logger(
            writeLoggerStrategy=mock_write_strategy,
            isgloballoggerenable=False
        )

        # Attempt to log a message
        Logger.log("This should not be logged")

        # Assert that writelog was never called
        mock_write_strategy.writelog.assert_not_called()

    def test_if_decorator_is_not_passed_and_used_log_directly_gives_an_exception(self):
        # Create a mock write strategy
        with patch("logger.src.writeLogMessage.FileWriterLog") as MockFileWriterLog:
            mock_write_strategy = MockFileWriterLog.return_value 

        with pytest.raises(LoggerException) as logException:
            # Initialize the logger with global logging disabled
            logger = Logger(
                writeLoggerStrategy=mock_write_strategy,
                includeloglevel = True,
                includefunctionname = False
            )

            def decorated_function():
                    # Attempt to log a message
                    Logger.log("This should not be logged")
                
            decorated_function()
        
        assert LoggerExceptionMessageConstant.LOGGER_DECORATOR_REQUIRED in str(logException.value)

    def test_if_log_level_is_true_and_not_provide_log_level_exception(self):
        # Create a mock write strategy
        with patch("logger.src.writeLogMessage.FileWriterLog") as MockFileWriterLog:
            mock_write_strategy = MockFileWriterLog.return_value 

        with pytest.raises(LoggerException) as logException:
            # Initialize the logger with global logging disabled
            logger = Logger(
                writeLoggerStrategy=mock_write_strategy,
                includeloglevel = True,
                includefunctionname = False
            )

            with patch("logger.src.loggerDecorator.gaurav_logger", lambda func: func) as gaurav_logger:
                @gaurav_logger
                def decorated_function():
                    # Attempt to log a message
                    Logger.log("This should not be logged")
                
                decorated_function()
        
            assert LoggerExceptionMessageConstant.LOGGER_INCLUDE_LOG_LEVEL_EXCEPTION in str(logException.value)

    def test_sending_logger_json_to_coresponding_strategy_function_to_write_logs(self):

        # Create a mock write strategy
        with patch("logger.src.writeLogMessage.FileWriterLog") as MockFileWriterLog:
            mock_write_strategy = MockFileWriterLog.return_value 

        message = "This should not be logged"
        functionname = "decorated_function"
        
        with pytest.raises(LoggerException) as logException:
            # Initialize the logger with global logging disabled
            logger = Logger(
                writeLoggerStrategy=mock_write_strategy,
                includeloglevel = True,
                includefunctionname = False
            )

            Logger._thread_functionname[threading.get_ident()] = functionname        

            with patch("logger.src.loggerDecorator.gaurav_logger", lambda func: func) as gaurav_logger:
                @gaurav_logger
                def decorated_function():
                    # Attempt to log a message
                    Logger.log(message, LoglevelEnum.DEBUG)
                
                decorated_function()

                logger_json = {LogConstants.LOG_LEVEL: LoglevelEnum.DEBUG.value, LogConstants.LOG_MESSAGE: message, LogConstants.LOG_FUNCTION_NAME: functionname}
                
                mock_write_strategy.writelog.assert_called_once_with(logger_json)

    def teardown_method(self):
        Logger._instance = None
        Logger._thread_functionname = {}
        Logger._isfunctionlevel_enable = {}
        Logger._isgloballoggerenable = True
        Logger._Logger__loggerMessageDecorator = SimpleLogger()
        Logger._Logger__writeLoggerStrategy = None
        Logger._Logger__includefunctionname = True
        Logger._Logger__includeloglevel = True
        




        
        

        

        



    


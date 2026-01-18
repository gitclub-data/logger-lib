from unittest.mock import patch, Mock
from src.logger import Logger
from src.loggerDecorator import gaurav_logger


class TestLoggerDecoratorWhenGlobalLoggerEnable:

    def setup_method(self):
        with patch("src.writeLogMessage.FileWriterLog") as MockFileWriterLog:
            mock_writer_log = MockFileWriterLog.return_value         
        self.logger = Logger(mock_writer_log)

        self.mock_function = Mock()
        self.mock_function.return_value = 42
        self.mock_function.__name__ = "mock_function"

    def test_gaurav_decorator_returns_callable(self):
        func = gaurav_logger()
        assert callable(func)

    def test_gaurav_decorator_return_a_callable_which_returns_a_callable(self):
        func = gaurav_logger()
        inside_func = func(self.mock_function)
        assert callable(inside_func)

    def test_gaurav_decorator_return_a_callable_which_returns_a_callable_which_returns_wrapper_callable(self):
        func = gaurav_logger()
        wrapper_func = func(self.mock_function)
        wrapper_func()
        assert callable(self.mock_function)
    
    def test_is_logger_enable_is_true_when_provide_nothing_as_gaurav_decorator_args(self):
        func = gaurav_logger()
        wrapper_func = func(self.mock_function)
        wrapper_func()
        assert self.logger._isloggerenable

    def test_is_logger_enable_is_true_when_provide_true_as_gaurav_decorator_args(self):
        func = gaurav_logger(enable=True)
        wrapper_func = func(self.mock_function)
        wrapper_func()
        assert self.logger._isloggerenable

    def test_is_logger_enable_is_false_when_provide_false_as_gaurav_decorator_args(self):
        func = gaurav_logger(enable=False)
        wrapper_func = func(self.mock_function)
        wrapper_func()
        assert not self.logger._isloggerenable

    def tearDown(self):
        self.mock_function.reset_mock()
        Logger._setUpDefaultValues()
        del self.logger

        



from unittest.mock import patch, Mock
from logger.src.logger import Logger
from logger.src.loggerMessageDecorators import SimpleLogger
from logger.src.loggerDecorator import gaurav_logger

class TestLoggerDecoratorWhenGlobalLoggerEnable:

    def setup_method(self):
        with patch("logger.src.writeLogMessage.FileWriterLog") as MockFileWriterLog:
            mock_writer_log = MockFileWriterLog.return_value         
        self.logger = Logger(mock_writer_log)

        self.mock_function = Mock()
        self.mock_function.return_value = 42
        self.mock_function.__qualname__ = "file"
        self.mock_function.__name__ = "mock_function"
        Logger._isfunctionlevel_enable = {}

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
        function_uid = f"{self.mock_function.__module__}.{self.mock_function.__qualname__}"

        assert function_uid in Logger._isfunctionlevel_enable
        assert Logger._isfunctionlevel_enable[function_uid] == True

    def test_is_logger_enable_is_true_when_provide_true_as_gaurav_decorator_args(self):
        func = gaurav_logger(enable=True)
        wrapper_func = func(self.mock_function)
        wrapper_func()
        function_uid = f"{self.mock_function.__module__}.{self.mock_function.__qualname__}"

        assert function_uid in Logger._isfunctionlevel_enable
        assert Logger._isfunctionlevel_enable[function_uid] == True

    def test_is_logger_enable_is_false_when_provide_false_as_gaurav_decorator_args(self):
        func = gaurav_logger(enable=False)
        wrapper_func = func(self.mock_function)
        wrapper_func()
        function_uid = f"{self.mock_function.__module__}.{self.mock_function.__qualname__}"

        assert function_uid in Logger._isfunctionlevel_enable
        assert Logger._isfunctionlevel_enable[function_uid] == False
    
    def teardown_method(self):
        Logger._instance = None
        Logger._thread_functionname = {}
        Logger._isfunctionlevel_enable = {}
        Logger._isgloballoggerenable = True
        Logger._Logger__loggerMessageDecorator = SimpleLogger()
        Logger._Logger__writeLoggerStrategy = None
        Logger._Logger__includefunctionname = True
        Logger._Logger__includeloglevel = True

class TestLoggerDecoratorWhenGlobalLoggerDisable:
    def setup_method(self):
        with patch("logger.src.writeLogMessage.FileWriterLog") as MockFileWriterLog:
            mock_writer_log = MockFileWriterLog.return_value         
        self.logger = Logger(mock_writer_log, isgloballoggerenable=False)

        self.mock_function = Mock()
        self.mock_function.return_value = 42
        self.mock_function.__qualname__ = "file"
        self.mock_function.__name__ = "mock_function"
        Logger._isfunctionlevel_enable = {}

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
        function_uid = f"{self.mock_function.__module__}.{self.mock_function.__qualname__}"

        assert function_uid not in Logger._isfunctionlevel_enable

    def test_is_logger_enable_is_true_when_provide_true_as_gaurav_decorator_args(self):
        func = gaurav_logger(enable=True)
        wrapper_func = func(self.mock_function)
        wrapper_func()
        function_uid = f"{self.mock_function.__module__}.{self.mock_function.__qualname__}"

        assert function_uid not in Logger._isfunctionlevel_enable

    def teardown_method(self):
        Logger._instance = None
        Logger._thread_functionname = {}
        Logger._isfunctionlevel_enable = {}
        Logger._isgloballoggerenable = True
        Logger._Logger__loggerMessageDecorator = SimpleLogger()
        Logger._Logger__writeLoggerStrategy = None
        Logger._Logger__includefunctionname = True
        Logger._Logger__includeloglevel = True

        



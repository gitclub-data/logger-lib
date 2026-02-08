from logger.src.loggerMessageDecorators import LoggerMessageDecorator, SimpleLogger, LoggerWithTimeStamp, LoggerWithServiceName
from logger.src.logConstants import LogConstants

from unittest.mock import patch
from datetime import timezone, datetime

class TestLoggerMessageDecoratorForSimpleLogger:

    def setup_method(self):
        self.messagedecorator : LoggerMessageDecorator = SimpleLogger()

    def testgetLogreturnsajson(self):
        loggerjson = self.messagedecorator.getLog({LogConstants.LOG_MESSAGE : "hello"})
        assert isinstance(loggerjson,dict)

    def testandverifyitsjsonvalueforgetLog(self):
        loggerjson = self.messagedecorator.getLog({LogConstants.LOG_MESSAGE : "hello"})
        assert loggerjson == {LogConstants.LOG_MESSAGE : "hello"}

    def testifapplynextloggertolognextvaluework(self):
        with patch('logger.src.loggerMessageDecorators.LoggerWithTimeStamp') as LoggerWithTimeStamp:
            timestamploggerdecorator = LoggerWithTimeStamp()
            self.messagedecorator = SimpleLogger(timestamploggerdecorator)
            self.messagedecorator.getLog({LogConstants.LOG_MESSAGE : "hello"})
            assert timestamploggerdecorator.getLog.asset_called_once()


class TestLoggerMessageDecoratorForLoggerWithTimeStamp:

    def setup_method(self):
        self.localtimezone : timezone = timezone.utc
        self.messagedecorator : LoggerMessageDecorator = LoggerWithTimeStamp(self.localtimezone)

    def testgetLogreturnsajson(self):
        loggerjson = self.messagedecorator.getLog({LogConstants.LOG_MESSAGE : "hello"})
        assert isinstance(loggerjson,dict)

    def testandverifyitsjsonvalueforgetLog(self):
        fixed_dt = datetime(
            2026, 1, 29, 12, 2, 41, 641322, tzinfo=timezone.utc
        )
        with patch("logger.src.loggerMessageDecorators.datetime") as mock_datetime:
            mock_datetime.now.return_value = fixed_dt
            loggerjson = self.messagedecorator.getLog({LogConstants.LOG_MESSAGE : "hello"})

        assert loggerjson == {LogConstants.LOG_MESSAGE : "hello", LogConstants.LOG_TIMESTAMP: "2026-01-29 12:02:41.641322+00:00"}

    def testifapplynextloggertolognextvaluework(self):
        with patch('logger.src.loggerMessageDecorators.LoggerWithServiceName') as LoggerWithServiceName:
            servicenameloggerdecorator = LoggerWithServiceName()
            self.messagedecorator = SimpleLogger(servicenameloggerdecorator)
            self.messagedecorator.getLog({LogConstants.LOG_MESSAGE : "hello"})
            assert servicenameloggerdecorator.getLog.asset_called_once()

class TestLoggerMessageDecoratorForLoggerWithServiceName:

    def setup_method(self):
        self.servicename = "Service-1"
        self.messagedecorator : LoggerMessageDecorator = LoggerWithServiceName(self.servicename)

    def testgetLogreturnsajson(self):
        loggerjson = self.messagedecorator.getLog({LogConstants.LOG_MESSAGE : "hello"})
        assert isinstance(loggerjson,dict)

    def testandverifyitsjsonvalueforgetLog(self):
        loggerjson = self.messagedecorator.getLog({LogConstants.LOG_MESSAGE : "hello"})
        assert loggerjson == {LogConstants.LOG_MESSAGE : "hello", LogConstants.LOG_SERVICE_NAME: self.servicename}

    def testifapplynextloggertolognextvaluework(self):
        with patch('logger.src.loggerMessageDecorators.LoggerWithTimeStamp') as LoggerWithTimeStamp:
            timestamploggerdecorator = LoggerWithTimeStamp()
            self.messagedecorator = SimpleLogger(timestamploggerdecorator)
            self.messagedecorator.getLog({LogConstants.LOG_MESSAGE : "hello"})
            assert timestamploggerdecorator.getLog.asset_called_once()




    
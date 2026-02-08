# Simplest Hello World Examples for testing a logger 

# create a simple sync filewriter and injected into logger to tell where to write the logs
# and then use logger to do the logging process. and multiple data using decorators

from logger import Logger
from logger import *

logMessanger : WriteLogMessage = AsyncFileWriterLog("log.txt")
logdecorator : LoggerMessageDecorator = SimpleLogger(LoggerWithTimeStamp(additionallogger=LoggerWithServiceName(serviceName="Service1")))

# remove log level even though we have provided.. as a statement by default it will include it
# remove function name from the log by default it will include it
# enbale global logger (all logger will be enabled or disable if enable you can decide for individual)
logger = Logger(logMessanger, loggerDecorator=logdecorator, includeloglevel=False, includefunctionname=False, isgloballoggerenable=False)

@gaurav_logger()
def func1(msg: str):
    Logger.log("before writing message", LoglevelEnum.DEBUG)
    print(msg)
    Logger.log("after writing message", LoglevelEnum.DEBUG)

@gaurav_logger()
def func2(msg: str):
    Logger.log("before writing message", LoglevelEnum.DEBUG)
    print(msg)
    Logger.log("after writing message", LoglevelEnum.DEBUG)

func1("hello World")
func2("new world")

# Simplest Hello World Examples for testing a logger 

# create a simple sync filewriter and injected into logger to tell where to write the logs
# and then use logger to do the logging process. and multiple data using decorators

from logger import Logger
from logger import *

from zoneinfo import ZoneInfo
from collections import deque

logdeque = deque()

logMessanger : WriteLogMessage =  WriteLogsInQueue(logdeque)
logdecorator : LoggerMessageDecorator = SimpleLogger(LoggerWithTimeStamp(localtimezone=ZoneInfo("Asia/Kolkata") ,additionallogger=LoggerWithServiceName(serviceName="Service1")))
logger = Logger(logMessanger, loggerDecorator=logdecorator)

@gaurav_logger()
def func1(msg: str):
    Logger.log("before writing message", LoglevelEnum.DEBUG)
    print(msg)
    Logger.log("after writing message", LoglevelEnum.DEBUG)

func1("hello World")
print(logdeque)



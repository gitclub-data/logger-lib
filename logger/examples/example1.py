# Simplest Hello World Examples for testing a logger 

# create a simple sync filewriter and injected into logger to tell where to write the logs
# and then use logger to do the logging process.

from logger import Logger
from logger import *

logMessanger : WriteLogMessage = FileWriterLog("log.txt")
logger = Logger(logMessanger)

@gaurav_logger()
def func1(msg: str):
    Logger.log("before writing message", LoglevelEnum.DEBUG)
    print(msg)
    Logger.log("after writing message", LoglevelEnum.DEBUG)

func1("hello World")

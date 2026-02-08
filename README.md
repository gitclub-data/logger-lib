## Project Structure : 

```text
logger/
|   ├──__init__.py
│   └──src/
│       ├──__init__.py
│       ├──logConstants.py
│       ├──logger.py
│       ├──loggerDecorator.py
│       ├──loggerException.py
│       ├──loggerMessageDecorators.py
│       ├──logLevelEnum.py
│       ├──writeLogMessage.py
│   └──test/
│       ├──__init__.py
│       ├──test_logger.py
│       ├──test_loggerDecorator.py
│       ├──test_loggerMessageDecorators.py
│       ├──test_writeLogMessage.py
|   └──examples/
|       ├──example..py
```

## What is logger?
Logger is a lightweight, modular logging library that provides a clean and pluggable interface for seamless integration into any application.

It is designed for fast and reliable log processing, with a strongly modular architecture where each component is clearly segregated. This makes the library easy to extend, customize, and contribute to.

Logger can be easily integrated into existing applications and tailored to meet user-specific logging requirements.

> **Note:** `logger-lib` is not yet published on PyPI or any other package index. You can still install it locally by following the steps below.

## Installation
**Clone the repository** 
```bash
git clone https://github.com/gitclub-data/logger-lib.git
```

**Navigate to the project folder**
```bash
python setup.py sdist bdist_wheel
```

**Build the package**

This will create distribution files in the `dist/` folder.
```bash
pip install dist\logger_lib-0.1.0-py3-none-any.whl
```

**install the package**
```bash
pip install dist\logger_lib-0.1.0-py3-none-any.whl
```

## Usage Guide

The logger library is easy to use. You only need to import the required modules and provide configuration based on your needs.

### how to use?

You can import all classes and functions from the logger library using:

```python
from logger import *
```

However, the main class you need is Logger. Import it explicitly as shown below:

```python
from logger import Logger
```

**Initializing the Logger**

```python
logger = Logger(logMessanger)
```

**Required Arguments**

The Logger constructor requires the following argument:

```python
writeLoggerStrategy : WriteLogMessage = logMessanger,
```

* writeLoggerStrategy: Defines how and where log messages are written (for example, console, file, or any custom destination).

**Optional Configuration Arguments**

The Logger class provides several optional arguments with default values. You can override these based on your requirements:

```python
loggerDecorator: LoggerMessageDecorator = SimpleLogger(), 
includefunctionname : bool = True, 
includeloglevel : bool = True, 
isgloballoggerenable: bool = True)
```

***Description of Optional Arguments***

* loggerDecorator (LoggerMessageDecorator): Controls the formatting of log messages and determines which details are included.
 
* includefunctionname: Enables or disables the inclusion of the function name in log messages.

* includeloglevel: Enables or disables the inclusion of the log level (e.g., DEBUG, ERROR, WARNING) in log messages.

* isgloballoggerenable: Enables or disables logging globally for the entire application.


**Complete Logger Setup** 

To fully configure the logger, you must set both the writeLoggerStrategy and the LoggerMessageDecorator.

Let’s walk through how to configure these components.

***Setting Up writeLoggerStrategy***

The writeLoggerStrategy defines how and where log messages are written.

1. <u>***Synchronous File Writer***</u>

    ```python
    from logger import WriteLogMessage, FileWriterLog

    logMessanger : WriteLogMessage = FileWriterLog("filename.txt")
    ```

    * FileWriterLog : A synchronous file writer that writes log messages to a file one by one. 
        
        Since it operates synchronously, the application waits until the log is written before continuing.

2. <u>***Writing Logs to a Queue***</u>

    ```python
    from collections import deque
    from logger import WriteLogMessage, WriteLogsInQueue

    deque = deque([])
    logMessanger : WriteLogMessage = WriteLogsInQueue(deque)
    ```

    * WriteLogsInQueue: This strategy creates log entries (in JSON format) and stores them in the provided queue.

        You have full control over the deque, allowing you to:

        * Write logs to a file later

        * Send logs to Kafka or another messaging system

        * Process or filter logs asynchronously

        This approach is useful when you want custom log handling or deferred processing.

3. <u>***Asynchronous File Writer***</u>

    ```python
    from logger import WriteLogMessage, AsyncFileWriterLog

    logMessanger : WriteLogMessage = AsyncFileWriterLog("filename.txt")
    ```

    * AsyncFileWriterLog: Writes logs to a file asynchronously, ensuring that logging does not block the main application flow.

        This helps prevent performance issues or lag when large volumes of logs are generated.

***Setting Up loggerDecorator***

`LoggerMessageDecorator` defines which parameters are attached to each log entry.
Internally, it creates a `loggerjson` object and populates it with all the required log parameters.

Each Logger instance accepts an **additional loggerDecorator argument.** Using this decorator, you can attach extra parameters to the loggerjson in any order. The logger framework automatically handles ordering internally and ensures that log fields are written in a consistent sequence, especially when logs are written directly to a file.

***Available LoggerMessageDecorators***

1. <u>***SimpleLogger***</u>

    `SimpleLogger` is the most basic decorator. 

    * Accepts an optional additional logger decorator

    * Adds only the log message to the loggerjson

    * This decorator is useful when:

        * You do not want to include any extra metadata

        * You only need the log message in your logs

    Note: Even if you add other decorators, the log message will always be included automatically in the loggerjson.

    ```python
    from logger import LoggerMessageDecorator, SimpleLogger

    logdecorator : LoggerMessageDecorator = SimpleLogger()
    ```

2. <u>***LoggerWithTimeStamp***</u>

    Use LoggerWithTimeStamp when you want to attach a timestamp to each log entry.

    It accepts:

    * A timezone (`localtimezone`)

    * An optional additional logger decorator

    If no timezone is provided, the timestamp defaults to UTC.

    ```python
    from zoneinfo import ZoneInfo
    from logger import LoggerMessageDecorator, LoggerWithTimeStamp

    logdecorator : LoggerMessageDecorator = LoggerWithTimeStamp(localtimezone=ZoneInfo("Asia/Kolkata"))
    ```

    This decorator adds the current timestamp to the loggerjson at the time the log is created.

3. <u>***LoggerWithServiceName***</u>

    `LoggerWithServiceName` allows you to attach the name of the service or program that generated the log.

    It accepts:

    * `serviceName`: Name of the service or application

    * An optional additional logger decorator

    This is especially useful when:

    * Multiple services write logs to the same file

    * You want to filter or analyze logs by service name later

    ```python
    from logger import LoggerMessageDecorator, LoggerWithServiceName

    logdecorator : LoggerMessageDecorator = LoggerWithServiceName(serviceName="Service1")
    ```

## Using the Logger Decorator

After completing the logger setup, you can freely use `@gaurav_logger` as a decorator on any function.
This allows you to `enable` or `disable` logging at the `function level` as needed.

```python
@gaurav_logger(enable=True)
def func1(msg: str):
    Logger.log("before writing message", LoglevelEnum.DEBUG)
    print(msg)
    Logger.log("after writing message", LoglevelEnum.DEBUG)
```

In this example:

* Logging is explicitly enabled for func1

* Log messages are recorded before and after the function logic executes

Note: If you do not pass any arguments to `@gaurav_logger`, logging is enabled by default.

```python
@gaurav_logger()
def func2():
    Logger.log("logging is enabled by default", LoglevelEnum.INFO)
```

## Performance & Load Testing
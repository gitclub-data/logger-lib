from typing import Callable, Any
import inspect
import threading

# logger import
from .logger import Logger
from .loggerException import LoggerException, LoggerExceptionMessageConstant

def function_uid(func):
    func = inspect.unwrap(func)
    if hasattr(func, "__func__"):  # bound method
        func = func.__func__
    return f"{func.__module__}.{func.__qualname__}"

def gaurav_logger(enable: bool = True) -> Callable:  
    """
        Decorator to enable or disable logging for a specific function.

        Args:
            enable (bool, optional): Flag to enable or disable logging for the
                decorated function. Defaults to True.

        Returns:
            Callable: The decorator that applies logging behavior to the function.
    """ 
    def decorator(function: Callable[..., Any])-> Callable:
        """
            Inner decorator that wraps the target function.

            Args:
                function (Callable[..., Any]): The function to be decorated.

            Returns:
                Callable: The wrapped function with logging behavior.
        """
        def wrapper(*args, **kwargs) -> Any:
            """
                Wrapper function that executes the target function and controls logging.

                Before executing the function, it sets logger flags based on the
                decorator arguments and global logger settings.

                Args:
                    *args: Positional arguments for the target function.
                    **kwargs: Keyword arguments for the target function.

                Returns:
                    Any: The result of executing the target function.
            """

            # check logger is even initialized or not
            if Logger._instance==None:
                raise LoggerException(LoggerExceptionMessageConstant.LOGGER_INSTANTIATION_EXCEPTION)
            
            thread_id = threading.get_ident()
            functionid = function_uid(function)
            if Logger._isgloballoggerenable:
                # adding threadid and attaching this function
                Logger._thread_functionname[thread_id] = functionid

                # attaching if function level is enabled for logging or not
                if functionid not in Logger._isfunctionlevel_enable:
                    Logger._isfunctionlevel_enable[functionid] = enable
                                
            result = function(*args, **kwargs)
            
            # cleanup tasks
            if Logger._isgloballoggerenable:
                # removing threadid by which this function is attached
                Logger._thread_functionname.pop(thread_id)

            return result
        return wrapper            
    return decorator
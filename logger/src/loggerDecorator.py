from typing import Callable, Any

# logger import
from .logger import Logger

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
            if Logger._isgloballoggerenable:
                Logger._isloggerenable = enable
            Logger._funcname = function.__name__
            return function(*args, **kwargs)
        return wrapper            
    return decorator
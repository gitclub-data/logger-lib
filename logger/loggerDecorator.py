from typing import Callable, Any

# logger import
from .logger import Logger

def gaurav_logger(enable: bool = True):   
    def decorator(function: Callable[..., Any]):
        def wrapper(*args, **kwargs):
            if Logger._isgloballoggerenable:
                Logger._isloggerenable = enable
            Logger._funcname = function.__name__
            return function(*args, **kwargs)
        return wrapper            
    return decorator
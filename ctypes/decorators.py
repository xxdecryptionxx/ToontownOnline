# File: c (Python 2.4)

import sys
import ctypes
LOGGING = False

def stdcall(restype, dll, argtypes, logging = False):
    
    def decorate(func):
        if isinstance(dll, basestring):
            this_dll = ctypes.CDLL(dll)
        else:
            this_dll = dll
        api = ctypes.WINFUNCTYPE(restype, *argtypes)(func.func_name, this_dll)
        func._api_ = api
        if logging or LOGGING:
            
            def f(*args):
                result = func(*args)
                print >>sys.stderr, '# function call: %s%s -> %s' % (func.func_name, args, result)
                return result

            return f
        else:
            return func

    return decorate


def cdecl(restype, dll, argtypes, logging = False):
    
    def decorate(func):
        if isinstance(dll, basestring):
            this_dll = ctypes.CDLL(dll)
        else:
            this_dll = dll
        api = ctypes.CFUNCTYPE(restype, *argtypes)(func.func_name, this_dll)
        func._api_ = api
        if logging or LOGGING:
            
            def f(*args):
                result = func(*args)
                print >>sys.stderr, func.func_name, args, '->', result
                return result

            return f
        else:
            return func

    return decorate


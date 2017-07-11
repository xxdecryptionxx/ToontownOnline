# File: n (Python 2.4)

from types import ClassType as classobj
from types import FunctionType as function
from types import InstanceType as instance
from types import MethodType as instancemethod
from types import ModuleType as module

try:
    from types import CodeType as code
except ImportError:
    pass


# File: d (Python 2.4)

global _nextThreadId
__all__ = [
    'error',
    'LockType',
    'start_new_thread',
    'interrupt_main',
    'exit',
    'allocate_lock',
    'get_ident',
    'stack_size',
    'forceYield',
    'considerYield']
from pandac import PandaModules as pm
forceYield = pm.Thread.forceYield
considerYield = pm.Thread.considerYield

class error(StandardError):
    pass


class LockType:
    
    def __init__(self):
        self._LockType__lock = pm.Mutex('PythonLock')
        self._LockType__cvar = pm.ConditionVar(self._LockType__lock)
        self._LockType__locked = False

    
    def acquire(self, waitflag = 1):
        self._LockType__lock.acquire()
        
        try:
            if self._LockType__locked and not waitflag:
                return False
            
            while self._LockType__locked:
                self._LockType__cvar.wait()
            self._LockType__locked = True
            return True
        finally:
            self._LockType__lock.release()


    
    def release(self):
        self._LockType__lock.acquire()
        
        try:
            if not self._LockType__locked:
                raise error, 'Releasing unheld lock.'
            
            self._LockType__locked = False
            self._LockType__cvar.notify()
        finally:
            self._LockType__lock.release()


    
    def locked(self):
        return self._LockType__locked

    __enter__ = acquire
    
    def __exit__(self, t, v, tb):
        self.release()


_threads = { }
_nextThreadId = 0
_threadsLock = pm.Mutex('thread._threadsLock')

def start_new_thread(function, args, kwargs = { }, name = None):
    global _nextThreadId
    
    def threadFunc(threadId, function = function, args = args, kwargs = kwargs):
        
        try:
            function(*args, **args)
        except SystemExit:
            pass
        finally:
            _remove_thread_id(threadId)


    _threadsLock.acquire()
    
    try:
        threadId = _nextThreadId
        _nextThreadId += 1
        if name is None:
            name = 'PythonThread-%s' % threadId
        
        thread = pm.PythonThread(threadFunc, [
            threadId], name, name)
        thread.setPythonData(threadId)
        _threads[threadId] = (thread, { }, None)
        thread.start(pm.TPNormal, False)
        return threadId
    finally:
        _threadsLock.release()



def _add_thread(thread, wrapper):
    global _nextThreadId
    _threadsLock.acquire()
    
    try:
        threadId = _nextThreadId
        _nextThreadId += 1
        thread.setPythonData(threadId)
        _threads[threadId] = (thread, { }, wrapper)
        return threadId
    finally:
        _threadsLock.release()



def _get_thread_wrapper(thread, wrapperClass):
    global _nextThreadId
    threadId = thread.getPythonData()
    if threadId is None:
        _threadsLock.acquire()
        
        try:
            threadId = _nextThreadId
            _nextThreadId += 1
            thread.setPythonData(threadId)
            wrapper = wrapperClass(thread, threadId)
            _threads[threadId] = (thread, { }, wrapper)
            return wrapper
        finally:
            _threadsLock.release()

    else:
        _threadsLock.acquire()
        
        try:
            (t, locals, wrapper) = _threads[threadId]
            if wrapper is None:
                wrapper = wrapperClass(thread, threadId)
                _threads[threadId] = (thread, locals, wrapper)
            
            return wrapper
        finally:
            _threadsLock.release()



def _get_thread_locals(thread, i):
    global _nextThreadId
    threadId = thread.getPythonData()
    if threadId is None:
        _threadsLock.acquire()
        
        try:
            threadId = _nextThreadId
            _nextThreadId += 1
            thread.setPythonData(threadId)
            locals = { }
            _threads[threadId] = (thread, locals, None)
            return locals.setdefault(i, { })
        finally:
            _threadsLock.release()

    else:
        _threadsLock.acquire()
        
        try:
            (t, locals, wrapper) = _threads[threadId]
            return locals.setdefault(i, { })
        finally:
            _threadsLock.release()



def _remove_thread_id(threadId):
    _threadsLock.acquire()
    
    try:
        (thread, locals, wrapper) = _threads[threadId]
        del _threads[threadId]
        thread.setPythonData(None)
    finally:
        _threadsLock.release()



def interrupt_main():
    pass


def exit():
    raise SystemExit


def allocate_lock():
    return LockType()


def get_ident():
    return pm.Thread.getCurrentThread().this


def stack_size(size = 0):
    raise error


class _local(object):
    
    def __del__(self):
        i = id(self)
        _threadsLock.acquire()
        
        try:
            for (thread, locals, wrapper) in _threads.values():
                
                try:
                    del locals[i]
                continue
                except KeyError:
                    continue
                

        finally:
            _threadsLock.release()


    
    def __setattr__(self, key, value):
        d = _get_thread_locals(pm.Thread.getCurrentThread(), id(self))
        d[key] = value

    
    def __getattribute__(self, key):
        d = _get_thread_locals(pm.Thread.getCurrentThread(), id(self))
        if key == '__dict__':
            return d
        
        
        try:
            return d[key]
        except KeyError:
            return object.__getattribute__(self, key)




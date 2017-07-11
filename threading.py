# File: t (Python 2.4)

import sys as _sys

try:
    import thread
except ImportError:
    del _sys.modules[__name__]
    raise 

from time import time as _time, sleep as _sleep
from traceback import format_exc as _format_exc
from collections import deque
__all__ = [
    'activeCount',
    'Condition',
    'currentThread',
    'enumerate',
    'Event',
    'Lock',
    'RLock',
    'Semaphore',
    'BoundedSemaphore',
    'Thread',
    'Timer',
    'setprofile',
    'settrace',
    'local']
_start_new_thread = thread.start_new_thread
_allocate_lock = thread.allocate_lock
_get_ident = thread.get_ident
ThreadError = thread.error
del thread
_VERBOSE = False

class _Verbose(object):
    
    def __init__(self, verbose = None):
        pass

    
    def _note(self, *args):
        pass


_profile_hook = None
_trace_hook = None

def setprofile(func):
    global _profile_hook
    _profile_hook = func


def settrace(func):
    global _trace_hook
    _trace_hook = func

Lock = _allocate_lock

def RLock(*args, **kwargs):
    return _RLock(*args, **args)


class _RLock(_Verbose):
    
    def __init__(self, verbose = None):
        _Verbose.__init__(self, verbose)
        self._RLock__block = _allocate_lock()
        self._RLock__owner = None
        self._RLock__count = 0

    
    def __repr__(self):
        if self._RLock__owner:
            pass
        return '<%s(%s, %d)>' % (self.__class__.__name__, self._RLock__owner.getName(), self._RLock__count)

    
    def acquire(self, blocking = 1):
        me = currentThread()
        if self._RLock__owner is me:
            self._RLock__count = self._RLock__count + 1
            return 1
        
        rc = self._RLock__block.acquire(blocking)
        if rc:
            self._RLock__owner = me
            self._RLock__count = 1
        
        return rc

    
    def release(self):
        me = currentThread()
        self._RLock__count = self._RLock__count - 1
        count = self._RLock__count - 1
        if not count:
            self._RLock__owner = None
            self._RLock__block.release()
        

    
    def _acquire_restore(self, .2):
        (count, owner) = .2
        self._RLock__block.acquire()
        self._RLock__count = count
        self._RLock__owner = owner

    
    def _release_save(self):
        count = self._RLock__count
        self._RLock__count = 0
        owner = self._RLock__owner
        self._RLock__owner = None
        self._RLock__block.release()
        return (count, owner)

    
    def _is_owned(self):
        return self._RLock__owner is currentThread()



def Condition(*args, **kwargs):
    return _Condition(*args, **args)


class _Condition(_Verbose):
    
    def __init__(self, lock = None, verbose = None):
        _Verbose.__init__(self, verbose)
        if lock is None:
            lock = RLock()
        
        self._Condition__lock = lock
        self.acquire = lock.acquire
        self.release = lock.release
        
        try:
            self._release_save = lock._release_save
        except AttributeError:
            pass

        
        try:
            self._acquire_restore = lock._acquire_restore
        except AttributeError:
            pass

        
        try:
            self._is_owned = lock._is_owned
        except AttributeError:
            pass

        self._Condition__waiters = []

    
    def __repr__(self):
        return '<Condition(%s, %d)>' % (self._Condition__lock, len(self._Condition__waiters))

    
    def _release_save(self):
        self._Condition__lock.release()

    
    def _acquire_restore(self, x):
        self._Condition__lock.acquire()

    
    def _is_owned(self):
        if self._Condition__lock.acquire(0):
            self._Condition__lock.release()
            return False
        else:
            return True

    
    def wait(self, timeout = None):
        waiter = _allocate_lock()
        waiter.acquire()
        self._Condition__waiters.append(waiter)
        saved_state = self._release_save()
        
        try:
            if timeout is None:
                waiter.acquire()
            else:
                endtime = _time() + timeout
                delay = 0.00050000000000000001
                while True:
                    gotit = waiter.acquire(0)
                    if gotit:
                        break
                    
                    remaining = endtime - _time()
                    if remaining <= 0:
                        break
                    
                    delay = min(delay * 2, remaining, 0.050000000000000003)
                    _sleep(delay)
                if not gotit:
                    
                    try:
                        self._Condition__waiters.remove(waiter)
                    except ValueError:
                        pass
                    

        finally:
            self._acquire_restore(saved_state)


    
    def notify(self, n = 1):
        _Condition__waiters = self._Condition__waiters
        waiters = _Condition__waiters[:n]
        if not waiters:
            return None
        
        if not n != 1 or 's':
            pass
        self._note('%s.notify(): notifying %d waiter%s', self, n, '')
        for waiter in waiters:
            waiter.release()
            
            try:
                _Condition__waiters.remove(waiter)
            continue
            except ValueError:
                continue
            

        

    
    def notifyAll(self):
        self.notify(len(self._Condition__waiters))



def Semaphore(*args, **kwargs):
    return _Semaphore(*args, **args)


class _Semaphore(_Verbose):
    
    def __init__(self, value = 1, verbose = None):
        _Verbose.__init__(self, verbose)
        self._Semaphore__cond = Condition(Lock())
        self._Semaphore__value = value

    
    def acquire(self, blocking = 1):
        rc = False
        self._Semaphore__cond.acquire()
        while self._Semaphore__value == 0:
            if not blocking:
                break
            
            self._Semaphore__cond.wait()
        self._Semaphore__value = self._Semaphore__value - 1
        rc = True
        self._Semaphore__cond.release()
        return rc

    
    def release(self):
        self._Semaphore__cond.acquire()
        self._Semaphore__value = self._Semaphore__value + 1
        self._Semaphore__cond.notify()
        self._Semaphore__cond.release()



def BoundedSemaphore(*args, **kwargs):
    return _BoundedSemaphore(*args, **args)


class _BoundedSemaphore(_Semaphore):
    
    def __init__(self, value = 1, verbose = None):
        _Semaphore.__init__(self, value, verbose)
        self._initial_value = value

    
    def release(self):
        if self._Semaphore__value >= self._initial_value:
            raise ValueError, 'Semaphore released too many times'
        
        return _Semaphore.release(self)



def Event(*args, **kwargs):
    return _Event(*args, **args)


class _Event(_Verbose):
    
    def __init__(self, verbose = None):
        _Verbose.__init__(self, verbose)
        self._Event__cond = Condition(Lock())
        self._Event__flag = False

    
    def isSet(self):
        return self._Event__flag

    
    def set(self):
        self._Event__cond.acquire()
        
        try:
            self._Event__flag = True
            self._Event__cond.notifyAll()
        finally:
            self._Event__cond.release()


    
    def clear(self):
        self._Event__cond.acquire()
        
        try:
            self._Event__flag = False
        finally:
            self._Event__cond.release()


    
    def wait(self, timeout = None):
        self._Event__cond.acquire()
        
        try:
            if not self._Event__flag:
                self._Event__cond.wait(timeout)
        finally:
            self._Event__cond.release()



_counter = 0

def _newname(template = 'Thread-%d'):
    global _counter
    _counter = _counter + 1
    return template % _counter

_active_limbo_lock = _allocate_lock()
_active = { }
_limbo = { }

class Thread(_Verbose):
    _Thread__initialized = False
    _Thread__exc_info = _sys.exc_info
    
    def __init__(self, group = None, target = None, name = None, args = (), kwargs = { }, verbose = None):
        _Verbose.__init__(self, verbose)
        self._Thread__target = target
        if not name:
            pass
        self._Thread__name = str(_newname())
        self._Thread__args = args
        self._Thread__kwargs = kwargs
        self._Thread__daemonic = self._set_daemon()
        self._Thread__started = False
        self._Thread__stopped = False
        self._Thread__block = Condition(Lock())
        self._Thread__initialized = True
        self._Thread__stderr = _sys.stderr

    
    def _set_daemon(self):
        return currentThread().isDaemon()

    
    def __repr__(self):
        status = 'initial'
        if self._Thread__started:
            status = 'started'
        
        if self._Thread__stopped:
            status = 'stopped'
        
        if self._Thread__daemonic:
            status = status + ' daemon'
        
        return '<%s(%s, %s)>' % (self.__class__.__name__, self._Thread__name, status)

    
    def start(self):
        _active_limbo_lock.acquire()
        _limbo[self] = self
        _active_limbo_lock.release()
        _start_new_thread(self._Thread__bootstrap, ())
        self._Thread__started = True
        _sleep(9.9999999999999995e-007)

    
    def run(self):
        if self._Thread__target:
            self._Thread__target(*self._Thread__args, **self._Thread__args)
        

    
    def _Thread__bootstrap(self):
        
        try:
            self._Thread__started = True
            _active_limbo_lock.acquire()
            _active[_get_ident()] = self
            del _limbo[self]
            _active_limbo_lock.release()
            if _trace_hook:
                self._note('%s.__bootstrap(): registering trace hook', self)
                _sys.settrace(_trace_hook)
            
            if _profile_hook:
                self._note('%s.__bootstrap(): registering profile hook', self)
                _sys.setprofile(_profile_hook)
            
            
            try:
                self.run()
            except SystemExit:
                pass
            except:
                if _sys:
                    _sys.stderr.write('Exception in thread %s:\n%s\n' % (self.getName(), _format_exc()))
                else:
                    (exc_type, exc_value, exc_tb) = self._Thread__exc_info()
                    
                    try:
                        print >>self._Thread__stderr, 'Exception in thread ' + self.getName() + ' (most likely raised during interpreter shutdown):'
                        print >>self._Thread__stderr, 'Traceback (most recent call last):'
                        while exc_tb:
                            print >>self._Thread__stderr, '  File "%s", line %s, in %s' % (exc_tb.tb_frame.f_code.co_filename, exc_tb.tb_lineno, exc_tb.tb_frame.f_code.co_name)
                            exc_tb = exc_tb.tb_next
                        print >>self._Thread__stderr, '%s: %s' % (exc_type, exc_value)
                    finally:
                        del exc_type
                        del exc_value
                        del exc_tb


        finally:
            self._Thread__stop()
            
            try:
                self._Thread__delete()
            except:
                pass



    
    def _Thread__stop(self):
        self._Thread__block.acquire()
        self._Thread__stopped = True
        self._Thread__block.notifyAll()
        self._Thread__block.release()

    
    def _Thread__delete(self):
        _active_limbo_lock.acquire()
        
        try:
            del _active[_get_ident()]
        except KeyError:
            if 'dummy_threading' not in _sys.modules:
                raise 
            
        except:
            'dummy_threading' not in _sys.modules
        finally:
            _active_limbo_lock.release()


    
    def join(self, timeout = None):
        self._Thread__block.acquire()
        if timeout is None:
            while not self._Thread__stopped:
                self._Thread__block.wait()
        else:
            deadline = _time() + timeout
            while not self._Thread__stopped:
                delay = deadline - _time()
                if delay <= 0:
                    break
                
                self._Thread__block.wait(delay)
        self._Thread__block.release()

    
    def getName(self):
        return self._Thread__name

    
    def setName(self, name):
        self._Thread__name = str(name)

    
    def isAlive(self):
        if self._Thread__started:
            pass
        return not (self._Thread__stopped)

    
    def isDaemon(self):
        return self._Thread__daemonic

    
    def setDaemon(self, daemonic):
        self._Thread__daemonic = daemonic



def Timer(*args, **kwargs):
    return _Timer(*args, **args)


class _Timer(Thread):
    
    def __init__(self, interval, function, args = [], kwargs = { }):
        Thread.__init__(self)
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.finished = Event()

    
    def cancel(self):
        self.finished.set()

    
    def run(self):
        self.finished.wait(self.interval)
        if not self.finished.isSet():
            self.function(*self.args, **self.args)
        
        self.finished.set()



class _MainThread(Thread):
    
    def __init__(self):
        Thread.__init__(self, name = 'MainThread')
        self._Thread__started = True
        _active_limbo_lock.acquire()
        _active[_get_ident()] = self
        _active_limbo_lock.release()
        import atexit as atexit
        atexit.register(self._MainThread__exitfunc)

    
    def _set_daemon(self):
        return False

    
    def _MainThread__exitfunc(self):
        self._Thread__stop()
        t = _pickSomeNonDaemonThread()
        if t:
            pass
        1
        while t:
            t.join()
            t = _pickSomeNonDaemonThread()
        self._Thread__delete()



def _pickSomeNonDaemonThread():
    for t in enumerate():
        if not t.isDaemon() and t.isAlive():
            return t
            continue
    


class _DummyThread(Thread):
    
    def __init__(self):
        Thread.__init__(self, name = _newname('Dummy-%d'))
        self._Thread__started = True
        _active_limbo_lock.acquire()
        _active[_get_ident()] = self
        _active_limbo_lock.release()

    
    def _set_daemon(self):
        return True

    
    def join(self, timeout = None):
        pass



def currentThread():
    
    try:
        return _active[_get_ident()]
    except KeyError:
        return _DummyThread()



def activeCount():
    _active_limbo_lock.acquire()
    count = len(_active) + len(_limbo)
    _active_limbo_lock.release()
    return count


def enumerate():
    _active_limbo_lock.acquire()
    active = _active.values() + _limbo.values()
    _active_limbo_lock.release()
    return active

_MainThread()

try:
    from thread import _local as local
except ImportError:
    from _threading_local import local


def _test():
    
    class BoundedQueue(_Verbose):
        
        def __init__(self, limit):
            _Verbose.__init__(self)
            self.mon = RLock()
            self.rc = Condition(self.mon)
            self.wc = Condition(self.mon)
            self.limit = limit
            self.queue = deque()

        
        def put(self, item):
            self.mon.acquire()
            while len(self.queue) >= self.limit:
                self._note('put(%s): queue full', item)
                self.wc.wait()
            self.queue.append(item)
            self._note('put(%s): appended, length now %d', item, len(self.queue))
            self.rc.notify()
            self.mon.release()

        
        def get(self):
            self.mon.acquire()
            while not self.queue:
                self._note('get(): queue empty')
                self.rc.wait()
            item = self.queue.popleft()
            self._note('get(): got %s, %d left', item, len(self.queue))
            self.wc.notify()
            self.mon.release()
            return item


    
    class ProducerThread(Thread):
        
        def __init__(self, queue, quota):
            Thread.__init__(self, name = 'Producer')
            self.queue = queue
            self.quota = quota

        
        def run(self):
            random = random
            import random
            counter = 0
            while counter < self.quota:
                counter = counter + 1
                self.queue.put('%s.%d' % (self.getName(), counter))
                _sleep(random() * 1.0000000000000001e-005)


    
    class ConsumerThread(Thread):
        
        def __init__(self, queue, count):
            Thread.__init__(self, name = 'Consumer')
            self.queue = queue
            self.count = count

        
        def run(self):
            while self.count > 0:
                item = self.queue.get()
                print item
                self.count = self.count - 1


    NP = 3
    QL = 4
    NI = 5
    Q = BoundedQueue(QL)
    P = []
    for i in range(NP):
        t = ProducerThread(Q, NI)
        t.setName('Producer-%d' % (i + 1))
        P.append(t)
    
    C = ConsumerThread(Q, NI * NP)
    for t in P:
        t.start()
        _sleep(9.9999999999999995e-007)
    
    C.start()
    for t in P:
        t.join()
    
    C.join()

if __name__ == '__main__':
    _test()


# File: d (Python 2.4)

__all__ = [
    'TaskThreaded',
    'TaskThread']
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.task import Task

class TaskThreaded:
    notify = directNotify.newCategory('TaskThreaded')
    _Serial = SerialNumGen()
    
    def __init__(self, name, threaded = True, timeslice = None, callback = None):
        self._TaskThreaded__name = name
        self._TaskThreaded__threaded = threaded
        if timeslice is None:
            timeslice = 0.01
        
        self._TaskThreaded__timeslice = timeslice
        self._TaskThreaded__taskNames = set()
        self._taskStartTime = None
        self._TaskThreaded__threads = set()
        self._callback = callback

    
    def finished(self):
        if self._callback:
            self._callback()
        

    
    def destroy(self):
        for taskName in self._TaskThreaded__taskNames:
            taskMgr.remove(taskName)
        
        del self._TaskThreaded__taskNames
        for thread in self._TaskThreaded__threads:
            thread.tearDown()
            thread._destroy()
        
        del self._TaskThreaded__threads
        del self._callback
        self.ignoreAll()

    
    def getTimeslice(self):
        return self._TaskThreaded___timeslice

    
    def setTimeslice(self, timeslice):
        self._TaskThreaded__timeslice = timeslice

    
    def scheduleCallback(self, callback):
        if not self._TaskThreaded__threaded:
            callback()
        else:
            taskName = '%s-ThreadedTask-%s' % (self._TaskThreaded__name, TaskThreaded._Serial.next())
            self._TaskThreaded__taskNames.add(taskName)
            taskMgr.add(Functor(self._TaskThreaded__doCallback, callback, taskName), taskName)

    
    def scheduleThread(self, thread):
        thread._init(self)
        thread.setUp()
        if thread.isFinished():
            thread._destroy()
        elif not self._TaskThreaded__threaded:
            while not thread.isFinished():
                thread.run()
            thread._destroy()
        else:
            self._TaskThreaded__threads.add(thread)
            taskName = '%s-ThreadedTask-%s-%s' % (self._TaskThreaded__name, thread.__class__.__name__, TaskThreaded._Serial.next())
            self._TaskThreaded__taskNames.add(taskName)
            self._TaskThreaded__threads.add(thread)
            taskMgr.add(Functor(self._doThreadCallback, thread, taskName), taskName)

    
    def _doCallback(self, callback, taskName, task):
        self._TaskThreaded__taskNames.remove(taskName)
        self._taskStartTime = globalClock.getRealTime()
        callback()
        self._taskStartTime = None
        return Task.done

    
    def _doThreadCallback(self, thread, taskName, task):
        self._taskStartTime = globalClock.getRealTime()
        thread.run()
        self._taskStartTime = None
        if thread.isFinished():
            thread._destroy()
            self._TaskThreaded__taskNames.remove(taskName)
            self._TaskThreaded__threads.remove(thread)
            return Task.done
        else:
            return Task.cont

    
    def taskTimeLeft(self):
        if self._taskStartTime is None:
            return True
        
        return globalClock.getRealTime() - self._taskStartTime < self._TaskThreaded__timeslice



class TaskThread:
    
    def setUp(self):
        pass

    
    def run(self):
        pass

    
    def tearDown(self):
        pass

    
    def done(self):
        pass

    
    def finished(self):
        self.tearDown()
        self._finished = True
        self.done()

    
    def isFinished(self):
        return self._finished

    
    def timeLeft(self):
        return self.parent.taskTimeLeft()

    
    def _init(self, parent):
        self.parent = parent
        self._finished = False

    
    def _destroy(self):
        del self.parent
        del self._finished



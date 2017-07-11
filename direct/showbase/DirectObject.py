# File: d (Python 2.4)

__all__ = [
    'DirectObject']
from direct.directnotify.DirectNotifyGlobal import directNotify
from MessengerGlobal import messenger
from direct.showbase.PythonUtil import ClassTree

class DirectObject:
    
    def __init__(self):
        pass

    
    def accept(self, event, method, extraArgs = []):
        return messenger.accept(event, self, method, extraArgs, 1)

    
    def acceptOnce(self, event, method, extraArgs = []):
        return messenger.accept(event, self, method, extraArgs, 0)

    
    def ignore(self, event):
        return messenger.ignore(event, self)

    
    def ignoreAll(self):
        return messenger.ignoreAll(self)

    
    def isAccepting(self, event):
        return messenger.isAccepting(event, self)

    
    def getAllAccepting(self):
        return messenger.getAllAccepting(self)

    
    def isIgnoring(self, event):
        return messenger.isIgnoring(event, self)

    
    def classTree(self):
        return ClassTree(self)

    
    def addTask(self, *args, **kwargs):
        if not hasattr(self, '_taskList'):
            self._taskList = { }
        
        kwargs['owner'] = self
        task = taskMgr.add(*args, **args)
        return task

    
    def doMethodLater(self, *args, **kwargs):
        if not hasattr(self, '_taskList'):
            self._taskList = { }
        
        kwargs['owner'] = self
        task = taskMgr.doMethodLater(*args, **args)
        return task

    
    def removeTask(self, taskOrName):
        if type(taskOrName) == type(''):
            if hasattr(self, '_taskList'):
                taskListValues = self._taskList.values()
                for task in taskListValues:
                    if task.name == taskOrName:
                        task.remove()
                        continue
                
            
        else:
            taskOrName.remove()

    
    def removeAllTasks(self):
        if hasattr(self, '_taskList'):
            for task in self._taskList.values():
                task.remove()
            
        

    
    def _addTask(self, task):
        self._taskList[task.id] = task

    
    def _clearTask(self, task):
        del self._taskList[task.id]

    
    def detectLeaks(self):
        if not __dev__:
            return None
        
        events = messenger.getAllAccepting(self)
        tasks = []
        if hasattr(self, '_taskList'):
            continue
            tasks = [ task.name for task in self._taskList.values() ]
        
        if len(events) or len(tasks):
            estr = choice(len(events), 'listening to events: %s' % events, '')
            if len(events):
                pass
            andStr = choice(len(tasks), ' and ', '')
            tstr = choice(len(tasks), '%srunning tasks: %s' % (andStr, tasks), '')
            notify = directNotify.newCategory('LeakDetect')
            func = choice(getRepository()._crashOnProactiveLeakDetect, self.notify.error, self.notify.warning)
            func('destroyed %s instance is still %s%s' % (self.__class__.__name__, estr, tstr))
        



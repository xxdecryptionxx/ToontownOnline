# File: d (Python 2.4)

__all__ = [
    'EventManager']
from MessengerGlobal import *
from direct.directnotify.DirectNotifyGlobal import *

class EventManager:
    notify = None
    PStatCollector = None
    EventStorePandaNode = None
    EventQueue = None
    EventHandler = None
    
    def __init__(self, eventQueue = None):
        if EventManager.notify == None:
            EventManager.notify = directNotify.newCategory('EventManager')
        
        self.eventQueue = eventQueue
        self.eventHandler = None
        self._wantPstats = None

    
    def doEvents(self):
        if self._wantPstats is None:
            self._wantPstats = config.GetBool('pstats-eventmanager', 0)
            PStatCollector = PStatCollector
            import pandac.PandaModules
            EventManager.PStatCollector = PStatCollector
        
        if self._wantPstats:
            processFunc = self.processEventPstats
        else:
            processFunc = self.processEvent
        while not self.eventQueue.isQueueEmpty():
            processFunc(self.eventQueue.dequeueEvent())

    
    def eventLoopTask(self, task):
        self.doEvents()
        messenger.send('event-loop-done')
        return task.cont

    
    def parseEventParameter(self, eventParameter):
        if eventParameter.isInt():
            return eventParameter.getIntValue()
        elif eventParameter.isDouble():
            return eventParameter.getDoubleValue()
        elif eventParameter.isString():
            return eventParameter.getStringValue()
        elif eventParameter.isWstring():
            return eventParameter.getWstringValue()
        elif eventParameter.isTypedRefCount():
            return eventParameter.getTypedRefCountValue()
        elif eventParameter.isEmpty():
            return None
        else:
            ptr = eventParameter.getPtr()
            if EventManager.EventStorePandaNode is None:
                EventStorePandaNode = EventStorePandaNode
                import pandac.PandaModules
                EventManager.EventStorePandaNode = EventStorePandaNode
            
            if isinstance(ptr, EventManager.EventStorePandaNode):
                ptr = ptr.getValue()
            
            return ptr

    
    def processEvent(self, event):
        eventName = event.getName()
        if eventName:
            paramList = []
            for i in range(event.getNumParameters()):
                eventParameter = event.getParameter(i)
                eventParameterData = self.parseEventParameter(eventParameter)
                paramList.append(eventParameterData)
            
            if EventManager.notify.getDebug() and eventName != 'NewFrame':
                EventManager.notify.debug('received C++ event named: ' + eventName + ' parameters: ' + repr(paramList))
            
            if paramList:
                messenger.send(eventName, paramList)
            else:
                messenger.send(eventName)
            if self.eventHandler:
                self.eventHandler.dispatchEvent(event)
            
        else:
            EventManager.notify.warning('unnamed event in processEvent')

    
    def processEventPstats(self, event):
        eventName = event.getName()
        if eventName:
            paramList = []
            for i in range(event.getNumParameters()):
                eventParameter = event.getParameter(i)
                eventParameterData = self.parseEventParameter(eventParameter)
                paramList.append(eventParameterData)
            
            if EventManager.notify.getDebug() and eventName != 'NewFrame':
                EventManager.notify.debug('received C++ event named: ' + eventName + ' parameters: ' + repr(paramList))
            
            if self._wantPstats:
                name = eventName
                hyphen = name.find('-')
                if hyphen >= 0:
                    name = name[0:hyphen]
                
                pstatCollector = EventManager.PStatCollector('App:Show code:eventManager:' + name)
                pstatCollector.start()
                if self.eventHandler:
                    cppPstatCollector = EventManager.PStatCollector('App:Show code:eventManager:' + name + ':C++')
                
            
            if paramList:
                messenger.send(eventName, paramList)
            else:
                messenger.send(eventName)
            if self.eventHandler:
                if self._wantPstats:
                    cppPstatCollector.start()
                
                self.eventHandler.dispatchEvent(event)
            
            if self._wantPstats:
                if self.eventHandler:
                    cppPstatCollector.stop()
                
                pstatCollector.stop()
            
        else:
            EventManager.notify.warning('unnamed event in processEvent')

    
    def restart(self):
        if None in (EventManager.EventQueue, EventManager.EventHandler):
            EventQueue = EventQueue
            EventHandler = EventHandler
            import pandac.PandaModules
            EventManager.EventQueue = EventQueue
            EventManager.EventHandler = EventHandler
        
        if self.eventQueue == None:
            self.eventQueue = EventManager.EventQueue.getGlobalEventQueue()
        
        if self.eventHandler == None:
            if self.eventQueue == EventManager.EventQueue.getGlobalEventQueue():
                self.eventHandler = EventManager.EventHandler.getGlobalEventHandler()
            else:
                self.eventHandler = EventManager.EventHandler(self.eventQueue)
        
        taskMgr = taskMgr
        import direct.task.TaskManagerGlobal
        taskMgr.add(self.eventLoopTask, 'eventManager')

    
    def shutdown(self):
        taskMgr = taskMgr
        import direct.task.TaskManagerGlobal
        taskMgr.remove('eventManager')



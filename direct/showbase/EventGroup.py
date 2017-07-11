# File: d (Python 2.4)

__all__ = [
    'EventGroup']
from direct.showbase import DirectObject
from direct.showbase.PythonUtil import SerialNumGen, Functor

class EventGroup(DirectObject.DirectObject):
    _SerialNumGen = SerialNumGen()
    
    def __init__(self, name, subEvents = None, doneEvent = None):
        self._name = name
        self._subEvents = set()
        self._completedEvents = set()
        if doneEvent is None:
            doneEvent = 'EventGroup-%s-%s-Done' % (EventGroup._SerialNumGen.next(), self._name)
        
        self._doneEvent = doneEvent
        self._completed = False
        if subEvents is not None:
            for event in subEvents:
                self.addEvent(event)
            
        

    
    def destroy(self):
        if hasattr(self, '_name'):
            del self._name
            del self._subEvents
            del self._completedEvents
            self.ignoreAll()
        

    
    def getName(self):
        return self._name

    
    def getDoneEvent(self):
        return self._doneEvent

    
    def isCompleted(self):
        return self._completed

    
    def addEvent(self, eventName):
        if self._completed:
            self.notify.error("addEvent('%s') called on completed EventGroup '%s'" % (eventName, self.getName()))
        
        if eventName in self._subEvents:
            self.notify.error("addEvent('%s'): event already in EventGroup '%s'" % (eventName, self.getName()))
        
        self._subEvents.add(eventName)
        self.acceptOnce(eventName, Functor(self._subEventComplete, eventName))
        return eventName

    
    def newEvent(self, name):
        return self.addEvent('%s-SubEvent-%s-%s' % (self._name, EventGroup._SerialNumGen.next(), name))

    
    def _subEventComplete(self, subEventName, *args, **kwArgs):
        if subEventName in self._completedEvents:
            self.notify.warning("_subEventComplete: '%s' already received" % subEventName)
        else:
            self._completedEvents.add(subEventName)
            if self._completedEvents == self._subEvents:
                self._signalComplete()
            

    
    def _signalComplete(self):
        self._completed = True
        messenger.send(self._doneEvent)
        self.destroy()

    
    def __repr__(self):
        return "%s('%s', %s, doneEvent='%s') # completed=%s" % (self.__class__.__name__, self._name, tuple(self._subEvents), self._doneEvent, tuple(self._completedEvents))



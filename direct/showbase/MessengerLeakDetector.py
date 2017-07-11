# File: d (Python 2.4)

from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.showbase.DirectObject import DirectObject
from direct.showbase.Job import Job
import gc
import __builtin__

class MessengerLeakObject(DirectObject):
    
    def __init__(self):
        self.accept('leakEvent', self._handleEvent)

    
    def _handleEvent(self):
        pass



def _leakMessengerObject():
    leakObject = MessengerLeakObject()


class MessengerLeakDetector(Job):
    notify = directNotify.newCategory('MessengerLeakDetector')
    
    def __init__(self, name):
        Job.__init__(self, name)
        self.setPriority(Job.Priorities.Normal * 2)
        jobMgr.add(self)

    
    def run(self):
        builtinIds = set()
        builtinIds.add(id(__builtin__.__dict__))
        
        try:
            builtinIds.add(id(base))
            builtinIds.add(id(base.cr))
            builtinIds.add(id(base.cr.doId2do))
        except:
            pass

        
        try:
            builtinIds.add(id(simbase))
            builtinIds.add(id(simbase.air))
            builtinIds.add(id(simbase.air.doId2do))
        except:
            pass

        
        try:
            builtinIds.add(id(uber))
            builtinIds.add(id(uber.air))
            builtinIds.add(id(uber.air.doId2do))
        except:
            pass

        while True:
            yield None
            objects = messenger._Messenger__objectEvents.keys()
            for object in objects:
                yield None
                objList1 = []
                objList2 = []
                curObjList = objList1
                nextObjList = objList2
                visitedObjIds = set()
                visitedObjIds.add(id(object))
                visitedObjIds.add(id(messenger._Messenger__objectEvents))
                visitedObjIds.add(id(messenger._Messenger__callbacks))
                nextObjList.append(object)
                foundBuiltin = False
                while len(nextObjList):
                    if foundBuiltin:
                        break
                    
                    curObjList = nextObjList
                    nextObjList = []
                    for curObj in curObjList:
                        if foundBuiltin:
                            break
                        
                        yield None
                        referrers = gc.get_referrers(curObj)
                        for referrer in referrers:
                            yield None
                            refId = id(referrer)
                            if refId in visitedObjIds:
                                continue
                            
                            if referrer is curObjList or referrer is nextObjList:
                                continue
                            
                            if refId in builtinIds:
                                foundBuiltin = True
                                break
                                continue
                            visitedObjIds.add(refId)
                            nextObjList.append(referrer)
                        
                    
                if not foundBuiltin:
                    self.notify.warning('%s is referenced only by the messenger' % itype(object))
                    continue
            



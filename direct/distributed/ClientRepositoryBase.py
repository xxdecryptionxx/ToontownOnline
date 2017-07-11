# File: d (Python 2.4)

from pandac.PandaModules import *
from MsgTypes import *
from direct.task import Task
from direct.directnotify import DirectNotifyGlobal
import CRCache
from direct.distributed.CRDataCache import CRDataCache
from direct.distributed.ConnectionRepository import ConnectionRepository
from direct.showbase import PythonUtil
import ParentMgr
import RelatedObjectMgr
import time
from ClockDelta import *
from PyDatagram import PyDatagram
from PyDatagramIterator import PyDatagramIterator
import types

class ClientRepositoryBase(ConnectionRepository):
    notify = DirectNotifyGlobal.directNotify.newCategory('ClientRepositoryBase')
    
    def __init__(self, dcFileNames = None, dcSuffix = '', connectMethod = None, threadedNet = None):
        if connectMethod is None:
            connectMethod = self.CM_HTTP
        
        ConnectionRepository.__init__(self, connectMethod, base.config, hasOwnerView = True, threadedNet = threadedNet)
        self.dcSuffix = dcSuffix
        if hasattr(self, 'setVerbose'):
            if self.config.GetBool('verbose-clientrepository'):
                self.setVerbose(1)
            
        
        self.context = 100000
        self.setClientDatagram(1)
        self.deferredGenerates = []
        self.deferredDoIds = { }
        self.lastGenerate = 0
        self.setDeferInterval(base.config.GetDouble('deferred-generate-interval', 0.20000000000000001))
        self.noDefer = False
        self.recorder = base.recorder
        self.readDCFile(dcFileNames)
        self.cache = CRCache.CRCache()
        self.doDataCache = CRDataCache()
        self.cacheOwner = CRCache.CRCache()
        self.serverDelta = 0
        self.bootedIndex = None
        self.bootedText = None
        self.parentMgr = ParentMgr.ParentMgr()
        self.relatedObjectMgr = RelatedObjectMgr.RelatedObjectMgr(self)
        self.timeManager = None
        self.heartbeatInterval = base.config.GetDouble('heartbeat-interval', 10)
        self.heartbeatStarted = 0
        self.lastHeartbeat = 0
        self._delayDeletedDOs = { }
        self.specialNameNumber = 0
        self.wantUpdateCalls = False

    
    def setDeferInterval(self, deferInterval):
        self.deferInterval = deferInterval
        self.setHandleCUpdates(self.deferInterval == 0)
        if self.deferredGenerates:
            taskMgr.remove('deferredGenerate')
            taskMgr.doMethodLater(self.deferInterval, self.doDeferredGenerate, 'deferredGenerate')
        

    
    def specialName(self, label):
        name = 'SpecialName %s %s' % (self.specialNameNumber, label)
        self.specialNameNumber += 1
        return name

    
    def getTables(self, ownerView):
        if ownerView:
            return (self.doId2ownerView, self.cacheOwner)
        else:
            return (self.doId2do, self.cache)

    
    def _getMsgName(self, msgId):
        return makeList(MsgId2Names.get(msgId, 'UNKNOWN MESSAGE: %s' % msgId))[0]

    
    def allocateContext(self):
        self.context += 1
        return self.context

    
    def setServerDelta(self, delta):
        self.serverDelta = delta

    
    def getServerDelta(self):
        return self.serverDelta

    
    def getServerTimeOfDay(self):
        return time.time() + self.serverDelta

    
    def doGenerate(self, parentId, zoneId, classId, doId, di):
        dclass = self.dclassesByNumber[classId]
        dclass.startGenerate()
        distObj = self.generateWithRequiredOtherFields(dclass, doId, di, parentId, zoneId)
        dclass.stopGenerate()

    
    def flushGenerates(self):
        while self.deferredGenerates:
            (msgType, extra) = self.deferredGenerates[0]
            del self.deferredGenerates[0]
            self.replayDeferredGenerate(msgType, extra)
        taskMgr.remove('deferredGenerate')

    
    def replayDeferredGenerate(self, msgType, extra):
        if msgType == CLIENT_CREATE_OBJECT_REQUIRED_OTHER:
            doId = extra
            if doId in self.deferredDoIds:
                (args, deferrable, dg, updates) = self.deferredDoIds[doId]
                del self.deferredDoIds[doId]
                self.doGenerate(*args)
                if deferrable:
                    self.lastGenerate = globalClock.getFrameTime()
                
                for (dg, di) in updates:
                    if type(di) is types.TupleType:
                        msgType = dg
                        (dg, di) = di
                        self.replayDeferredGenerate(msgType, (dg, di))
                        continue
                    self._ClientRepositoryBase__doUpdate(doId, di, True)
                
            
        else:
            self.notify.warning('Ignoring deferred message %s' % msgType)

    
    def doDeferredGenerate(self, task):
        now = globalClock.getFrameTime()
        while self.deferredGenerates:
            if now - self.lastGenerate < self.deferInterval:
                return Task.again
            
            (msgType, extra) = self.deferredGenerates[0]
            del self.deferredGenerates[0]
            self.replayDeferredGenerate(msgType, extra)
        return Task.done

    
    def generateWithRequiredFields(self, dclass, doId, di, parentId, zoneId):
        if self.doId2do.has_key(doId):
            distObj = self.doId2do[doId]
            distObj.generate()
            distObj.setLocation(parentId, zoneId)
            distObj.updateRequiredFields(dclass, di)
        elif self.cache.contains(doId):
            distObj = self.cache.retrieve(doId)
            self.doId2do[doId] = distObj
            distObj.generate()
            distObj.parentId = None
            distObj.zoneId = None
            distObj.setLocation(parentId, zoneId)
            distObj.updateRequiredFields(dclass, di)
        else:
            classDef = dclass.getClassDef()
            if classDef == None:
                self.notify.error('Could not create an undefined %s object.' % dclass.getName())
            
            distObj = classDef(self)
            distObj.dclass = dclass
            distObj.doId = doId
            self.doId2do[doId] = distObj
            distObj.generateInit()
            distObj._retrieveCachedData()
            distObj.generate()
            distObj.setLocation(parentId, zoneId)
            distObj.updateRequiredFields(dclass, di)
            print 'New DO:%s, dclass:%s' % (doId, dclass.getName())
        return distObj

    
    def generateWithRequiredOtherFields(self, dclass, doId, di, parentId = None, zoneId = None):
        if self.doId2do.has_key(doId):
            distObj = self.doId2do[doId]
            distObj.generate()
            distObj.setLocation(parentId, zoneId)
            distObj.updateRequiredOtherFields(dclass, di)
        elif self.cache.contains(doId):
            distObj = self.cache.retrieve(doId)
            self.doId2do[doId] = distObj
            distObj.generate()
            distObj.parentId = None
            distObj.zoneId = None
            distObj.setLocation(parentId, zoneId)
            distObj.updateRequiredOtherFields(dclass, di)
        else:
            classDef = dclass.getClassDef()
            if classDef == None:
                self.notify.error('Could not create an undefined %s object.' % dclass.getName())
            
            distObj = classDef(self)
            distObj.dclass = dclass
            distObj.doId = doId
            self.doId2do[doId] = distObj
            distObj.generateInit()
            distObj._retrieveCachedData()
            distObj.generate()
            distObj.setLocation(parentId, zoneId)
            distObj.updateRequiredOtherFields(dclass, di)
        return distObj

    
    def generateWithRequiredOtherFieldsOwner(self, dclass, doId, di):
        if self.doId2ownerView.has_key(doId):
            self.notify.error('duplicate owner generate for %s (%s)' % (doId, dclass.getName()))
            distObj = self.doId2ownerView[doId]
            distObj.generate()
            distObj.updateRequiredOtherFields(dclass, di)
        elif self.cacheOwner.contains(doId):
            distObj = self.cacheOwner.retrieve(doId)
            self.doId2ownerView[doId] = distObj
            distObj.generate()
            distObj.updateRequiredOtherFields(dclass, di)
        else:
            classDef = dclass.getOwnerClassDef()
            if classDef == None:
                self.notify.error('Could not create an undefined %s object. Have you created an owner view?' % dclass.getName())
            
            distObj = classDef(self)
            distObj.dclass = dclass
            distObj.doId = doId
            self.doId2ownerView[doId] = distObj
            distObj.generateInit()
            distObj.generate()
            distObj.updateRequiredOtherFields(dclass, di)
        return distObj

    
    def disableDoId(self, doId, ownerView = False):
        (table, cache) = self.getTables(ownerView)
        if table.has_key(doId):
            distObj = table[doId]
            del table[doId]
            cached = False
            if distObj.getCacheable() and distObj.getDelayDeleteCount() <= 0:
                cached = cache.cache(distObj)
            
            if not cached:
                distObj.deleteOrDelay()
                if distObj.getDelayDeleteCount() <= 0:
                    distObj.detectLeaks()
                
            
        elif self.deferredDoIds.has_key(doId):
            del self.deferredDoIds[doId]
            i = self.deferredGenerates.index((CLIENT_CREATE_OBJECT_REQUIRED_OTHER, doId))
            del self.deferredGenerates[i]
            if len(self.deferredGenerates) == 0:
                taskMgr.remove('deferredGenerate')
            
        else:
            self._logFailedDisable(doId, ownerView)

    
    def _logFailedDisable(self, doId, ownerView):
        self.notify.warning('Disable failed. DistObj ' + str(doId) + ' is not in dictionary, ownerView=%s' % ownerView)

    
    def handleDelete(self, di):
        pass

    
    def handleUpdateField(self, di):
        doId = di.getUint32()
        ovUpdated = self._ClientRepositoryBase__doUpdateOwner(doId, di)
        if doId in self.deferredDoIds:
            (args, deferrable, dg0, updates) = self.deferredDoIds[doId]
            dg = Datagram(di.getDatagram())
            di = DatagramIterator(dg, di.getCurrentIndex())
            updates.append((dg, di))
        else:
            self._ClientRepositoryBase__doUpdate(doId, di, ovUpdated)

    
    def _ClientRepositoryBase__doUpdate(self, doId, di, ovUpdated):
        do = self.doId2do.get(doId)
        if do is not None:
            do.dclass.receiveUpdate(do, di)
        elif not ovUpdated:
            
            try:
                handle = self.identifyAvatar(doId)
                if handle:
                    dclass = self.dclassesByName[handle.dclassName]
                    dclass.receiveUpdate(handle, di)
                else:
                    self.notify.warning('Asked to update non-existent DistObj ' + str(doId))
            self.notify.warning('Asked to update non-existent DistObj ' + str(doId) + 'and failed to find it')

        

    
    def _ClientRepositoryBase__doUpdateOwner(self, doId, di):
        ovObj = self.doId2ownerView.get(doId)
        if ovObj:
            odg = Datagram(di.getDatagram())
            odi = DatagramIterator(odg, di.getCurrentIndex())
            ovObj.dclass.receiveUpdate(ovObj, odi)
            return True
        
        return False

    
    def handleGoGetLost(self, di):
        if di.getRemainingSize() > 0:
            self.bootedIndex = di.getUint16()
            self.bootedText = di.getString()
            self.notify.warning('Server is booting us out (%d): %s' % (self.bootedIndex, self.bootedText))
        else:
            self.bootedIndex = None
            self.bootedText = None
            self.notify.warning('Server is booting us out with no explanation.')
        self.stopReaderPollTask()
        self.lostConnection()

    
    def handleServerHeartbeat(self, di):
        if base.config.GetBool('server-heartbeat-info', 1):
            self.notify.info('Server heartbeat.')
        

    
    def handleSystemMessage(self, di):
        message = di.getString()
        self.notify.info('Message from server: %s' % message)
        return message

    
    def handleSystemMessageAknowledge(self, di):
        message = di.getString()
        self.notify.info('Message with aknowledge from server: %s' % message)
        messenger.send('system message aknowledge', [
            message])
        return message

    
    def getObjectsOfClass(self, objClass):
        doDict = { }
        for (doId, do) in self.doId2do.items():
            if isinstance(do, objClass):
                doDict[doId] = do
                continue
        
        return doDict

    
    def getObjectsOfExactClass(self, objClass):
        doDict = { }
        for (doId, do) in self.doId2do.items():
            if do.__class__ == objClass:
                doDict[doId] = do
                continue
        
        return doDict

    
    def considerHeartbeat(self):
        if not self.heartbeatStarted:
            self.notify.debug('Heartbeats not started; not sending.')
            return None
        
        elapsed = globalClock.getRealTime() - self.lastHeartbeat
        if elapsed < 0 or elapsed > self.heartbeatInterval:
            self.notify.info('Sending heartbeat mid-frame.')
            self.startHeartbeat()
        

    
    def stopHeartbeat(self):
        taskMgr.remove('heartBeat')
        self.heartbeatStarted = 0

    
    def startHeartbeat(self):
        self.stopHeartbeat()
        self.heartbeatStarted = 1
        self.sendHeartbeat()
        self.waitForNextHeartBeat()

    
    def sendHeartbeatTask(self, task):
        self.sendHeartbeat()
        return Task.again

    
    def waitForNextHeartBeat(self):
        taskMgr.doMethodLater(self.heartbeatInterval, self.sendHeartbeatTask, 'heartBeat', taskChain = 'net')

    
    def replaceMethod(self, oldMethod, newFunction):
        return 0

    
    def getWorld(self, doId):
        obj = self.doId2do[doId]
        worldNP = obj.getParent()
        while None:
            nextNP = worldNP.getParent()
            if nextNP == render:
                break
                continue
            if worldNP.isEmpty():
                return None
                continue
        return worldNP

    
    def isLive(self):
        if base.config.GetBool('force-live', 0):
            return True
        
        if not __dev__:
            pass
        return not launcher.isTestServer()

    
    def isLocalId(self, id):
        return 0

    
    def _addDelayDeletedDO(self, do):
        key = id(do)
        self._delayDeletedDOs[key] = do

    
    def _removeDelayDeletedDO(self, do):
        key = id(do)
        del self._delayDeletedDOs[key]

    
    def printDelayDeletes(self):
        print 'DelayDeletes:'
        print '============='
        for obj in self._delayDeletedDOs.itervalues():
            print '%s\t%s (%s)\tdelayDeletes=%s' % (obj.doId, safeRepr(obj), itype(obj), obj.getDelayDeleteNames())
        



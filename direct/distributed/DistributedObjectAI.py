# File: d (Python 2.4)

from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed.DistributedObjectBase import DistributedObjectBase
from direct.showbase import PythonUtil
from pandac.PandaModules import *

class DistributedObjectAI(DistributedObjectBase):
    notify = directNotify.newCategory('DistributedObjectAI')
    QuietZone = 1
    
    def __init__(self, air):
        
        try:
            pass
        except:
            self.DistributedObjectAI_initialized = 1
            DistributedObjectBase.__init__(self, air)
            self.accountName = ''
            self.air = air
            className = self.__class__.__name__
            self.dclass = self.air.dclassesByName[className]
            self._DistributedObjectAI__preallocDoId = 0
            self.lastNonQuietZone = None
            self._DOAI_requestedDelete = False
            self._DistributedObjectAI__nextBarrierContext = 0
            self._DistributedObjectAI__barriers = { }
            self._DistributedObjectAI__generated = False
            self._DistributedObjectAI__generates = 0
            self._zoneData = None


    
    def getDeleteEvent(self):
        if hasattr(self, 'doId'):
            return 'distObjDelete-%s' % self.doId
        

    
    def sendDeleteEvent(self):
        delEvent = self.getDeleteEvent()
        if delEvent:
            messenger.send(delEvent)
        

    
    def getCacheable(self):
        return False

    
    def deleteOrDelay(self):
        self.delete()

    
    def getDelayDeleteCount(self):
        return 0

    
    def delete(self):
        self._DistributedObjectAI__generates -= 1
        if self._DistributedObjectAI__generates < 0:
            self.notify.debug('DistributedObjectAI: delete() called more times than generate()')
        
        if self._DistributedObjectAI__generates == 0:
            if self.air is not None:
                if not self._DOAI_requestedDelete:
                    pass
                1
                self._DOAI_requestedDelete = False
                self.releaseZoneData()
                for barrier in self._DistributedObjectAI__barriers.values():
                    barrier.cleanup()
                
                self._DistributedObjectAI__barriers = { }
                self.air.stopTrackRequestDeletedDO(self)
                if not hasattr(self, 'doNotDeallocateChannel'):
                    if self.air and not hasattr(self.air, 'doNotDeallocateChannel'):
                        if self.air.minChannel <= self.doId:
                            pass
                        self.doId <= self.air.maxChannel
                        if 1:
                            self.air.deallocateChannel(self.doId)
                        
                    
                
                self.air = None
                self.parentId = None
                self.zoneId = None
                self._DistributedObjectAI__generated = False
            
        

    
    def isDeleted(self):
        return self.air == None

    
    def isGenerated(self):
        return self._DistributedObjectAI__generated

    
    def getDoId(self):
        return self.doId

    
    def preAllocateDoId(self):
        self.doId = self.air.allocateChannel()
        self._DistributedObjectAI__preallocDoId = 1

    
    def announceGenerate(self):
        pass

    
    def addInterest(self, zoneId, note = '', event = None):
        self.air.addInterest(self.doId, zoneId, note, event)

    
    def b_setLocation(self, parentId, zoneId):
        self.d_setLocation(parentId, zoneId)
        self.setLocation(parentId, zoneId)

    
    def d_setLocation(self, parentId, zoneId):
        self.air.sendSetLocation(self, parentId, zoneId)

    
    def setLocation(self, parentId, zoneId):
        if self.parentId == parentId and self.zoneId == zoneId:
            return None
        
        oldParentId = self.parentId
        oldZoneId = self.zoneId
        self.air.storeObjectLocation(self, parentId, zoneId)
        if oldParentId != parentId or oldZoneId != zoneId:
            self.releaseZoneData()
            messenger.send(self.getZoneChangeEvent(), [
                zoneId,
                oldZoneId])
            if zoneId != DistributedObjectAI.QuietZone:
                lastLogicalZone = oldZoneId
                if oldZoneId == DistributedObjectAI.QuietZone:
                    lastLogicalZone = self.lastNonQuietZone
                
                self.handleLogicalZoneChange(zoneId, lastLogicalZone)
                self.lastNonQuietZone = zoneId
            
        

    
    def getLocation(self):
        
        try:
            if self.parentId <= 0 and self.zoneId <= 0:
                return None
            
            if self.parentId == 0xFFFFFFFFL and self.zoneId == 0xFFFFFFFFL:
                return None
            
            return (self.parentId, self.zoneId)
        except AttributeError:
            return None


    
    def postGenerateMessage(self):
        self._DistributedObjectAI__generated = True
        messenger.send(self.uniqueName('generate'), [
            self])

    
    def updateRequiredFields(self, dclass, di):
        dclass.receiveUpdateBroadcastRequired(self, di)
        self.announceGenerate()
        self.postGenerateMessage()

    
    def updateAllRequiredFields(self, dclass, di):
        dclass.receiveUpdateAllRequired(self, di)
        self.announceGenerate()
        self.postGenerateMessage()

    
    def updateRequiredOtherFields(self, dclass, di):
        dclass.receiveUpdateBroadcastRequired(self, di)
        self.announceGenerate()
        self.postGenerateMessage()
        dclass.receiveUpdateOther(self, di)

    
    def updateAllRequiredOtherFields(self, dclass, di):
        dclass.receiveUpdateAllRequired(self, di)
        self.announceGenerate()
        self.postGenerateMessage()
        dclass.receiveUpdateOther(self, di)

    
    def sendSetZone(self, zoneId):
        self.air.sendSetZone(self, zoneId)

    
    def startMessageBundle(self, name):
        self.air.startMessageBundle(name)

    
    def sendMessageBundle(self):
        self.air.sendMessageBundle(self.doId)

    
    def getZoneChangeEvent(self):
        return DistributedObjectAI.staticGetZoneChangeEvent(self.doId)

    
    def getLogicalZoneChangeEvent(self):
        return DistributedObjectAI.staticGetLogicalZoneChangeEvent(self.doId)

    
    def staticGetZoneChangeEvent(doId):
        return 'DOChangeZone-%s' % doId

    staticGetZoneChangeEvent = staticmethod(staticGetZoneChangeEvent)
    
    def staticGetLogicalZoneChangeEvent(doId):
        return 'DOLogicalChangeZone-%s' % doId

    staticGetLogicalZoneChangeEvent = staticmethod(staticGetLogicalZoneChangeEvent)
    
    def handleLogicalZoneChange(self, newZoneId, oldZoneId):
        messenger.send(self.getLogicalZoneChangeEvent(), [
            newZoneId,
            oldZoneId])

    
    def getZoneData(self):
        if self._zoneData is None:
            AIZoneData = AIZoneData
            import otp.ai.AIZoneData
            self._zoneData = AIZoneData(self.air, self.parentId, self.zoneId)
        
        return self._zoneData

    
    def releaseZoneData(self):
        if self._zoneData is not None:
            self._zoneData.destroy()
            self._zoneData = None
        

    
    def getRender(self):
        return self.getZoneData().getRender()

    
    def getNonCollidableParent(self):
        return self.getZoneData().getNonCollidableParent()

    
    def getParentMgr(self):
        return self.getZoneData().getParentMgr()

    
    def getCollTrav(self, *args, **kArgs):
        return self.getZoneData().getCollTrav(*args, **args)

    
    def sendUpdate(self, fieldName, args = []):
        if self.air:
            self.air.sendUpdate(self, fieldName, args)
        

    
    def GetPuppetConnectionChannel(self, doId):
        return doId + (0x1L << 32)

    
    def GetAccountConnectionChannel(self, doId):
        return doId + (0x3L << 32)

    
    def GetAccountIDFromChannelCode(self, channel):
        return channel >> 32

    
    def GetAvatarIDFromChannelCode(self, channel):
        return channel & 0xFFFFFFFFL

    
    def sendUpdateToAvatarId(self, avId, fieldName, args):
        channelId = self.GetPuppetConnectionChannel(avId)
        self.sendUpdateToChannel(channelId, fieldName, args)

    
    def sendUpdateToAccountId(self, accountId, fieldName, args):
        channelId = self.GetAccountConnectionChannel(accountId)
        self.sendUpdateToChannel(channelId, fieldName, args)

    
    def sendUpdateToChannel(self, channelId, fieldName, args):
        if self.air:
            self.air.sendUpdateToChannel(self, channelId, fieldName, args)
        

    
    def generateWithRequired(self, zoneId, optionalFields = []):
        if self._DistributedObjectAI__preallocDoId:
            self._DistributedObjectAI__preallocDoId = 0
            return self.generateWithRequiredAndId(self.doId, zoneId, optionalFields)
        
        parentId = self.air.districtId
        self.air.generateWithRequired(self, parentId, zoneId, optionalFields)
        self.generate()
        self.announceGenerate()
        self.postGenerateMessage()

    
    def generateWithRequiredAndId(self, doId, parentId, zoneId, optionalFields = []):
        if self._DistributedObjectAI__preallocDoId:
            self._DistributedObjectAI__preallocDoId = 0
        
        self.air.generateWithRequiredAndId(self, doId, parentId, zoneId, optionalFields)
        self.generate()
        self.announceGenerate()
        self.postGenerateMessage()

    
    def generateOtpObject(self, parentId, zoneId, optionalFields = [], doId = None):
        if self._DistributedObjectAI__preallocDoId:
            doId = self.doId
            self._DistributedObjectAI__preallocDoId = 0
        
        if doId is None:
            self.doId = self.air.allocateChannel()
        else:
            self.doId = doId
        self.air.addDOToTables(self, location = (parentId, zoneId))
        self.sendGenerateWithRequired(self.air, parentId, zoneId, optionalFields)
        self.generate()
        self.announceGenerate()
        self.postGenerateMessage()

    
    def generate(self):
        self._DistributedObjectAI__generates += 1

    
    def generateInit(self, repository = None):
        pass

    
    def generateTargetChannel(self, repository):
        if hasattr(self, 'dbObject'):
            return self.doId
        
        return repository.serverId

    
    def sendGenerateWithRequired(self, repository, parentId, zoneId, optionalFields = []):
        dg = self.dclass.aiFormatGenerate(self, self.doId, parentId, zoneId, self.generateTargetChannel(repository), repository.ourChannel, optionalFields)
        repository.send(dg)

    
    def initFromServerResponse(self, valDict):
        dclass = self.dclass
        for (key, value) in valDict.items():
            dclass.directUpdate(self, key, value)
        

    
    def requestDelete(self):
        if not self.air:
            doId = 'none'
            if hasattr(self, 'doId'):
                doId = self.doId
            
            self.notify.warning('Tried to delete a %s (doId %s) that is already deleted' % (self.__class__, doId))
            return None
        
        self.air.requestDelete(self)
        self.air.startTrackRequestDeletedDO(self)
        self._DOAI_requestedDelete = True

    
    def taskName(self, taskString):
        return '%s-%s' % (taskString, self.doId)

    
    def uniqueName(self, idString):
        return '%s-%s' % (idString, self.doId)

    
    def logSuspicious(self, avId, msg):
        self.air.writeServerEvent('suspicious', avId, msg)
        self.notify.warning('suspicious: avId: %s -- %s' % (avId, msg))

    
    def validate(self, avId, bool, msg):
        if not bool:
            self.air.writeServerEvent('suspicious', avId, msg)
            self.notify.warning('validate error: avId: %s -- %s' % (avId, msg))
        
        return bool

    
    def beginBarrier(self, name, avIds, timeout, callback):
        Barrier = Barrier
        import otp.ai
        context = self._DistributedObjectAI__nextBarrierContext
        self._DistributedObjectAI__nextBarrierContext = self._DistributedObjectAI__nextBarrierContext + 1 & 65535
        if avIds:
            barrier = Barrier.Barrier(name, self.uniqueName(name), avIds, timeout, doneFunc = PythonUtil.Functor(self._DistributedObjectAI__barrierCallback, context, callback))
            self._DistributedObjectAI__barriers[context] = barrier
            self.sendUpdate('setBarrierData', [
                self.getBarrierData()])
        else:
            callback(avIds)
        return context

    
    def getBarrierData(self):
        data = []
        for (context, barrier) in self._DistributedObjectAI__barriers.items():
            avatars = barrier.pendingAvatars
            if avatars:
                data.append((context, barrier.name, avatars))
                continue
        
        return data

    
    def ignoreBarrier(self, context):
        barrier = self._DistributedObjectAI__barriers.get(context)
        if barrier:
            barrier.cleanup()
            del self._DistributedObjectAI__barriers[context]
        

    
    def setBarrierReady(self, context):
        avId = self.air.getAvatarIdFromSender()
        barrier = self._DistributedObjectAI__barriers.get(context)
        if barrier == None:
            return None
        
        barrier.clear(avId)

    
    def _DistributedObjectAI__barrierCallback(self, context, callback, avIds):
        barrier = self._DistributedObjectAI__barriers.get(context)
        if barrier:
            barrier.cleanup()
            del self._DistributedObjectAI__barriers[context]
            callback(avIds)
        else:
            self.notify.warning('Unexpected completion from barrier %s' % context)

    
    def isGridParent(self):
        return 0

    
    def execCommand(self, string, mwMgrId, avId, zoneId):
        pass

    
    def _retrieveCachedData(self):
        pass



# File: d (Python 2.4)

from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed.DistributedObjectBase import DistributedObjectBase
from direct.showbase import PythonUtil
from pandac.PandaModules import *

class DistributedObjectUD(DistributedObjectBase):
    notify = directNotify.newCategory('DistributedObjectUD')
    QuietZone = 1
    
    def __init__(self, air):
        
        try:
            pass
        except:
            self.DistributedObjectUD_initialized = 1
            DistributedObjectBase.__init__(self, air)
            self.accountName = ''
            self.air = air
            className = self.__class__.__name__
            self.dclass = self.air.dclassesByName[className]
            self._DistributedObjectUD__preallocDoId = 0
            self.lastNonQuietZone = None
            self._DOUD_requestedDelete = False
            self._DistributedObjectUD__nextBarrierContext = 0
            self._DistributedObjectUD__barriers = { }
            self._DistributedObjectUD__generated = False
            self._DistributedObjectUD__generates = 0


    
    def getDeleteEvent(self):
        if hasattr(self, 'doId'):
            return 'distObjDelete-%s' % self.doId
        

    
    def sendDeleteEvent(self):
        delEvent = self.getDeleteEvent()
        if delEvent:
            messenger.send(delEvent)
        

    
    def delete(self):
        self._DistributedObjectUD__generates -= 1
        if self._DistributedObjectUD__generates < 0:
            self.notify.debug('DistributedObjectUD: delete() called more times than generate()')
        
        if self._DistributedObjectUD__generates == 0:
            if self.air is not None:
                if not self._DOUD_requestedDelete:
                    pass
                1
                self._DOUD_requestedDelete = False
                for barrier in self._DistributedObjectUD__barriers.values():
                    barrier.cleanup()
                
                self._DistributedObjectUD__barriers = { }
                self.parentId = None
                self.zoneId = None
                self._DistributedObjectUD__generated = False
            
        

    
    def isDeleted(self):
        return self.air == None

    
    def isGenerated(self):
        return self._DistributedObjectUD__generated

    
    def getDoId(self):
        return self.doId

    
    def preAllocateDoId(self):
        self.doId = self.air.allocateChannel()
        self._DistributedObjectUD__preallocDoId = 1

    
    def announceGenerate(self):
        self._DistributedObjectUD__generated = True

    
    def postGenerateMessage(self):
        messenger.send(self.uniqueName('generate'), [
            self])

    
    def addInterest(self, zoneId, note = '', event = None):
        self.air.addInterest(self.getDoId(), zoneId, note, event)

    
    def b_setLocation(self, parentId, zoneId):
        self.d_setLocation(parentId, zoneId)
        self.setLocation(parentId, zoneId)

    
    def d_setLocation(self, parentId, zoneId):
        self.air.sendSetLocation(self, parentId, zoneId)

    
    def setLocation(self, parentId, zoneId):
        self.air.storeObjectLocation(self, parentId, zoneId)

    
    def getLocation(self):
        
        try:
            if self.parentId <= 0 and self.zoneId <= 0:
                return None
            
            if self.parentId == 0xFFFFFFFFL and self.zoneId == 0xFFFFFFFFL:
                return None
            
            return (self.parentId, self.zoneId)
        except AttributeError:
            return None


    
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

    
    def getZoneChangeEvent(self):
        return 'DOChangeZone-%s' % self.doId

    
    def getLogicalZoneChangeEvent(self):
        return 'DOLogicalChangeZone-%s' % self.doId

    
    def handleLogicalZoneChange(self, newZoneId, oldZoneId):
        messenger.send(self.getLogicalZoneChangeEvent(), [
            newZoneId,
            oldZoneId])

    
    def getRender(self):
        return self.air.getRender(self.zoneId)

    
    def getNonCollidableParent(self):
        return self.air.getNonCollidableParent(self.zoneId)

    
    def getParentMgr(self):
        return self.air.getParentMgr(self.zoneId)

    
    def getCollTrav(self, *args, **kArgs):
        return self.air.getCollTrav(self.zoneId, *args, **args)

    
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
        if self._DistributedObjectUD__preallocDoId:
            self._DistributedObjectUD__preallocDoId = 0
            return self.generateWithRequiredAndId(self.doId, zoneId, optionalFields)
        
        parentId = self.air.districtId
        self.parentId = parentId
        self.zoneId = zoneId
        self.air.generateWithRequired(self, parentId, zoneId, optionalFields)
        self.generate()

    
    def generateWithRequiredAndId(self, doId, parentId, zoneId, optionalFields = []):
        if self._DistributedObjectUD__preallocDoId:
            self._DistributedObjectUD__preallocDoId = 0
        
        self.air.generateWithRequiredAndId(self, doId, parentId, zoneId, optionalFields)
        self.generate()
        self.announceGenerate()
        self.postGenerateMessage()

    
    def generateOtpObject(self, parentId, zoneId, optionalFields = [], doId = None):
        if self._DistributedObjectUD__preallocDoId:
            doId = self._DistributedObjectUD__preallocDoId
            self._DistributedObjectUD__preallocDoId = 0
        
        if doId is None:
            self.doId = self.air.allocateChannel()
        else:
            self.doId = doId
        self.air.addDOToTables(self, location = (parentId, zoneId))
        self.sendGenerateWithRequired(self.air, parentId, zoneId, optionalFields)
        self.generate()

    
    def generate(self):
        self._DistributedObjectUD__generates += 1
        self.air.storeObjectLocation(self, self.parentId, self.zoneId)

    
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
        self._DOUD_requestedDelete = True

    
    def taskName(self, taskString):
        return '%s-%s' % (taskString, self.doId)

    
    def uniqueName(self, idString):
        return '%s-%s' % (idString, self.doId)

    
    def validate(self, avId, bool, msg):
        if not bool:
            self.air.writeServerEvent('suspicious', avId, msg)
            self.notify.warning('validate error: avId: %s -- %s' % (avId, msg))
        
        return bool

    
    def beginBarrier(self, name, avIds, timeout, callback):
        Barrier = Barrier
        import otp.ai
        context = self._DistributedObjectUD__nextBarrierContext
        self._DistributedObjectUD__nextBarrierContext = self._DistributedObjectUD__nextBarrierContext + 1 & 65535
        if avIds:
            barrier = Barrier.Barrier(name, self.uniqueName(name), avIds, timeout, doneFunc = PythonUtil.Functor(self._DistributedObjectUD__barrierCallback, context, callback))
            self._DistributedObjectUD__barriers[context] = barrier
            self.sendUpdate('setBarrierData', [
                self._DistributedObjectUD__getBarrierData()])
        else:
            callback(avIds)
        return context

    
    def _DistributedObjectUD__getBarrierData(self):
        data = []
        for (context, barrier) in self._DistributedObjectUD__barriers.items():
            toons = barrier.pendingToons
            if toons:
                data.append((context, barrier.name, toons))
                continue
        
        return data

    
    def ignoreBarrier(self, context):
        barrier = self._DistributedObjectUD__barriers.get(context)
        if barrier:
            barrier.cleanup()
            del self._DistributedObjectUD__barriers[context]
        

    
    def setBarrierReady(self, context):
        avId = self.air.getAvatarIdFromSender()
        barrier = self._DistributedObjectUD__barriers.get(context)
        if barrier == None:
            return None
        
        barrier.clear(avId)

    
    def _DistributedObjectUD__barrierCallback(self, context, callback, avIds):
        barrier = self._DistributedObjectUD__barriers.get(context)
        if barrier:
            barrier.cleanup()
            del self._DistributedObjectUD__barriers[context]
            callback(avIds)
        else:
            self.notify.warning('Unexpected completion from barrier %s' % context)

    
    def isGridParent(self):
        return 0

    
    def execCommand(self, string, mwMgrId, avId, zoneId):
        pass



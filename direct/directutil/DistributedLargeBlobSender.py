# File: d (Python 2.4)

from direct.distributed import DistributedObject
from direct.directnotify import DirectNotifyGlobal
import LargeBlobSenderConsts

class DistributedLargeBlobSender(DistributedObject.DistributedObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedLargeBlobSender')
    
    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)

    
    def generate(self):
        DistributedLargeBlobSender.notify.debug('generate')
        DistributedObject.DistributedObject.generate(self)
        self.complete = 0
        self.doneEvent = None

    
    def setMode(self, mode):
        self.mode = mode
        self.useDisk = mode & LargeBlobSenderConsts.USE_DISK

    
    def setTargetAvId(self, avId):
        self.targetAvId = avId

    
    def announceGenerate(self):
        DistributedLargeBlobSender.notify.debug('announceGenerate')
        DistributedObject.DistributedObject.announceGenerate(self)
        if self.targetAvId != base.localAvatar.doId:
            return None
        
        if not self.useDisk:
            self.blob = ''
        

    
    def setChunk(self, chunk):
        DistributedLargeBlobSender.notify.debug('setChunk')
        if len(chunk) > 0:
            self.blob += chunk
        else:
            self.privOnBlobComplete()

    
    def setFilename(self, filename):
        DistributedLargeBlobSender.notify.debug('setFilename: %s' % filename)
        import os as os
        origDir = os.getcwd()
        bPath = LargeBlobSenderConsts.getLargeBlobPath()
        
        try:
            os.chdir(bPath)
        except OSError:
            DistributedLargeBlobSender.notify.error('could not access %s' % bPath)

        f = file(filename, 'rb')
        self.blob = f.read()
        f.close()
        os.unlink(filename)
        os.chdir(origDir)
        self.privOnBlobComplete()

    
    def isComplete(self):
        return self.complete

    
    def setDoneEvent(self, event):
        self.doneEvent = event

    
    def privOnBlobComplete(self):
        self.complete = 1
        if self.doneEvent is not None:
            messenger.send(self.doneEvent, [
                self.blob])
        

    
    def getBlob(self):
        return self.blob

    
    def sendAck(self):
        self.sendUpdate('setAck', [])



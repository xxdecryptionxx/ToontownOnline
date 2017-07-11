# File: d (Python 2.4)

from DistributedObjectUD import DistributedObjectUD
from direct.directnotify.DirectNotifyGlobal import directNotify
import sys

class DistributedObjectGlobalUD(DistributedObjectUD):
    notify = directNotify.newCategory('DistributedObjectGlobalUD')
    doNotDeallocateChannel = 1
    isGlobalDistObj = 1
    
    def __init__(self, air):
        DistributedObjectUD.__init__(self, air)
        self.ExecNamespace = {
            'self': self }

    
    def announceGenerate(self):
        self.air.registerForChannel(self.doId)
        DistributedObjectUD.announceGenerate(self)

    
    def delete(self):
        self.air.unregisterForChannel(self.doId)
        DistributedObjectUD.delete(self)

    
    def execCommand(self, command, mwMgrId, avId, zoneId):
        text = str(self._DistributedObjectGlobalUD__execMessage(command))[:config.GetInt('ai-debug-length', 300)]
        dclass = uber.air.dclassesByName.get('PiratesMagicWordManagerAI')
        dg = dclass.aiFormatUpdate('setMagicWordResponse', mwMgrId, (1 << 32) + avId, uber.air.ourChannel, [
            text])
        uber.air.send(dg)

    
    def _DistributedObjectGlobalUD__execMessage(self, message):
        if not self.ExecNamespace:
            exec 'from pandac.PandaModules import *' in globals(), self.ExecNamespace
        
        
        try:
            if not isClient():
                print 'EXECWARNING DistributedObjectGlobalUD eval: %s' % message
                printStack()
            
            return str(eval(message, globals(), self.ExecNamespace))
        except SyntaxError:
            
            try:
                if not isClient():
                    print 'EXECWARNING DistributedObjectGlobalUD: %s' % message
                    printStack()
                
                exec message in globals(), self.ExecNamespace
                return 'ok'
            exception = sys.exc_info()[0]
            extraInfo = sys.exc_info()[1]
            if extraInfo:
                return str(extraInfo)
            else:
                return str(exception)

        

        exception = sys.exc_info()[0]
        extraInfo = sys.exc_info()[1]
        if extraInfo:
            return str(extraInfo)
        else:
            return str(exception)



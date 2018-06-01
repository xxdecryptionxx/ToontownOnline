from pandac.PandaModules import *
from toontown.toontowngui import TTDialog
from toontown.toonbase import TTLocalizer

class TutorialForceAcknowledge:
    
    def __init__(self, doneEvent):
        self.doneEvent = doneEvent
        self.dialog = None

    
    def enter(self): # Enter the tutorial
        base.localAvatar.loop('neutral')
        self.doneStatus = {
            'mode': 'incomplete' }
        msg = TTLocalizer.TutorialForceAcknowledgeMessage
        self.dialog = TTDialog.TTDialog(text = msg, command = self.handleOk, style = TTDialog.Acknowledge)

    
    def exit(self): # Exit the tutorial
        if self.dialog:
            self.dialog.cleanup()
            self.dialog = None
        

    
    def handleOk(self, value):
        messenger.send(self.doneEvent, [
            self.doneStatus])



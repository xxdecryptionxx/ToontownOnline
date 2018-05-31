# As far as I know, this is completely unused.
# It's the Bossbot Field Offices, which we don't know much about.
from direct.directnotify.DirectNotifyGlobal import directNotify
from toontown.cogdominium.DistCogdoLevelGame import DistCogdoLevelGame
from toontown.cogdominium.CogdoBoardroomGameBase import CogdoBoardroomGameBase
from toontown.cogdominium import CogdoBoardroomGameConsts as Consts
from toontown.toonbase import ToontownTimer
from toontown.toonbase import TTLocalizer as TTL

class DistCogdoBoardroomGame(CogdoBoardroomGameBase, DistCogdoLevelGame):
    notify = directNotify.newCategory('DistCogdoBoardroomGame')
    
    def __init__(self, cr):
        DistCogdoLevelGame.__init__(self, cr)

    
    def getTitle(self): # "Boardroom Hijinks"
        return TTL.BoardroomGameTitle

    
    def getInstructions(self): # Instructions, you would have to run through a boardroom to get gag destruction memos
        return TTL.BoardroomGameInstructions

    
    def announceGenerate(self):
        DistCogdoLevelGame.announceGenerate(self)
        self.timer = ToontownTimer.ToontownTimer() # You would've been timed for the minigame?
        self.timer.setScale(Consts.Settings.TimerScale.get())
        self.timer.stash()

    
    def disable(self):
        self.timer.destroy()
        self.timer = None
        DistCogdoLevelGame.disable(self)

    
    def enterGame(self): # Entering the game
        DistCogdoLevelGame.enterGame(self)
        timeLeft = Consts.GameDuration.get() - globalClock.getRealTime() - self.getStartTime()
        self.timer.setTime(timeLeft) # Loads the time left until it runs out
        self.timer.countdown(timeLeft, self.timerExpired) # Countdown the time left
        self.timer.unstash()

    
    def enterFinish(self): # Finished the minigame?
        DistCogdoLevelGame.enterFinish(self)
        timeLeft = Consts.FinishDuration.get() - globalClock.getRealTime() - self.getFinishTime()
        self.timer.setTime(timeLeft)
        self.timer.countdown(timeLeft, self.timerExpired)
        self.timer.unstash()

    
    def timerExpired(self): # This wasn't finished
        pass

    if __dev__:
        
        def _handleTimerScaleChanged(self, timerScale):
            if hasattr(self, 'timer'):
                self.timer.setScale(timerScale)
            

    


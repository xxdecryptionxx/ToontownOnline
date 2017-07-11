# File: d (Python 2.4)

from LoggerGlobal import defaultLogger
from direct.showbase import PythonUtil
from libpandaexpress import ConfigVariableBool
import time
import types
import sys

class Notifier:
    serverDelta = 0
    streamWriter = None
    showTime = ConfigVariableBool('notify-timestamp', False)
    
    def __init__(self, name, logger = None):
        self._Notifier__name = name
        if logger == None:
            self._Notifier__logger = defaultLogger
        else:
            self._Notifier__logger = logger
        self._Notifier__info = 1
        self._Notifier__warning = 1
        self._Notifier__debug = 0
        self._Notifier__logging = 0

    
    def setServerDelta(self, delta, timezone):
        delta = int(round(delta))
        Notifier.serverDelta = delta + time.timezone - timezone
        NotifyCategory = NotifyCategory
        import pandac.PandaModules
        NotifyCategory.setServerDelta(self.serverDelta)
        self.info('Notify clock adjusted by %s (and timezone adjusted by %s hours) to synchronize with server.' % (PythonUtil.formatElapsedSeconds(delta), (time.timezone - timezone) / 3600))

    
    def getTime(self):
        return time.strftime(':%m-%d-%Y %H:%M:%S ', time.localtime(time.time() + self.serverDelta))

    
    def getOnlyTime(self):
        return time.strftime('%H:%M:%S', time.localtime(time.time() + self.serverDelta))

    
    def __str__(self):
        return '%s: info = %d, warning = %d, debug = %d, logging = %d' % (self._Notifier__name, self._Notifier__info, self._Notifier__warning, self._Notifier__debug, self._Notifier__logging)

    
    def setSeverity(self, severity):
        NSDebug = NSDebug
        NSInfo = NSInfo
        NSWarning = NSWarning
        NSError = NSError
        import pandac.PandaModules
        if severity >= NSError:
            self.setWarning(0)
            self.setInfo(0)
            self.setDebug(0)
        elif severity == NSWarning:
            self.setWarning(1)
            self.setInfo(0)
            self.setDebug(0)
        elif severity == NSInfo:
            self.setWarning(1)
            self.setInfo(1)
            self.setDebug(0)
        elif severity <= NSDebug:
            self.setWarning(1)
            self.setInfo(1)
            self.setDebug(1)
        

    
    def getSeverity(self):
        NSDebug = NSDebug
        NSInfo = NSInfo
        NSWarning = NSWarning
        NSError = NSError
        import pandac.PandaModules
        if self.getDebug():
            return NSDebug
        elif self.getInfo():
            return NSInfo
        elif self.getWarning():
            return NSWarning
        else:
            return NSError

    
    def error(self, errorString, exception = StandardError):
        message = str(errorString)
        if Notifier.showTime.getValue():
            string = self.getTime() + str(exception) + ': ' + self._Notifier__name + '(error): ' + message
        else:
            string = str(exception) + ': ' + self._Notifier__name + '(error): ' + message
        self._Notifier__log(string)
        raise exception(errorString)

    
    def warning(self, warningString):
        if self._Notifier__warning:
            message = str(warningString)
            if Notifier.showTime.getValue():
                string = self.getTime() + self._Notifier__name + '(warning): ' + message
            else:
                string = ':' + self._Notifier__name + '(warning): ' + message
            self._Notifier__log(string)
            self._Notifier__print(string)
        
        return 1

    
    def setWarning(self, bool):
        self._Notifier__warning = bool

    
    def getWarning(self):
        return self._Notifier__warning

    
    def debug(self, debugString):
        if self._Notifier__debug:
            message = str(debugString)
            if Notifier.showTime.getValue():
                string = self.getTime() + self._Notifier__name + '(debug): ' + message
            else:
                string = ':' + self._Notifier__name + '(debug): ' + message
            self._Notifier__log(string)
            self._Notifier__print(string)
        
        return 1

    
    def setDebug(self, bool):
        self._Notifier__debug = bool

    
    def getDebug(self):
        return self._Notifier__debug

    
    def info(self, infoString):
        if self._Notifier__info:
            message = str(infoString)
            if Notifier.showTime.getValue():
                string = self.getTime() + self._Notifier__name + ': ' + message
            else:
                string = ':' + self._Notifier__name + ': ' + message
            self._Notifier__log(string)
            self._Notifier__print(string)
        
        return 1

    
    def getInfo(self):
        return self._Notifier__info

    
    def setInfo(self, bool):
        self._Notifier__info = bool

    
    def _Notifier__log(self, logEntry):
        if self._Notifier__logging:
            self._Notifier__logger.log(logEntry)
        

    
    def getLogging(self):
        return self._Notifier__logging

    
    def setLogging(self, bool):
        self._Notifier__logging = bool

    
    def _Notifier__print(self, string):
        if self.streamWriter:
            self.streamWriter.appendData(string + '\n')
        else:
            print >>sys.stderr, string

    
    def debugStateCall(self, obj = None, fsmMemberName = 'fsm', secondaryFsm = 'secondaryFSM'):
        if self._Notifier__debug:
            state = ''
            doId = ''
            if obj is not None:
                fsm = obj.__dict__.get(fsmMemberName)
                if fsm is not None:
                    stateObj = fsm.getCurrentState()
                    if stateObj is not None:
                        state = stateObj.getName()
                    
                
                fsm = obj.__dict__.get(secondaryFsm)
                if fsm is not None:
                    stateObj = fsm.getCurrentState()
                    if stateObj is not None:
                        state = '%s, %s' % (state, stateObj.getName())
                    
                
                if hasattr(obj, 'doId'):
                    doId = ' doId:%s' % (obj.doId,)
                
            
            string = ':%s:%s [%-7s] id(%s)%s %s' % (self.getOnlyTime(), self._Notifier__name, state, id(obj), doId, PythonUtil.traceParentCall())
            self._Notifier__log(string)
            self._Notifier__print(string)
        
        return 1

    
    def debugCall(self, debugString = ''):
        if self._Notifier__debug:
            message = str(debugString)
            string = ':%s:%s "%s" %s' % (self.getOnlyTime(), self._Notifier__name, message, PythonUtil.traceParentCall())
            self._Notifier__log(string)
            self._Notifier__print(string)
        
        return 1



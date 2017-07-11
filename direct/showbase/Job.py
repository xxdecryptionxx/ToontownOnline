# File: d (Python 2.4)

from direct.showbase.DirectObject import DirectObject

class Job(DirectObject):
    Done = object()
    Continue = None
    Sleep = object()
    Priorities = ScratchPad(Min = 1, Low = 100, Normal = 1000, High = 10000)
    _SerialGen = SerialNumGen()
    
    def __init__(self, name):
        self._name = name
        self._generator = None
        self._id = Job._SerialGen.next()
        self._printing = False
        self._priority = Job.Priorities.Normal
        self._finished = False

    
    def destroy(self):
        del self._name
        del self._generator
        del self._printing

    
    def getFinishedEvent(self):
        return 'job-finished-%s' % self._id

    
    def run(self):
        raise "don't call down"

    
    def getPriority(self):
        return self._priority

    
    def setPriority(self, priority):
        self._priority = priority

    
    def printingBegin(self):
        self._printing = True

    
    def printingEnd(self):
        self._printing = False

    
    def resume(self):
        pass

    
    def suspend(self):
        pass

    
    def _setFinished(self):
        self._finished = True
        self.finished()

    
    def isFinished(self):
        return self._finished

    
    def finished(self):
        pass

    
    def getJobName(self):
        return self._name

    
    def _getJobId(self):
        return self._id

    
    def _getGenerator(self):
        if self._generator is None:
            self._generator = self.run()
        
        return self._generator

    
    def _cleanupGenerator(self):
        if self._generator is not None:
            self._generator = None
        



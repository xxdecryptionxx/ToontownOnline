# File: d (Python 2.4)

__all__ = [
    'FakeObject',
    '_createGarbage',
    'GarbageReport',
    'GarbageLogger']
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.showbase.PythonUtil import safeRepr, fastRepr, printListEnumGen, printNumberedTypesGen
from direct.showbase.PythonUtil import AlphabetCounter
from direct.showbase.Job import Job
import gc
import types
GarbageCycleCountAnnounceEvent = 'announceGarbageCycleDesc2num'

class FakeObject:
    pass


class FakeDelObject:
    
    def __del__(self):
        pass



def _createGarbage(num = 1):
    for i in xrange(num):
        a = FakeObject()
        b = FakeObject()
        a.other = b
        b.other = a
        a = FakeDelObject()
        b = FakeDelObject()
        a.other = b
        b.other = a
    


class GarbageReport(Job):
    notify = directNotify.newCategory('GarbageReport')
    
    def __init__(self, name, log = True, verbose = False, fullReport = False, findCycles = True, threaded = False, doneCallback = None, autoDestroy = False, priority = None, safeMode = False, delOnly = False, collect = True):
        Job.__init__(self, name)
        self._args = ScratchPad(name = name, log = log, verbose = verbose, fullReport = fullReport, findCycles = findCycles, doneCallback = doneCallback, autoDestroy = autoDestroy, safeMode = safeMode, delOnly = delOnly, collect = collect)
        if priority is not None:
            self.setPriority(priority)
        
        jobMgr.add(self)
        if not threaded:
            jobMgr.finish(self)
        

    
    def run(self):
        oldFlags = gc.get_debug()
        if self._args.delOnly:
            gc.set_debug(0)
            if self._args.collect:
                gc.collect()
            
            garbageInstances = gc.garbage[:]
            del gc.garbage[:]
            if len(garbageInstances) > 0:
                yield None
            
            if self.notify.getDebug():
                self.notify.debug('garbageInstances == %s' % fastRepr(garbageInstances))
            
            self.numGarbageInstances = len(garbageInstances)
            self.garbageInstanceIds = set()
            for i in xrange(len(garbageInstances)):
                self.garbageInstanceIds.add(id(garbageInstances[i]))
                if not i % 20:
                    yield None
                    continue
            
            del garbageInstances
        else:
            self.garbageInstanceIds = set()
        gc.set_debug(gc.DEBUG_SAVEALL)
        if self._args.collect:
            gc.collect()
        
        self.garbage = gc.garbage[:]
        del gc.garbage[:]
        if len(self.garbage) > 0:
            yield None
        
        if self.notify.getDebug():
            self.notify.debug('self.garbage == %s' % fastRepr(self.garbage))
        
        gc.set_debug(oldFlags)
        self.numGarbage = len(self.garbage)
        if self.numGarbage > 0:
            yield None
        
        self.notify.info('found %s items in gc.garbage' % self.numGarbage)
        self._id2index = { }
        self.referrersByReference = { }
        self.referrersByNumber = { }
        self.referentsByReference = { }
        self.referentsByNumber = { }
        self._id2garbageInfo = { }
        self.cycles = []
        self.cyclesBySyntax = []
        self.uniqueCycleSets = set()
        self.cycleIds = set()
        for i in xrange(self.numGarbage):
            self._id2index[id(self.garbage[i])] = i
            if not i % 20:
                yield None
                continue
        
        if self._args.fullReport and self.numGarbage != 0:
            if self._args.verbose:
                self.notify.info('getting referrers...')
            
            for i in xrange(self.numGarbage):
                yield None
                for result in self._getReferrers(self.garbage[i]):
                    yield None
                
                (byNum, byRef) = result
                self.referrersByNumber[i] = byNum
                self.referrersByReference[i] = byRef
            
        
        if self.numGarbage > 0:
            if self._args.verbose:
                self.notify.info('getting referents...')
            
            for i in xrange(self.numGarbage):
                yield None
                for result in self._getReferents(self.garbage[i]):
                    yield None
                
                (byNum, byRef) = result
                self.referentsByNumber[i] = byNum
                self.referentsByReference[i] = byRef
            
        
        for i in xrange(self.numGarbage):
            if hasattr(self.garbage[i], '_garbageInfo') and callable(self.garbage[i]._garbageInfo):
                
                try:
                    info = self.garbage[i]._garbageInfo()
                except Exception:
                    e = None
                    info = str(e)

                self._id2garbageInfo[id(self.garbage[i])] = info
                yield None
                continue
            if not i % 20:
                yield None
                continue
        
        if self._args.findCycles and self.numGarbage > 0:
            if self._args.verbose:
                self.notify.info('calculating cycles...')
            
            for i in xrange(self.numGarbage):
                yield None
                for newCycles in self._getCycles(i, self.uniqueCycleSets):
                    yield None
                
                self.cycles.extend(newCycles)
                newCyclesBySyntax = []
                for cycle in newCycles:
                    cycleBySyntax = ''
                    objs = []
                    for index in cycle[:-1]:
                        objs.append(self.garbage[index])
                        yield None
                    
                    numObjs = len(objs) - 1
                    objs.extend(objs)
                    numToSkip = 0
                    objAlreadyRepresented = False
                    startIndex = 0
                    endIndex = numObjs + 1
                    if type(objs[-1]) is types.InstanceType and type(objs[0]) is types.DictType:
                        startIndex -= 1
                        endIndex -= 1
                    
                    for index in xrange(startIndex, endIndex):
                        if numToSkip:
                            numToSkip -= 1
                            continue
                        
                        obj = objs[index]
                        if type(obj) is types.InstanceType:
                            if not objAlreadyRepresented:
                                cycleBySyntax += '%s' % obj.__class__.__name__
                            
                            cycleBySyntax += '.'
                            numToSkip += 1
                            member = objs[index + 2]
                            for (key, value) in obj.__dict__.iteritems():
                                if value is member:
                                    break
                                
                                yield None
                            else:
                                key = '<unknown member name>'
                            cycleBySyntax += '%s' % key
                            objAlreadyRepresented = True
                            continue
                        if type(obj) is types.DictType:
                            cycleBySyntax += '{'
                            val = objs[index + 1]
                            for (key, value) in obj.iteritems():
                                if value is val:
                                    break
                                
                                yield None
                            else:
                                key = '<unknown key>'
                            cycleBySyntax += '%s}' % fastRepr(key)
                            objAlreadyRepresented = True
                            continue
                        if type(obj) in (types.TupleType, types.ListType):
                            brackets = {
                                types.TupleType: '()',
                                types.ListType: '[]' }[type(obj)]
                            nextObj = objs[index + 1]
                            cycleBySyntax += brackets[0]
                            for index in xrange(len(obj)):
                                if obj[index] is nextObj:
                                    index = str(index)
                                    break
                                
                                yield None
                            else:
                                index = '<unknown index>'
                            cycleBySyntax += '%s%s' % (index, brackets[1])
                            objAlreadyRepresented = True
                            continue
                        cycleBySyntax += '%s --> ' % itype(obj)
                        objAlreadyRepresented = False
                    
                    newCyclesBySyntax.append(cycleBySyntax)
                    yield None
                
                self.cyclesBySyntax.extend(newCyclesBySyntax)
                if not self._args.fullReport:
                    for cycle in newCycles:
                        yield None
                        self.cycleIds.update(set(cycle))
                    
            
        
        self.numCycles = len(self.cycles)
        if self._args.findCycles:
            s = [
                "===== GarbageReport: '%s' (%s %s) =====" % (self._args.name, self.numCycles, choice(self.numCycles == 1, 'cycle', 'cycles'))]
        else:
            s = [
                "===== GarbageReport: '%s' =====" % self._args.name]
        if self.numGarbage > 0:
            if self._args.fullReport:
                garbageIndices = range(self.numGarbage)
            else:
                garbageIndices = list(self.cycleIds)
                garbageIndices.sort()
            numGarbage = len(garbageIndices)
            if not self._args.fullReport:
                abbrev = '(abbreviated) '
            else:
                abbrev = ''
            s.append('===== Garbage Items %s=====' % abbrev)
            digits = 0
            n = numGarbage
            while n > 0:
                yield None
                digits += 1
                n /= 10
            digits = digits
            format = '%0' + '%s' % digits + 'i:%s \t%s'
            for i in xrange(numGarbage):
                yield None
                idx = garbageIndices[i]
                if self._args.safeMode:
                    objStr = repr(itype(self.garbage[idx]))
                else:
                    objStr = fastRepr(self.garbage[idx])
                maxLen = 5000
                if len(objStr) > maxLen:
                    snip = '<SNIP>'
                    objStr = '%s%s' % (objStr[:maxLen - len(snip)], snip)
                
                s.append(format % (idx, itype(self.garbage[idx]), objStr))
            
            s.append('===== Garbage Item Types %s=====' % abbrev)
            for i in xrange(numGarbage):
                yield None
                idx = garbageIndices[i]
                objStr = str(deeptype(self.garbage[idx]))
                maxLen = 5000
                if len(objStr) > maxLen:
                    snip = '<SNIP>'
                    objStr = '%s%s' % (objStr[:maxLen - len(snip)], snip)
                
                s.append(format % (idx, itype(self.garbage[idx]), objStr))
            
            if self._args.findCycles:
                s.append('===== Garbage Cycles (Garbage Item Numbers) =====')
                ac = AlphabetCounter()
                for i in xrange(self.numCycles):
                    yield None
                    s.append('%s:%s' % (ac.next(), self.cycles[i]))
                
            
            if self._args.findCycles:
                s.append('===== Garbage Cycles (Python Syntax) =====')
                ac = AlphabetCounter()
                for i in xrange(len(self.cyclesBySyntax)):
                    yield None
                    s.append('%s:%s' % (ac.next(), self.cyclesBySyntax[i]))
                
            
            if len(self._id2garbageInfo):
                format = '%0' + '%s' % digits + 'i:%s'
                s.append('===== Garbage Custom Info =====')
                ids = self._id2garbageInfo.keys()
                yield None
                indices = []
                for _id in ids:
                    indices.append(self._id2index[_id])
                    yield None
                
                indices.sort()
                yield None
                for i in indices:
                    _id = id(self.garbage[i])
                    s.append(format % (i, self._id2garbageInfo[_id]))
                    yield None
                
            
            if self._args.fullReport:
                format = '%0' + '%s' % digits + 'i:%s'
                s.append('===== Referrers By Number (what is referring to garbage item?) =====')
                for i in xrange(numGarbage):
                    yield None
                    s.append(format % (i, self.referrersByNumber[i]))
                
                s.append('===== Referents By Number (what is garbage item referring to?) =====')
                for i in xrange(numGarbage):
                    yield None
                    s.append(format % (i, self.referentsByNumber[i]))
                
                s.append('===== Referrers (what is referring to garbage item?) =====')
                for i in xrange(numGarbage):
                    yield None
                    s.append(format % (i, self.referrersByReference[i]))
                
                s.append('===== Referents (what is garbage item referring to?) =====')
                for i in xrange(numGarbage):
                    yield None
                    s.append(format % (i, self.referentsByReference[i]))
                
            
        
        self._report = s
        if self._args.log:
            self.printingBegin()
            for i in xrange(len(self._report)):
                if self.numGarbage > 0:
                    yield None
                
                self.notify.info(self._report[i])
            
            self.notify.info('===== Garbage Report Done =====')
            self.printingEnd()
        
        yield Job.Done

    
    def finished(self):
        if self._args.doneCallback:
            self._args.doneCallback(self)
        
        if self._args.autoDestroy:
            self.destroy()
        

    
    def destroy(self):
        del self._args
        del self.garbage
        del self.referrersByReference
        del self.referrersByNumber
        del self.referentsByReference
        del self.referentsByNumber
        if hasattr(self, 'cycles'):
            del self.cycles
        
        del self._report
        if hasattr(self, '_reportStr'):
            del self._reportStr
        
        Job.destroy(self)

    
    def getNumCycles(self):
        return self.numCycles

    
    def getDesc2numDict(self):
        desc2num = { }
        for cycleBySyntax in self.cyclesBySyntax:
            desc2num.setdefault(cycleBySyntax, 0)
            desc2num[cycleBySyntax] += 1
        
        return desc2num

    
    def getGarbage(self):
        return self.garbage

    
    def getReport(self):
        if not hasattr(self, '_reportStr'):
            self._reportStr = ''
            for str in self._report:
                self._reportStr += '\n' + str
            
        
        return self._reportStr

    
    def _getReferrers(self, obj):
        yield None
        byRef = gc.get_referrers(obj)
        yield None
        byNum = []
        for i in xrange(len(byRef)):
            if not i % 20:
                yield None
            
            referrer = byRef[i]
            num = self._id2index.get(id(referrer), None)
            byNum.append(num)
        
        yield (byNum, byRef)

    
    def _getReferents(self, obj):
        yield None
        byRef = gc.get_referents(obj)
        yield None
        byNum = []
        for i in xrange(len(byRef)):
            if not i % 20:
                yield None
            
            referent = byRef[i]
            num = self._id2index.get(id(referent), None)
            byNum.append(num)
        
        yield (byNum, byRef)

    
    def _getNormalizedCycle(self, cycle):
        if len(cycle) == 0:
            return cycle
        
        min = 1 << 30
        minIndex = None
        for i in xrange(len(cycle)):
            elem = cycle[i]
            if elem < min:
                min = elem
                minIndex = i
                continue
        
        return cycle[minIndex:] + cycle[:minIndex]

    
    def _getCycles(self, index, uniqueCycleSets = None):
        cycles = []
        if uniqueCycleSets is None:
            uniqueCycleSets = set()
        
        stateStack = Stack()
        rootId = index
        objId = id(self.garbage[rootId])
        numDelInstances = choice(objId in self.garbageInstanceIds, 1, 0)
        stateStack.push(([
            rootId], rootId, numDelInstances, 0))
        while True:
            yield None
            if len(stateStack) == 0:
                break
            
            (candidateCycle, curId, numDelInstances, resumeIndex) = stateStack.pop()
            if self.notify.getDebug():
                if self._args.delOnly:
                    print 'restart: %s root=%s cur=%s numDelInstances=%s resume=%s' % (candidateCycle, rootId, curId, numDelInstances, resumeIndex)
                else:
                    print 'restart: %s root=%s cur=%s resume=%s' % (candidateCycle, rootId, curId, resumeIndex)
            
            for index in xrange(resumeIndex, len(self.referentsByNumber[curId])):
                yield None
                refId = self.referentsByNumber[curId][index]
                if self.notify.getDebug():
                    print '       : %s -> %s' % (curId, refId)
                
                if refId == rootId:
                    normCandidateCycle = self._getNormalizedCycle(candidateCycle)
                    normCandidateCycleTuple = tuple(normCandidateCycle)
                    if normCandidateCycleTuple not in uniqueCycleSets:
                        if not (self._args.delOnly) or numDelInstances >= 1:
                            if self.notify.getDebug():
                                print '  FOUND: ', normCandidateCycle + [
normCandidateCycle[0]]
                            
                            cycles.append(normCandidateCycle + [
                                normCandidateCycle[0]])
                            uniqueCycleSets.add(normCandidateCycleTuple)
                        
                    
                normCandidateCycleTuple not in uniqueCycleSets
                if refId in candidateCycle:
                    continue
                if refId is not None:
                    objId = id(self.garbage[refId])
                    numDelInstances += choice(objId in self.garbageInstanceIds, 1, 0)
                    stateStack.push((list(candidateCycle), curId, numDelInstances, index + 1))
                    stateStack.push((list(candidateCycle) + [
                        refId], refId, numDelInstances, 0))
                    break
                    continue
            
        yield cycles



class GarbageLogger(GarbageReport):
    
    def __init__(self, name, *args, **kArgs):
        kArgs['log'] = True
        kArgs['autoDestroy'] = True
        GarbageReport.__init__(self, name, *args, **args)



class _CFGLGlobals:
    LastNumGarbage = 0
    LastNumCycles = 0


def checkForGarbageLeaks():
    gc.collect()
    numGarbage = len(gc.garbage)
    if numGarbage > 0 and config.GetBool('auto-garbage-logging', 0):
        if numGarbage != _CFGLGlobals.LastNumGarbage:
            print 
            gr = GarbageReport('found garbage', threaded = False, collect = False)
            print 
            _CFGLGlobals.LastNumGarbage = numGarbage
            _CFGLGlobals.LastNumCycles = gr.getNumCycles()
            messenger.send(GarbageCycleCountAnnounceEvent, [
                gr.getDesc2numDict()])
            gr.destroy()
        
        notify = directNotify.newCategory('GarbageDetect')
        if config.GetBool('allow-garbage-cycles', 1):
            func = notify.warning
        else:
            func = notify.error
        func('%s garbage cycles found, see info above' % _CFGLGlobals.LastNumCycles)
    
    return numGarbage


def b_checkForGarbageLeaks(wantReply = False):
    if not __dev__:
        return 0
    
    
    try:
        pass
    except:
        pass

    if base.cr.timeManager:
        base.cr.timeManager.d_checkForGarbageLeaks(wantReply = wantReply)
    
    return checkForGarbageLeaks()


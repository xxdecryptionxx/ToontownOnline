# File: d (Python 2.4)

from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.showbase.PythonUtil import Queue, fastRepr, invertDictLossless
from direct.showbase.PythonUtil import itype, safeRepr
from direct.showbase.Job import Job
import types

class ContainerReport(Job):
    notify = directNotify.newCategory('ContainerReport')
    PrivateIds = set()
    
    def __init__(self, name, log = False, limit = None, threaded = False):
        Job.__init__(self, name)
        self._log = log
        self._limit = limit
        self._visitedIds = set()
        self._id2pathStr = { }
        self._id2container = { }
        self._type2id2len = { }
        self._instanceDictIds = set()
        self._queue = Queue()
        jobMgr.add(self)
        if threaded == False:
            jobMgr.finish(self)
        

    
    def destroy(self):
        del self._queue
        del self._instanceDictIds
        del self._type2id2len
        del self._id2container
        del self._id2pathStr
        del self._visitedIds
        del self._limit
        del self._log

    
    def finished(self):
        if self._log:
            self.destroy()
        

    
    def run(self):
        ContainerReport.PrivateIds.update(set([
            id(ContainerReport.PrivateIds),
            id(self._visitedIds),
            id(self._id2pathStr),
            id(self._id2container),
            id(self._type2id2len),
            id(self._queue),
            id(self._instanceDictIds)]))
        
        try:
            pass
        except:
            pass

        self._enqueueContainer(base.__dict__, 'base')
        
        try:
            pass
        except:
            pass

        self._enqueueContainer(simbase.__dict__, 'simbase')
        self._queue.push(__builtins__)
        self._id2pathStr[id(__builtins__)] = ''
        while len(self._queue) > 0:
            yield None
            parentObj = self._queue.pop()
            isInstanceDict = False
            if id(parentObj) in self._instanceDictIds:
                isInstanceDict = True
            
            
            try:
                if parentObj.__class__.__name__ == 'method-wrapper':
                    continue
            except:
                pass

            if type(parentObj) in (types.StringType, types.UnicodeType):
                continue
            
            if type(parentObj) in (types.ModuleType, types.InstanceType):
                child = parentObj.__dict__
                if self._examine(child):
                    self._instanceDictIds.add(id(child))
                    self._id2pathStr[id(child)] = str(self._id2pathStr[id(parentObj)])
                    continue
                continue
            
            if type(parentObj) is types.DictType:
                key = None
                attr = None
                keys = parentObj.keys()
                
                try:
                    keys.sort()
                except TypeError:
                    e = None
                    self.notify.warning('non-sortable dict keys: %s: %s' % (self._id2pathStr[id(parentObj)], repr(e)))

                for key in keys:
                    
                    try:
                        attr = parentObj[key]
                    except KeyError:
                        e = None
                        self.notify.warning('could not index into %s with key %s' % (self._id2pathStr[id(parentObj)], key))

                    if id(attr) not in self._visitedIds:
                        self._visitedIds.add(id(attr))
                        if self._examine(attr):
                            if parentObj is __builtins__:
                                self._id2pathStr[id(attr)] = key
                            elif isInstanceDict:
                                self._id2pathStr[id(attr)] = self._id2pathStr[id(parentObj)] + '.%s' % key
                            else:
                                self._id2pathStr[id(attr)] = self._id2pathStr[id(parentObj)] + '[%s]' % safeRepr(key)
                        
                    self._examine(attr)
                
                del key
                del attr
                continue
            
            if type(parentObj) is not types.FileType:
                
                try:
                    itr = iter(parentObj)
                except:
                    pass

                
                try:
                    index = 0
                    while None:
                        
                        try:
                            attr = itr.next()
                        except:
                            attr = None
                            break

                        if id(attr) not in self._visitedIds:
                            self._visitedIds.add(id(attr))
                            if self._examine(attr):
                                self._id2pathStr[id(attr)] = self._id2pathStr[id(parentObj)] + '[%s]' % index
                            
                        
                        index += 1
                    del attr
                except StopIteration:
                    e = None

                del itr
                continue
            
            
            try:
                childNames = dir(parentObj)
            except:
                continue

            childName = None
            child = None
            for childName in childNames:
                child = getattr(parentObj, childName)
                if id(child) not in self._visitedIds:
                    self._visitedIds.add(id(child))
                    if self._examine(child):
                        self._id2pathStr[id(child)] = self._id2pathStr[id(parentObj)] + '.%s' % childName
                    
                self._examine(child)
            
            del childName
            del child
            continue
        if self._log:
            self.printingBegin()
            for i in self._output(limit = self._limit):
                yield None
            
            self.printingEnd()
        
        yield Job.Done

    
    def _enqueueContainer(self, obj, pathStr = None):
        self._queue.push(obj)
        objId = id(obj)
        if pathStr is not None:
            self._id2pathStr[objId] = pathStr
        
        
        try:
            length = len(obj)
        except:
            length = None

        if length is not None and length > 0:
            self._id2container[objId] = obj
            self._type2id2len.setdefault(type(obj), { })
            self._type2id2len[type(obj)][objId] = length
        

    
    def _examine(self, obj):
        if type(obj) in (types.BooleanType, types.BuiltinFunctionType, types.BuiltinMethodType, types.ComplexType, types.FloatType, types.IntType, types.LongType, types.NoneType, types.NotImplementedType, types.TypeType, types.CodeType, types.FunctionType):
            return False
        
        if id(obj) in ContainerReport.PrivateIds:
            return False
        
        self._enqueueContainer(obj)
        return True

    
    def _outputType(self, type, limit = None):
        if type not in self._type2id2len:
            return None
        
        len2ids = invertDictLossless(self._type2id2len[type])
        lengths = len2ids.keys()
        lengths.sort()
        lengths.reverse()
        print '====='
        print '===== %s' % type
        count = 0
        stop = False
        for l in lengths:
            pathStrList = list()
            for id in len2ids[l]:
                obj = self._id2container[id]
                pathStrList.append(self._id2pathStr[id])
                count += 1
                if count & 127 == 0:
                    yield None
                    continue
            
            pathStrList.sort()
            for pathstr in pathStrList:
                print '%s: %s' % (l, pathstr)
            
            if limit is not None and count >= limit:
                return None
                continue
        

    
    def _output(self, **kArgs):
        print "===== ContainerReport: '%s' =====" % (self._name,)
        initialTypes = (types.DictType, types.ListType, types.TupleType)
        for type in initialTypes:
            for i in self._outputType(type, **None):
                yield None
            
        
        otherTypes = list(set(self._type2id2len.keys()).difference(set(initialTypes)))
        otherTypes.sort()
        for type in otherTypes:
            for i in self._outputType(type, **None):
                yield None
            
        

    
    def log(self, **kArgs):
        self._output(**None)



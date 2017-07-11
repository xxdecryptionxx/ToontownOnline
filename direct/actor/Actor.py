# File: d (Python 2.4)

__all__ = [
    'Actor']
from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import LODNode
import types
import copy

class Actor(DirectObject, NodePath):
    notify = directNotify.newCategory('Actor')
    partPrefix = '__Actor_'
    modelLoaderOptions = LoaderOptions(LoaderOptions.LFSearch | LoaderOptions.LFReportErrors | LoaderOptions.LFConvertSkeleton)
    animLoaderOptions = LoaderOptions(LoaderOptions.LFSearch | LoaderOptions.LFReportErrors | LoaderOptions.LFConvertAnim)
    validateSubparts = ConfigVariableBool('validate-subparts', True)
    
    class PartDef:
        
        def __init__(self, partBundleNP, partBundleHandle, partModel):
            self.partBundleNP = partBundleNP
            self.partBundleHandle = partBundleHandle
            self.partModel = partModel

        
        def getBundle(self):
            return self.partBundleHandle.getBundle()

        
        def __repr__(self):
            return 'Actor.PartDef(%s, %s)' % (repr(self.partBundleNP), repr(self.partModel))


    
    class AnimDef:
        
        def __init__(self, filename = None, animBundle = None):
            self.filename = filename
            self.animBundle = None
            self.animControl = None

        
        def makeCopy(self):
            return Actor.AnimDef(self.filename, self.animBundle)

        
        def __repr__(self):
            return 'Actor.AnimDef(%s)' % repr(self.filename)


    
    class SubpartDef:
        
        def __init__(self, truePartName, subset = PartSubset()):
            self.truePartName = truePartName
            self.subset = subset

        
        def makeCopy(self):
            return Actor.SubpartDef(self.truePartName, PartSubset(self.subset))

        
        def __repr__(self):
            return 'Actor.SubpartDef(%s, %s)' % (repr(self.truePartName), repr(self.subset))


    
    def __init__(self, models = None, anims = None, other = None, copy = True, lodNode = None, flattenable = True, setFinal = False, mergeLODBundles = None, allowAsyncBind = None, okMissing = None):
        
        try:
            return None
        except:
            self.Actor_initialized = 1

        NodePath.__init__(self)
        if mergeLODBundles == None:
            self.mergeLODBundles = base.config.GetBool('merge-lod-bundles', True)
        else:
            self.mergeLODBundles = mergeLODBundles
        if allowAsyncBind == None:
            self.allowAsyncBind = base.config.GetBool('allow-async-bind', True)
        else:
            self.allowAsyncBind = allowAsyncBind
        self._Actor__commonBundleHandles = { }
        self._Actor__partBundleDict = { }
        self._Actor__subpartDict = { }
        self._Actor__sortedLODNames = []
        self._Actor__animControlDict = { }
        self._Actor__subpartsComplete = False
        self._Actor__LODNode = None
        self._Actor__LODAnimation = None
        self._Actor__LODCenter = Point3(0, 0, 0)
        self.switches = None
        if other == None:
            self.gotName = 0
            if flattenable:
                root = PandaNode('actor')
                self.assign(NodePath(root))
                self.setGeomNode(NodePath(self))
            else:
                root = ModelNode('actor')
                root.setPreserveTransform(1)
                self.assign(NodePath(root))
                self.setGeomNode(self.attachNewNode(ModelNode('actorGeom')))
            self._Actor__hasLOD = 0
            if models:
                if type(models) == type({ }):
                    if type(models[models.keys()[0]]) == type({ }):
                        self.setLODNode(node = lodNode)
                        sortedKeys = models.keys()
                        sortedKeys.sort()
                        for lodName in sortedKeys:
                            self.addLOD(str(lodName))
                            for modelName in models[lodName].keys():
                                self.loadModel(models[lodName][modelName], modelName, lodName, copy = copy, okMissing = okMissing)
                            
                        
                    elif type(anims[anims.keys()[0]]) == type({ }):
                        for partName in models.keys():
                            self.loadModel(models[partName], partName, copy = copy, okMissing = okMissing)
                        
                    else:
                        self.setLODNode(node = lodNode)
                        sortedKeys = models.keys()
                        sortedKeys.sort()
                        for lodName in sortedKeys:
                            self.addLOD(str(lodName))
                            self.loadModel(models[lodName], lodName = lodName, copy = copy, okMissing = okMissing)
                        
                else:
                    self.loadModel(models, copy = copy, okMissing = okMissing)
            
            if anims:
                if len(anims) >= 1:
                    if type(anims[anims.keys()[0]]) == type({ }):
                        if type(models) == type({ }):
                            if type(models[models.keys()[0]]) == type({ }):
                                sortedKeys = models.keys()
                                sortedKeys.sort()
                                for lodName in sortedKeys:
                                    for partName in anims.keys():
                                        self.loadAnims(anims[partName], partName, lodName)
                                    
                                
                            else:
                                for partName in anims.keys():
                                    self.loadAnims(anims[partName], partName)
                                
                        
                    elif type(models) == type({ }):
                        sortedKeys = models.keys()
                        sortedKeys.sort()
                        for lodName in sortedKeys:
                            self.loadAnims(anims, lodName = lodName)
                        
                    else:
                        self.loadAnims(anims)
                
            
        else:
            self.copyActor(other, True)
        if setFinal:
            self._Actor__geomNode.node().setFinal(1)
        

    
    def delete(self):
        
        try:
            return None
        except:
            self.Actor_deleted = 1
            self.cleanup()


    
    def copyActor(self, other, overwrite = False):
        self.gotName = other.gotName
        if overwrite:
            otherCopy = other.copyTo(NodePath())
            otherCopy.detachNode()
            self.assign(otherCopy)
        else:
            otherCopy = other.copyTo(self)
        if other.getGeomNode().getName() == other.getName():
            self.setGeomNode(otherCopy)
        else:
            self.setGeomNode(otherCopy.getChild(0))
        self.switches = other.switches
        self._Actor__LODNode = self.find('**/+LODNode')
        self._Actor__hasLOD = 0
        if not self._Actor__LODNode.isEmpty():
            self._Actor__hasLOD = 1
        
        self._Actor__copyPartBundles(other)
        self._Actor__copySubpartDict(other)
        self._Actor__subpartsComplete = other._Actor__subpartsComplete
        self._Actor__copyAnimControls(other)

    
    def __cmp__(self, other):
        if self is other:
            return 0
        else:
            return 1

    
    def __str__(self):
        return 'Actor %s, parts = %s, LODs = %s, anims = %s' % (self.getName(), self.getPartNames(), self.getLODNames(), self.getAnimNames())

    
    def listJoints(self, partName = 'modelRoot', lodName = 'lodRoot'):
        if self.mergeLODBundles:
            partBundleDict = self._Actor__commonBundleHandles
        else:
            partBundleDict = self._Actor__partBundleDict.get(lodName)
            if not partBundleDict:
                Actor.notify.error('no lod named: %s' % lodName)
            
        subpartDef = self._Actor__subpartDict.get(partName, Actor.SubpartDef(partName))
        partDef = partBundleDict.get(subpartDef.truePartName)
        if partDef == None:
            Actor.notify.error('no part named: %s' % partName)
        
        self._Actor__doListJoints(0, partDef.getBundle(), subpartDef.subset.isIncludeEmpty(), subpartDef.subset)

    
    def _Actor__doListJoints(self, indentLevel, part, isIncluded, subset):
        name = part.getName()
        if subset.matchesInclude(name):
            isIncluded = True
        elif subset.matchesExclude(name):
            isIncluded = False
        
        if isIncluded:
            value = ''
            if hasattr(part, 'outputValue'):
                lineStream = LineStream.LineStream()
                part.outputValue(lineStream)
                value = lineStream.getLine()
            
            print ' ' * indentLevel, part.getName(), value
        
        for i in range(part.getNumChildren()):
            self._Actor__doListJoints(indentLevel + 2, part.getChild(i), isIncluded, subset)
        

    
    def getActorInfo(self):
        lodInfo = []
        for (lodName, partDict) in self._Actor__animControlDict.items():
            if self.mergeLODBundles:
                lodName = self._Actor__sortedLODNames[0]
            
            partInfo = []
            for partName in partDict.keys():
                subpartDef = self._Actor__subpartDict.get(partName, Actor.SubpartDef(partName))
                partBundleDict = self._Actor__partBundleDict.get(lodName)
                partDef = partBundleDict.get(subpartDef.truePartName)
                partBundle = partDef.getBundle()
                animDict = partDict[partName]
                animInfo = []
                for animName in animDict.keys():
                    file = animDict[animName].filename
                    animControl = animDict[animName].animControl
                    animInfo.append([
                        animName,
                        file,
                        animControl])
                
                partInfo.append([
                    partName,
                    partBundle,
                    animInfo])
            
            lodInfo.append([
                lodName,
                partInfo])
        
        return lodInfo

    
    def getAnimNames(self):
        animNames = []
        for (lodName, lodInfo) in self.getActorInfo():
            for (partName, bundle, animInfo) in lodInfo:
                for (animName, file, animControl) in animInfo:
                    if animName not in animNames:
                        animNames.append(animName)
                        continue
                
            
        
        return animNames

    
    def pprint(self):
        for (lodName, lodInfo) in self.getActorInfo():
            print 'LOD:', lodName
            for (partName, bundle, animInfo) in lodInfo:
                print '  Part:', partName
                print '  Bundle:', repr(bundle)
                for (animName, file, animControl) in animInfo:
                    print '    Anim:', animName
                    print '      File:', file
                    if animControl == None:
                        print ' (not loaded)'
                        continue
                    print '      NumFrames: %d PlayRate: %0.2f' % (animControl.getNumFrames(), animControl.getPlayRate())
                
            
        

    
    def cleanup(self):
        self.stop(None)
        self.clearPythonData()
        self.flush()
        if self._Actor__geomNode:
            self._Actor__geomNode.removeNode()
            self._Actor__geomNode = None
        
        if not self.isEmpty():
            self.removeNode()
        

    
    def removeNode(self):
        if self._Actor__geomNode and self._Actor__geomNode.getNumChildren() > 0:
            pass
        1
        NodePath.removeNode(self)

    
    def clearPythonData(self):
        self._Actor__commonBundleHandles = { }
        self._Actor__partBundleDict = { }
        self._Actor__subpartDict = { }
        self._Actor__sortedLODNames = []
        self._Actor__animControlDict = { }

    
    def flush(self):
        self.clearPythonData()
        if self._Actor__LODNode and not self._Actor__LODNode.isEmpty():
            self._Actor__LODNode.removeNode()
            self._Actor__LODNode = None
        
        if self._Actor__geomNode:
            self._Actor__geomNode.removeChildren()
        
        self._Actor__hasLOD = 0

    
    def getAnimControlDict(self):
        return self._Actor__animControlDict

    
    def removeAnimControlDict(self):
        self._Actor__animControlDict = { }

    
    def getPartBundleDict(self):
        return self._Actor__partBundleDict

    
    def getPartBundles(self, partName = None):
        bundles = []
        for (lodName, partBundleDict) in self._Actor__partBundleDict.items():
            if partName == None:
                for partDef in partBundleDict.values():
                    bundles.append(partDef.getBundle())
                
            subpartDef = self._Actor__subpartDict.get(partName, Actor.SubpartDef(partName))
            partDef = partBundleDict.get(subpartDef.truePartName)
            if partDef != None:
                bundles.append(partDef.getBundle())
                continue
            Actor.notify.warning("Couldn't find part: %s" % partName)
        
        return bundles

    
    def _Actor__updateSortedLODNames(self):
        self._Actor__sortedLODNames = self._Actor__partBundleDict.keys()
        
        def sortFunc(x, y):
            if not str(x).isdigit():
                smap = {
                    'h': 3,
                    'm': 2,
                    'l': 1,
                    'f': 0 }
                return cmp(smap[y[0]], smap[x[0]])
            else:
                return cmp(int(y), int(x))

        self._Actor__sortedLODNames.sort(sortFunc)

    
    def getLODNames(self):
        return self._Actor__sortedLODNames

    
    def getPartNames(self):
        partNames = []
        if self._Actor__partBundleDict:
            partNames = self._Actor__partBundleDict.values()[0].keys()
        
        return partNames + self._Actor__subpartDict.keys()

    
    def getGeomNode(self):
        return self._Actor__geomNode

    
    def setGeomNode(self, node):
        self._Actor__geomNode = node

    
    def getLODNode(self):
        return self._Actor__LODNode.node()

    
    def setLODNode(self, node = None):
        if node == None:
            node = LODNode.makeDefaultLod('lod')
        
        if self._Actor__LODNode:
            self._Actor__LODNode = node
        else:
            self._Actor__LODNode = self._Actor__geomNode.attachNewNode(node)
            self._Actor__hasLOD = 1
            self.switches = { }

    
    def useLOD(self, lodName):
        child = self._Actor__LODNode.find(str(lodName))
        index = self._Actor__LODNode.node().findChild(child.node())
        self._Actor__LODNode.node().forceSwitch(index)

    
    def printLOD(self):
        sortedKeys = self._Actor__sortedLODNames
        for eachLod in sortedKeys:
            print 'python switches for %s: in: %d, out %d' % (eachLod, self.switches[eachLod][0], self.switches[eachLod][1])
        
        switchNum = self._Actor__LODNode.node().getNumSwitches()
        for eachSwitch in range(0, switchNum):
            print 'c++ switches for %d: in: %d, out: %d' % (eachSwitch, self._Actor__LODNode.node().getIn(eachSwitch), self._Actor__LODNode.node().getOut(eachSwitch))
        

    
    def resetLOD(self):
        self._Actor__LODNode.node().clearForceSwitch()

    
    def addLOD(self, lodName, inDist = 0, outDist = 0, center = None):
        self._Actor__LODNode.attachNewNode(str(lodName))
        self.switches[lodName] = [
            inDist,
            outDist]
        self._Actor__LODNode.node().addSwitch(inDist, outDist)
        if center != None:
            self.setCenter(center)
        

    
    def setLOD(self, lodName, inDist = 0, outDist = 0):
        self.switches[lodName] = [
            inDist,
            outDist]
        self._Actor__LODNode.node().setSwitch(self.getLODIndex(lodName), inDist, outDist)

    
    def getLODIndex(self, lodName):
        return list(self._Actor__LODNode.getChildren()).index(self.getLOD(lodName))

    
    def getLOD(self, lodName):
        if self._Actor__LODNode:
            lod = self._Actor__LODNode.find(str(lodName))
            if lod.isEmpty():
                return None
            else:
                return lod
        else:
            return None

    
    def hasLOD(self):
        return self._Actor__hasLOD

    
    def setCenter(self, center):
        if center == None:
            center = Point3(0, 0, 0)
        
        self._Actor__LODCenter = center
        if self._Actor__LODNode:
            self._Actor__LODNode.node().setCenter(self._Actor__LODCenter)
        
        if self._Actor__LODAnimation:
            self.setLODAnimation(*self._Actor__LODAnimation)
        

    
    def setLODAnimation(self, farDistance, nearDistance, delayFactor):
        self._Actor__LODAnimation = (farDistance, nearDistance, delayFactor)
        for lodData in self._Actor__partBundleDict.values():
            for partData in lodData.values():
                char = partData.partBundleNP
                char.node().setLodAnimation(self._Actor__LODCenter, farDistance, nearDistance, delayFactor)
            
        

    
    def clearLODAnimation(self):
        self._Actor__LODAnimation = None
        for lodData in self._Actor__partBundleDict.values():
            for partData in lodData.values():
                char = partData.partBundleNP
                char.node().clearLodAnimation()
            
        

    
    def update(self, lod = 0, partName = None, lodName = None, force = False):
        if lodName == None:
            lodNames = self.getLODNames()
        else:
            lodNames = [
                lodName]
        anyChanged = False
        if lod < len(lodNames):
            lodName = lodNames[lod]
            if partName == None:
                partBundleDict = self._Actor__partBundleDict[lodName]
                partNames = partBundleDict.keys()
            else:
                partNames = [
                    partName]
            for partName in partNames:
                partBundle = self.getPartBundle(partName, lodNames[lod])
                if force:
                    if partBundle.forceUpdate():
                        anyChanged = True
                    
                partBundle.forceUpdate()
                if partBundle.update():
                    anyChanged = True
                    continue
            
        else:
            self.notify.warning('update() - no lod: %d' % lod)
        return anyChanged

    
    def getFrameRate(self, animName = None, partName = None):
        lodName = self._Actor__animControlDict.keys()[0]
        controls = self.getAnimControls(animName, partName)
        if len(controls) == 0:
            return None
        
        return controls[0].getFrameRate()

    
    def getBaseFrameRate(self, animName = None, partName = None):
        lodName = self._Actor__animControlDict.keys()[0]
        controls = self.getAnimControls(animName, partName)
        if len(controls) == 0:
            return None
        
        return controls[0].getAnim().getBaseFrameRate()

    
    def getPlayRate(self, animName = None, partName = None):
        if self._Actor__animControlDict:
            lodName = self._Actor__animControlDict.keys()[0]
            controls = self.getAnimControls(animName, partName)
            if controls:
                return controls[0].getPlayRate()
            
        

    
    def setPlayRate(self, rate, animName, partName = None):
        for control in self.getAnimControls(animName, partName):
            control.setPlayRate(rate)
        

    
    def getDuration(self, animName = None, partName = None, fromFrame = None, toFrame = None):
        lodName = self._Actor__animControlDict.keys()[0]
        controls = self.getAnimControls(animName, partName)
        if len(controls) == 0:
            return None
        
        animControl = controls[0]
        if fromFrame is None:
            fromFrame = 0
        
        if toFrame is None:
            toFrame = animControl.getNumFrames() - 1
        
        return (toFrame + 1 - fromFrame) / animControl.getFrameRate()

    
    def getNumFrames(self, animName = None, partName = None):
        lodName = self._Actor__animControlDict.keys()[0]
        controls = self.getAnimControls(animName, partName)
        if len(controls) == 0:
            return None
        
        return controls[0].getNumFrames()

    
    def getFrameTime(self, anim, frame, partName = None):
        numFrames = self.getNumFrames(anim, partName)
        animTime = self.getDuration(anim, partName)
        frameTime = animTime * float(frame) / numFrames
        return frameTime

    
    def getCurrentAnim(self, partName = None):
        if len(self._Actor__animControlDict.items()) == 0:
            return None
        
        (lodName, animControlDict) = self._Actor__animControlDict.items()[0]
        if partName == None:
            (partName, animDict) = animControlDict.items()[0]
        else:
            animDict = animControlDict.get(partName)
            if animDict == None:
                Actor.notify.warning("couldn't find part: %s" % partName)
                return None
            
        for (animName, anim) in animDict.items():
            if anim.animControl and anim.animControl.isPlaying():
                return animName
                continue
        

    
    def getCurrentFrame(self, animName = None, partName = None):
        (lodName, animControlDict) = self._Actor__animControlDict.items()[0]
        if partName == None:
            (partName, animDict) = animControlDict.items()[0]
        else:
            animDict = animControlDict.get(partName)
            if animDict == None:
                Actor.notify.warning("couldn't find part: %s" % partName)
                return None
            
        if animName:
            anim = animDict.get(animName)
            if not anim:
                Actor.notify.warning("couldn't find anim: %s" % animName)
            elif anim.animControl:
                return anim.animControl.getFrame()
            
        else:
            for (animName, anim) in animDict.items():
                if anim.animControl and anim.animControl.isPlaying():
                    return anim.animControl.getFrame()
                    continue
            

    
    def getPart(self, partName, lodName = 'lodRoot'):
        partBundleDict = self._Actor__partBundleDict.get(lodName)
        if not partBundleDict:
            Actor.notify.warning('no lod named: %s' % lodName)
            return None
        
        subpartDef = self._Actor__subpartDict.get(partName, Actor.SubpartDef(partName))
        partDef = partBundleDict.get(subpartDef.truePartName)
        if partDef != None:
            return partDef.partBundleNP
        

    
    def getPartBundle(self, partName, lodName = 'lodRoot'):
        partBundleDict = self._Actor__partBundleDict.get(lodName)
        if not partBundleDict:
            Actor.notify.warning('no lod named: %s' % lodName)
            return None
        
        subpartDef = self._Actor__subpartDict.get(partName, Actor.SubpartDef(partName))
        partDef = partBundleDict.get(subpartDef.truePartName)
        if partDef != None:
            return partDef.getBundle()
        

    
    def removePart(self, partName, lodName = 'lodRoot'):
        partBundleDict = self._Actor__partBundleDict.get(lodName)
        if not partBundleDict:
            Actor.notify.warning('no lod named: %s' % lodName)
            return None
        
        if partBundleDict.has_key(partName):
            partBundleDict[partName].partBundleNP.removeNode()
            del partBundleDict[partName]
        
        if self.mergeLODBundles:
            lodName = 'common'
        
        partDict = self._Actor__animControlDict.get(lodName)
        if not partDict:
            Actor.notify.warning('no lod named: %s' % lodName)
            return None
        
        if partDict.has_key(partName):
            del partDict[partName]
        

    
    def hidePart(self, partName, lodName = 'lodRoot'):
        partBundleDict = self._Actor__partBundleDict.get(lodName)
        if not partBundleDict:
            Actor.notify.warning('no lod named: %s' % lodName)
            return None
        
        partDef = partBundleDict.get(partName)
        if partDef:
            partDef.partBundleNP.hide()
        else:
            Actor.notify.warning('no part named %s!' % partName)

    
    def showPart(self, partName, lodName = 'lodRoot'):
        partBundleDict = self._Actor__partBundleDict.get(lodName)
        if not partBundleDict:
            Actor.notify.warning('no lod named: %s' % lodName)
            return None
        
        partDef = partBundleDict.get(partName)
        if partDef:
            partDef.partBundleNP.show()
        else:
            Actor.notify.warning('no part named %s!' % partName)

    
    def showAllParts(self, partName, lodName = 'lodRoot'):
        partBundleDict = self._Actor__partBundleDict.get(lodName)
        if not partBundleDict:
            Actor.notify.warning('no lod named: %s' % lodName)
            return None
        
        partDef = partBundleDict.get(partName)
        if partDef:
            partDef.partBundleNP.show()
            partDef.partBundleNP.getChildren().show()
        else:
            Actor.notify.warning('no part named %s!' % partName)

    
    def exposeJoint(self, node, partName, jointName, lodName = 'lodRoot', localTransform = 0):
        partBundleDict = self._Actor__partBundleDict.get(lodName)
        if not partBundleDict:
            Actor.notify.warning('no lod named: %s' % lodName)
            return None
        
        subpartDef = self._Actor__subpartDict.get(partName, Actor.SubpartDef(partName))
        partDef = partBundleDict.get(subpartDef.truePartName)
        if partDef:
            bundle = partDef.getBundle()
        else:
            Actor.notify.warning('no part named %s!' % partName)
            return None
        joint = bundle.findChild(jointName)
        if node == None:
            node = self.attachNewNode(jointName)
        
        if joint:
            if localTransform:
                joint.addLocalTransform(node.node())
            else:
                joint.addNetTransform(node.node())
        else:
            Actor.notify.warning('no joint named %s!' % jointName)
        return node

    
    def stopJoint(self, partName, jointName, lodName = 'lodRoot'):
        partBundleDict = self._Actor__partBundleDict.get(lodName)
        if not partBundleDict:
            Actor.notify.warning('no lod named: %s' % lodName)
            return None
        
        subpartDef = self._Actor__subpartDict.get(partName, Actor.SubpartDef(partName))
        partDef = partBundleDict.get(subpartDef.truePartName)
        if partDef:
            bundle = partDef.getBundle()
        else:
            Actor.notify.warning('no part named %s!' % partName)
            return None
        joint = bundle.findChild(jointName)
        if joint:
            joint.clearNetTransforms()
            joint.clearLocalTransforms()
        else:
            Actor.notify.warning('no joint named %s!' % jointName)

    
    def getJoints(self, partName = None, jointName = '*', lodName = None):
        joints = []
        pattern = GlobPattern(jointName)
        if lodName == None and self.mergeLODBundles:
            partBundleDicts = [
                self._Actor__commonBundleHandles]
        elif lodName == None:
            partBundleDicts = self._Actor__partBundleDict.values()
        else:
            partBundleDict = self._Actor__partBundleDict.get(lodName)
            if not partBundleDict:
                Actor.notify.warning("couldn't find lod: %s" % lodName)
                return []
            
            partBundleDicts = [
                partBundleDict]
        for partBundleDict in partBundleDicts:
            parts = []
            if partName:
                subpartDef = self._Actor__subpartDict.get(partName, None)
                if not subpartDef:
                    subset = None
                    partDef = partBundleDict.get(partName)
                else:
                    subset = subpartDef.subset
                    partDef = partBundleDict.get(subpartDef.truePartName)
                if not partDef:
                    Actor.notify.warning('no part named %s!' % partName)
                    return []
                
                parts = [
                    partDef]
            else:
                subset = None
                parts = partBundleDict.values()
            for partData in parts:
                partBundle = partData.getBundle()
                if not pattern.hasGlobCharacters() and not subset:
                    joint = partBundle.findChild(jointName)
                    if joint:
                        joints.append(joint)
                    
                isIncluded = True
                if subset:
                    isIncluded = subset.isIncludeEmpty()
                
                self._Actor__getPartJoints(joints, pattern, partBundle, subset, isIncluded)
            
        
        return joints

    
    def getOverlappingJoints(self, partNameA, partNameB, jointName = '*', lodName = None):
        jointsA = set(self.getJoints(partName = partNameA, jointName = jointName, lodName = lodName))
        jointsB = set(self.getJoints(partName = partNameB, jointName = jointName, lodName = lodName))
        return jointsA & jointsB

    
    def _Actor__getPartJoints(self, joints, pattern, partNode, subset, isIncluded):
        name = partNode.getName()
        if subset:
            if subset.matchesInclude(name):
                isIncluded = True
            elif subset.matchesExclude(name):
                isIncluded = False
            
        
        if isIncluded and pattern.matches(name) and isinstance(partNode, MovingPartBase):
            joints.append(partNode)
        
        for child in partNode.getChildren():
            self._Actor__getPartJoints(joints, pattern, child, subset, isIncluded)
        

    
    def getJointTransform(self, partName, jointName, lodName = 'lodRoot'):
        partBundleDict = self._Actor__partBundleDict.get(lodName)
        if not partBundleDict:
            Actor.notify.warning('no lod named: %s' % lodName)
            return None
        
        subpartDef = self._Actor__subpartDict.get(partName, Actor.SubpartDef(partName))
        partDef = partBundleDict.get(subpartDef.truePartName)
        if partDef:
            bundle = partDef.getBundle()
        else:
            Actor.notify.warning('no part named %s!' % partName)
            return None
        joint = bundle.findChild(jointName)
        if joint == None:
            Actor.notify.warning('no joint named %s!' % jointName)
            return None
        
        return joint.getDefaultValue()

    
    def controlJoint(self, node, partName, jointName, lodName = 'lodRoot'):
        subpartDef = self._Actor__subpartDict.get(partName, Actor.SubpartDef(partName))
        trueName = subpartDef.truePartName
        anyGood = False
        for bundleDict in self._Actor__partBundleDict.values():
            bundle = bundleDict[trueName].getBundle()
            if node == None:
                node = self.attachNewNode(ModelNode(jointName))
                joint = bundle.findChild(jointName)
                if joint and isinstance(joint, MovingPartMatrix):
                    node.setMat(joint.getDefaultValue())
                
            
            if bundle.controlJoint(jointName, node.node()):
                anyGood = True
                continue
        
        if not anyGood:
            self.notify.warning('Cannot control joint %s' % jointName)
        
        return node

    
    def freezeJoint(self, partName, jointName, transform = None, pos = Vec3(0, 0, 0), hpr = Vec3(0, 0, 0), scale = Vec3(1, 1, 1)):
        if transform == None:
            transform = TransformState.makePosHprScale(pos, hpr, scale)
        
        subpartDef = self._Actor__subpartDict.get(partName, Actor.SubpartDef(partName))
        trueName = subpartDef.truePartName
        anyGood = False
        for bundleDict in self._Actor__partBundleDict.values():
            if bundleDict[trueName].getBundle().freezeJoint(jointName, transform):
                anyGood = True
                continue
        
        if not anyGood:
            self.notify.warning('Cannot freeze joint %s' % jointName)
        

    
    def releaseJoint(self, partName, jointName):
        subpartDef = self._Actor__subpartDict.get(partName, Actor.SubpartDef(partName))
        trueName = subpartDef.truePartName
        for bundleDict in self._Actor__partBundleDict.values():
            bundleDict[trueName].getBundle().releaseJoint(jointName)
        

    
    def instance(self, path, partName, jointName, lodName = 'lodRoot'):
        partBundleDict = self._Actor__partBundleDict.get(lodName)
        if partBundleDict:
            subpartDef = self._Actor__subpartDict.get(partName, Actor.SubpartDef(partName))
            partDef = partBundleDict.get(subpartDef.truePartName)
            if partDef:
                joint = partDef.partBundleNP.find('**/' + jointName)
                if joint.isEmpty():
                    Actor.notify.warning('%s not found!' % jointName)
                else:
                    return path.instanceTo(joint)
            else:
                Actor.notify.warning('no part named %s!' % partName)
        else:
            Actor.notify.warning('no lod named %s!' % lodName)

    
    def attach(self, partName, anotherPartName, jointName, lodName = 'lodRoot'):
        partBundleDict = self._Actor__partBundleDict.get(lodName)
        if partBundleDict:
            subpartDef = self._Actor__subpartDict.get(partName, Actor.SubpartDef(partName))
            partDef = partBundleDict.get(subpartDef.truePartName)
            if partDef:
                anotherPartDef = partBundleDict.get(anotherPartName)
                if anotherPartDef:
                    joint = anotherPartDef.partBundleNP.find('**/' + jointName)
                    if joint.isEmpty():
                        Actor.notify.warning('%s not found!' % jointName)
                    else:
                        partDef.partBundleNP.reparentTo(joint)
                else:
                    Actor.notify.warning('no part named %s!' % anotherPartName)
            else:
                Actor.notify.warning('no part named %s!' % partName)
        else:
            Actor.notify.warning('no lod named %s!' % lodName)

    
    def drawInFront(self, frontPartName, backPartName, mode, root = None, lodName = None):
        if lodName != None:
            lodRoot = self._Actor__LODNode.find(str(lodName))
            if root == None:
                root = lodRoot
            else:
                root = lodRoot.find('**/' + root)
        elif root == None:
            root = self
        
        frontParts = root.findAllMatches('**/' + frontPartName)
        if mode > 0:
            numFrontParts = frontParts.getNumPaths()
            for partNum in range(0, numFrontParts):
                frontParts[partNum].setBin('fixed', mode)
            
            return None
        
        if mode == -2:
            numFrontParts = frontParts.getNumPaths()
            for partNum in range(0, numFrontParts):
                frontParts[partNum].setDepthWrite(0)
                frontParts[partNum].setDepthTest(0)
            
        
        backPart = root.find('**/' + backPartName)
        if backPart.isEmpty():
            Actor.notify.warning('no part named %s!' % backPartName)
            return None
        
        if mode == -3:
            backPart.node().setEffect(DecalEffect.make())
        else:
            backPart.reparentTo(backPart.getParent(), -1)
        frontParts.reparentTo(backPart)

    
    def fixBounds(self, partName = None):
        if partName == None:
            for lodData in self._Actor__partBundleDict.values():
                for partData in lodData.values():
                    char = partData.partBundleNP
                    char.node().update()
                    geomNodes = char.findAllMatches('**/+GeomNode')
                    numGeomNodes = geomNodes.getNumPaths()
                    for nodeNum in xrange(numGeomNodes):
                        thisGeomNode = geomNodes.getPath(nodeNum)
                        numGeoms = thisGeomNode.node().getNumGeoms()
                        for geomNum in xrange(numGeoms):
                            thisGeom = thisGeomNode.node().getGeom(geomNum)
                            thisGeom.markBoundsStale()
                        
                        thisGeomNode.node().markInternalBoundsStale()
                    
                
            
        else:
            for lodData in self._Actor__partBundleDict.values():
                partData = lodData.get(partName)
                if partData:
                    char = partData.partBundleNP
                    char.node().update()
                    geomNodes = char.findAllMatches('**/+GeomNode')
                    numGeomNodes = geomNodes.getNumPaths()
                    for nodeNum in xrange(numGeomNodes):
                        thisGeomNode = geomNodes.getPath(nodeNum)
                        numGeoms = thisGeomNode.node().getNumGeoms()
                        for geomNum in xrange(numGeoms):
                            thisGeom = thisGeomNode.node().getGeom(geomNum)
                            thisGeom.markBoundsStale()
                        
                        thisGeomNode.node().markInternalBoundsStale()
                    
            

    
    def fixBounds_old(self, part = None):
        if part == None:
            part = self
        
        charNodes = part.findAllMatches('**/+Character')
        numCharNodes = charNodes.getNumPaths()
        for charNum in range(0, numCharNodes):
            charNodes.getPath(charNum).node().update()
        
        geomNodes = part.findAllMatches('**/+GeomNode')
        numGeomNodes = geomNodes.getNumPaths()
        for nodeNum in range(0, numGeomNodes):
            thisGeomNode = geomNodes.getPath(nodeNum)
            numGeoms = thisGeomNode.node().getNumGeoms()
            for geomNum in range(0, numGeoms):
                thisGeom = thisGeomNode.node().getGeom(geomNum)
                thisGeom.markBoundsStale()
            
            thisGeomNode.node().markInternalBoundsStale()
        

    
    def showAllBounds(self):
        geomNodes = self._Actor__geomNode.findAllMatches('**/+GeomNode')
        numGeomNodes = geomNodes.getNumPaths()
        for nodeNum in range(0, numGeomNodes):
            geomNodes.getPath(nodeNum).showBounds()
        

    
    def hideAllBounds(self):
        geomNodes = self._Actor__geomNode.findAllMatches('**/+GeomNode')
        numGeomNodes = geomNodes.getNumPaths()
        for nodeNum in range(0, numGeomNodes):
            geomNodes.getPath(nodeNum).hideBounds()
        

    
    def animPanel(self):
        TkGlobal = TkGlobal
        import direct.showbase
        AnimPanel = AnimPanel
        import direct.tkpanels
        return AnimPanel.AnimPanel(self)

    
    def stop(self, animName = None, partName = None):
        for control in self.getAnimControls(animName, partName):
            control.stop()
        

    
    def play(self, animName, partName = None, fromFrame = None, toFrame = None):
        if fromFrame == None:
            for control in self.getAnimControls(animName, partName):
                control.play()
            
        else:
            for control in self.getAnimControls(animName, partName):
                if toFrame == None:
                    control.play(fromFrame, control.getNumFrames() - 1)
                    continue
                control.play(fromFrame, toFrame)
            

    
    def loop(self, animName, restart = 1, partName = None, fromFrame = None, toFrame = None):
        if fromFrame == None:
            for control in self.getAnimControls(animName, partName):
                control.loop(restart)
            
        else:
            for control in self.getAnimControls(animName, partName):
                if toFrame == None:
                    control.loop(restart, fromFrame, control.getNumFrames() - 1)
                    continue
                control.loop(restart, fromFrame, toFrame)
            

    
    def pingpong(self, animName, restart = 1, partName = None, fromFrame = None, toFrame = None):
        if fromFrame == None:
            fromFrame = 0
        
        for control in self.getAnimControls(animName, partName):
            if toFrame == None:
                control.pingpong(restart, fromFrame, control.getNumFrames() - 1)
                continue
            control.pingpong(restart, fromFrame, toFrame)
        

    
    def pose(self, animName, frame, partName = None, lodName = None):
        for control in self.getAnimControls(animName, partName, lodName):
            control.pose(frame)
        

    
    def setBlend(self, animBlend = None, frameBlend = None, blendType = None, partName = None):
        for bundle in self.getPartBundles(partName = partName):
            if blendType != None:
                bundle.setBlendType(blendType)
            
            if animBlend != None:
                bundle.setAnimBlendFlag(animBlend)
            
            if frameBlend != None:
                bundle.setFrameBlendFlag(frameBlend)
                continue
        

    
    def enableBlend(self, blendType = PartBundle.BTNormalizedLinear, partName = None):
        self.setBlend(animBlend = True, blendType = blendType, partName = partName)

    
    def disableBlend(self, partName = None):
        self.setBlend(animBlend = False, partName = partName)

    
    def setControlEffect(self, animName, effect, partName = None, lodName = None):
        for control in self.getAnimControls(animName, partName, lodName):
            control.getPart().setControlEffect(control, effect)
        

    
    def getAnimFilename(self, animName, partName = 'modelRoot'):
        if self.mergeLODBundles:
            lodName = 'common'
        elif self.switches:
            lodName = str(self.switches.keys()[0])
        else:
            lodName = 'lodRoot'
        
        try:
            return self._Actor__animControlDict[lodName][partName][animName].filename
        except:
            return None


    
    def getAnimControl(self, animName, partName = None, lodName = None, allowAsyncBind = True):
        if not partName:
            partName = 'modelRoot'
        
        if self.mergeLODBundles:
            lodName = 'common'
        elif not lodName:
            if self.switches:
                lodName = str(self.switches.keys()[0])
            else:
                lodName = 'lodRoot'
        
        partDict = self._Actor__animControlDict.get(lodName)
        animDict = partDict.get(partName)
        if animDict == None:
            Actor.notify.warning("couldn't find part: %s" % partName)
        else:
            anim = animDict.get(animName)
            if anim == None:
                pass
            1
            if not anim.animControl:
                self._Actor__bindAnimToPart(animName, partName, lodName, allowAsyncBind = allowAsyncBind)
            elif not allowAsyncBind:
                anim.animControl.waitPending()
            
            return anim.animControl

    
    def getAnimControls(self, animName = None, partName = None, lodName = None, allowAsyncBind = True):
        if partName == None and self._Actor__subpartsComplete:
            partName = self._Actor__subpartDict.keys()
        
        controls = []
        if lodName == None or self.mergeLODBundles:
            animControlDictItems = self._Actor__animControlDict.items()
        else:
            partDict = self._Actor__animControlDict.get(lodName)
            if partDict == None:
                Actor.notify.warning("couldn't find lod: %s" % lodName)
                animControlDictItems = []
            else:
                animControlDictItems = [
                    (lodName, partDict)]
        for (lodName, partDict) in animControlDictItems:
            if partName == None:
                animDictItems = []
                for (thisPart, animDict) in partDict.items():
                    if not self._Actor__subpartDict.has_key(thisPart):
                        animDictItems.append((thisPart, animDict))
                        continue
                
            elif isinstance(partName, types.StringTypes):
                partNameList = [
                    partName]
            else:
                partNameList = partName
            animDictItems = []
            for pName in partNameList:
                animDict = partDict.get(pName)
                if animDict == None:
                    subpartDef = self._Actor__subpartDict.get(pName)
                    if subpartDef:
                        animDict = { }
                        partDict[pName] = animDict
                    
                
                if animDict == None:
                    Actor.notify.warning("couldn't find part: %s" % pName)
                    continue
                animDictItems.append((pName, animDict))
            
            if animName is None:
                for (thisPart, animDict) in animDictItems:
                    for anim in animDict.values():
                        if anim.animControl and anim.animControl.isPlaying():
                            controls.append(anim.animControl)
                            continue
                    
                
            if isinstance(animName, types.StringTypes):
                animNameList = [
                    animName]
            else:
                animNameList = animName
            for (thisPart, animDict) in animDictItems:
                names = animNameList
                if animNameList is True:
                    names = animDict.keys()
                
                for animName in names:
                    anim = animDict.get(animName)
                    if anim == None and partName != None:
                        for pName in partNameList:
                            subpartDef = self._Actor__subpartDict.get(pName)
                            if subpartDef:
                                truePartName = subpartDef.truePartName
                                anim = partDict[truePartName].get(animName)
                                if anim:
                                    anim = anim.makeCopy()
                                    animDict[animName] = anim
                                
                        
                    
                    if anim == None:
                        continue
                    animControl = anim.animControl
                    if animControl == None:
                        animControl = self._Actor__bindAnimToPart(animName, thisPart, lodName, allowAsyncBind = allowAsyncBind)
                    elif not allowAsyncBind:
                        animControl.waitPending()
                    
                    if animControl:
                        controls.append(animControl)
                        continue
                
            
        
        return controls

    
    def loadModel(self, modelPath, partName = 'modelRoot', lodName = 'lodRoot', copy = True, okMissing = None, autoBindAnims = True):
        if isinstance(modelPath, NodePath):
            if copy:
                model = modelPath.copyTo(NodePath())
            else:
                model = modelPath
        else:
            loaderOptions = self.modelLoaderOptions
            if not copy:
                loaderOptions = LoaderOptions(loaderOptions)
                loaderOptions.setFlags(loaderOptions.getFlags() & ~(LoaderOptions.LFNoRamCache))
            
            model = loader.loadModel(modelPath, loaderOptions = loaderOptions, okMissing = okMissing)
        if model == None:
            raise StandardError, 'Could not load Actor model %s' % modelPath
        
        if model.node().isOfType(Character.getClassType()):
            bundleNP = model
        else:
            bundleNP = model.find('**/+Character')
        if bundleNP.isEmpty():
            Actor.notify.warning('%s is not a character!' % modelPath)
            model.reparentTo(self._Actor__geomNode)
        elif autoBindAnims:
            acc = AnimControlCollection()
            autoBind(model.node(), acc, -1)
            numAnims = acc.getNumAnims()
        else:
            numAnims = 0
        if lodName != 'lodRoot':
            bundleNP.reparentTo(self._Actor__LODNode.find(str(lodName)))
        else:
            bundleNP.reparentTo(self._Actor__geomNode)
        self._Actor__prepareBundle(bundleNP, model.node(), partName, lodName)
        bundleNP.node().setName('%s%s' % (Actor.partPrefix, partName))
        if numAnims != 0:
            Actor.notify.info('model contains %s animations.' % numAnims)
            if self.mergeLODBundles:
                lodName = 'common'
            
            self._Actor__animControlDict.setdefault(lodName, { })
            self._Actor__animControlDict[lodName].setdefault(partName, { })
            for i in range(numAnims):
                animControl = acc.getAnim(i)
                animName = acc.getAnimName(i)
                animDef = Actor.AnimDef()
                animDef.animControl = animControl
                self._Actor__animControlDict[lodName][partName][animName] = animDef
            
        

    
    def _Actor__prepareBundle(self, bundleNP, partModel, partName = 'modelRoot', lodName = 'lodRoot'):
        if not self.gotName:
            self.node().setName(bundleNP.node().getName())
            self.gotName = 1
        
        bundleDict = self._Actor__partBundleDict.get(lodName, None)
        if bundleDict == None:
            bundleDict = { }
            self._Actor__partBundleDict[lodName] = bundleDict
            self._Actor__updateSortedLODNames()
        
        node = bundleNP.node()
        bundleHandle = node.getBundleHandle(0)
        if self.mergeLODBundles:
            loadedBundleHandle = self._Actor__commonBundleHandles.get(partName, None)
            if loadedBundleHandle:
                node.mergeBundles(bundleHandle, loadedBundleHandle)
                bundleHandle = loadedBundleHandle
            else:
                self._Actor__commonBundleHandles[partName] = bundleHandle
        
        bundleDict[partName] = Actor.PartDef(bundleNP, bundleHandle, partModel)

    
    def makeSubpart(self, partName, includeJoints, excludeJoints = [], parent = 'modelRoot', overlapping = False):
        subpartDef = self._Actor__subpartDict.get(parent, Actor.SubpartDef(''))
        subset = PartSubset(subpartDef.subset)
        for name in includeJoints:
            subset.addIncludeJoint(GlobPattern(name))
        
        for name in excludeJoints:
            subset.addExcludeJoint(GlobPattern(name))
        
        self._Actor__subpartDict[partName] = Actor.SubpartDef(parent, subset)
        if __dev__ and not overlapping and self.validateSubparts.getValue():
            for (otherPartName, otherPartDef) in self._Actor__subpartDict.items():
                if otherPartName != partName and otherPartDef.truePartName == parent:
                    joints = self.getOverlappingJoints(partName, otherPartName)
                    if joints:
                        raise StandardError, 'Overlapping joints: %s and %s' % (partName, otherPartName)
                    
            
        

    
    def setSubpartsComplete(self, flag):
        self._Actor__subpartsComplete = flag
        if __dev__ and self._Actor__subpartsComplete and self.validateSubparts.getValue():
            if self._Actor__subpartDict:
                self.verifySubpartsComplete()
            
        

    
    def getSubpartsComplete(self):
        return self._Actor__subpartsComplete

    
    def verifySubpartsComplete(self, partName = None, lodName = None):
        if partName:
            partNames = [
                partName]
        elif lodName:
            partNames = self._Actor__partBundleDict[lodName].keys()
        else:
            partNames = self._Actor__partBundleDict.values()[0].keys()
        for partName in partNames:
            subJoints = set()
            for (subPartName, subPartDef) in self._Actor__subpartDict.items():
                if subPartName != partName and subPartDef.truePartName == partName:
                    subJoints |= set(self.getJoints(partName = subPartName, lodName = lodName))
                    continue
            
            allJoints = set(self.getJoints(partName = partName, lodName = lodName))
            diff = allJoints.difference(subJoints)
            if diff:
                self.notify.warning('Uncovered joints: %s' % list(diff))
                continue
        

    
    def loadAnims(self, anims, partName = 'modelRoot', lodName = 'lodRoot'):
        reload = True
        if self.mergeLODBundles:
            lodNames = [
                'common']
        elif lodName == 'all':
            reload = False
            lodNames = self.switches.keys()
            lodNames.sort()
            for i in range(0, len(lodNames)):
                lodNames[i] = str(lodNames[i])
            
        else:
            lodNames = [
                lodName]
        firstLoad = True
        if not reload:
            
            try:
                self._Actor__animControlDict[lodNames[0]][partName]
                firstLoad = False

        
        for lName in lodNames:
            if firstLoad:
                self._Actor__animControlDict.setdefault(lName, { })
                self._Actor__animControlDict[lName].setdefault(partName, { })
                continue
        
        for (animName, filename) in anims.items():
            for lName in lodNames:
                if firstLoad:
                    self._Actor__animControlDict[lName][partName][animName] = Actor.AnimDef()
                
                if isinstance(filename, NodePath):
                    if filename.node().isOfType(AnimBundleNode.getClassType()):
                        animBundleNP = filename
                    else:
                        animBundleNP = filename.find('**/+AnimBundleNode')
                    self._Actor__animControlDict[lName][partName][animName].animBundle = animBundleNP.node().getBundle()
                    continue
                self._Actor__animControlDict[lName][partName][animName].filename = filename
            
        

    
    def initAnimsOnAllLODs(self, partNames):
        if self.mergeLODBundles:
            lodNames = [
                'common']
        else:
            lodNames = self._Actor__partBundleDict.keys()
        for lod in lodNames:
            for part in partNames:
                self._Actor__animControlDict.setdefault(lod, { })
                self._Actor__animControlDict[lod].setdefault(part, { })
            
        

    
    def loadAnimsOnAllLODs(self, anims, partName = 'modelRoot'):
        if self.mergeLODBundles:
            lodNames = [
                'common']
        else:
            lodNames = self._Actor__partBundleDict.keys()
        for (animName, filename) in anims.items():
            for lod in lodNames:
                self._Actor__animControlDict[lod][partName][animName] = Actor.AnimDef(filename)
            
        

    
    def postFlatten(self):
        if self.mergeLODBundles:
            self._Actor__commonBundleHandles = { }
            for (lodName, bundleDict) in self._Actor__partBundleDict.items():
                for (partName, partDef) in bundleDict.items():
                    loadedBundleHandle = self._Actor__commonBundleHandles.get(partName, None)
                    node = partDef.partBundleNP.node()
                    if loadedBundleHandle:
                        node.mergeBundles(partDef.partBundleHandle, loadedBundleHandle)
                        partDef.partBundleHandle = loadedBundleHandle
                        continue
                    self._Actor__commonBundleHandles[partName] = partDef.partBundleHandle
                
            
        
        self.unloadAnims()

    
    def unloadAnims(self, anims = None, partName = None, lodName = None):
        if lodName == None or self.mergeLODBundles:
            lodNames = self._Actor__animControlDict.keys()
        else:
            lodNames = [
                lodName]
        if partName == None:
            if len(lodNames) > 0:
                partNames = self._Actor__animControlDict[lodNames[0]].keys()
            else:
                partNames = []
        else:
            partNames = [
                partName]
        if anims == None:
            for lodName in lodNames:
                for partName in partNames:
                    for animDef in self._Actor__animControlDict[lodName][partName].values():
                        if animDef.animControl != None:
                            animDef.animControl.getPart().clearControlEffects()
                            animDef.animControl = None
                            continue
                    
                
            
        else:
            for lodName in lodNames:
                for partName in partNames:
                    for anim in anims:
                        animDef = self._Actor__animControlDict[lodName][partName].get(anim)
                        if animDef and animDef.animControl != None:
                            animDef.animControl.getPart().clearControlEffects()
                            animDef.animControl = None
                            continue
                    
                
            

    
    def bindAnim(self, animName, partName = None, lodName = None, allowAsyncBind = False):
        self.getAnimControls(animName = animName, partName = partName, lodName = lodName, allowAsyncBind = allowAsyncBind)

    
    def bindAllAnims(self, allowAsyncBind = False):
        self.getAnimControls(animName = True, allowAsyncBind = allowAsyncBind)

    
    def waitPending(self, partName = None):
        for bundle in self.getPartBundles(partName = partName):
            bundle.waitPending()
        

    
    def _Actor__bindAnimToPart(self, animName, partName, lodName, allowAsyncBind = True):
        subpartDef = self._Actor__subpartDict.get(partName, Actor.SubpartDef(partName))
        partDict = self._Actor__animControlDict[lodName]
        animDict = partDict.get(partName)
        if animDict == None:
            animDict = { }
            partDict[partName] = animDict
        
        anim = animDict.get(animName)
        if anim == None:
            anim = partDict[subpartDef.truePartName].get(animName)
            anim = anim.makeCopy()
            animDict[animName] = anim
        
        if anim == None:
            Actor.notify.error('actor has no animation %s', animName)
        
        if anim.animControl:
            return anim.animControl
        
        if self.mergeLODBundles:
            bundle = self._Actor__commonBundleHandles[subpartDef.truePartName].getBundle()
        else:
            bundle = self._Actor__partBundleDict[lodName][subpartDef.truePartName].getBundle()
        if anim.animBundle:
            animControl = bundle.bindAnim(anim.animBundle, -1, subpartDef.subset)
        elif allowAsyncBind:
            pass
        animControl = bundle.loadBindAnim(loader.loader, Filename(anim.filename), -1, subpartDef.subset, self.allowAsyncBind)
        if not animControl:
            return None
        
        anim.animControl = animControl
        return animControl

    
    def _Actor__copyPartBundles(self, other):
        for lodName in other._Actor__partBundleDict.keys():
            if lodName == 'lodRoot':
                partLod = self
            else:
                partLod = self._Actor__LODNode.find(str(lodName))
            if partLod.isEmpty():
                Actor.notify.warning('no lod named: %s' % lodName)
                return None
            
            for (partName, partDef) in other._Actor__partBundleDict[lodName].items():
                bundleNP = partLod.find('**/%s%s' % (Actor.partPrefix, partName))
                if bundleNP != None:
                    self._Actor__prepareBundle(bundleNP, partDef.partModel, partName, lodName)
                    continue
                Actor.notify.error('lod: %s has no matching part: %s' % (lodName, partName))
            
        

    
    def _Actor__copySubpartDict(self, other):
        self._Actor__subpartDict = { }
        for (partName, subpartDef) in other._Actor__subpartDict.items():
            subpartDefCopy = subpartDef
            if subpartDef:
                subpartDef = subpartDef.makeCopy()
            
            self._Actor__subpartDict[partName] = subpartDef
        

    
    def _Actor__copyAnimControls(self, other):
        for lodName in other._Actor__animControlDict.keys():
            self._Actor__animControlDict[lodName] = { }
            for partName in other._Actor__animControlDict[lodName].keys():
                self._Actor__animControlDict[lodName][partName] = { }
                for animName in other._Actor__animControlDict[lodName][partName].keys():
                    anim = other._Actor__animControlDict[lodName][partName][animName]
                    anim = anim.makeCopy()
                    self._Actor__animControlDict[lodName][partName][animName] = anim
                
            
        

    
    def actorInterval(self, *args, **kw):
        ActorInterval = ActorInterval
        import direct.interval
        return ActorInterval.ActorInterval(self, *args, **args)

    
    def getAnimBlends(self, animName = None, partName = None, lodName = None):
        result = []
        if animName is None:
            animNames = self.getAnimNames()
        else:
            animNames = [
                animName]
        if lodName is None:
            lodNames = self.getLODNames()
            if self.mergeLODBundles:
                lodNames = lodNames[:1]
            
        else:
            lodNames = [
                lodName]
        if partName == None and self._Actor__subpartsComplete:
            partNames = self._Actor__subpartDict.keys()
        else:
            partNames = [
                partName]
        for lodName in lodNames:
            animList = []
            for animName in animNames:
                blendList = []
                for partName in partNames:
                    control = self.getAnimControl(animName, partName, lodName)
                    if control:
                        part = control.getPart()
                        effect = part.getControlEffect(control)
                        if effect > 0.0:
                            blendList.append((partName, effect))
                        
                    effect > 0.0
                
                if blendList:
                    animList.append((animName, blendList))
                    continue
            
            if animList:
                result.append((lodName, animList))
                continue
        
        return result

    
    def printAnimBlends(self, animName = None, partName = None, lodName = None):
        for (lodName, animList) in self.getAnimBlends(animName, partName, lodName):
            print 'LOD %s:' % lodName
            for (animName, blendList) in animList:
                list = []
                for (partName, effect) in blendList:
                    list.append('%s:%.3f' % (partName, effect))
                
                print '  %s: %s' % (animName, ', '.join(list))
            
        

    
    def osdAnimBlends(self, animName = None, partName = None, lodName = None):
        if not onScreenDebug.enabled:
            return None
        
        if animName is None:
            animNames = self.getAnimNames()
        else:
            animNames = [
                animName]
        for animName in animNames:
            if animName is 'nothing':
                continue
            
            thisAnim = ''
            totalEffect = 0.0
            controls = self.getAnimControls(animName, partName, lodName)
            for control in controls:
                part = control.getPart()
                name = part.getName()
                effect = part.getControlEffect(control)
                if effect > 0.0:
                    totalEffect += effect
                    thisAnim += '%s:%.3f, ' % (name, effect)
                    continue
            
            thisAnim += '\n'
            for control in controls:
                part = control.getPart()
                name = part.getName()
                rate = control.getPlayRate()
                thisAnim += '%s:%.1f, ' % (name, rate)
            
            itemName = 'anim %s' % animName
            if totalEffect > 0.0:
                onScreenDebug.add(itemName, thisAnim)
                continue
            if onScreenDebug.has(itemName):
                onScreenDebug.remove(itemName)
                continue
        

    
    def faceAwayFromViewer(self):
        self.getGeomNode().setH(180)

    
    def faceTowardsViewer(self):
        self.getGeomNode().setH(0)

    
    def renamePartBundles(self, partName, newBundleName):
        subpartDef = self._Actor__subpartDict.get(partName, Actor.SubpartDef(partName))
        for partBundleDict in self._Actor__partBundleDict.values():
            partDef = partBundleDict.get(subpartDef.truePartName)
            partDef.getBundle().setName(newBundleName)
        



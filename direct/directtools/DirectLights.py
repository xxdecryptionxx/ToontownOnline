# File: d (Python 2.4)

from pandac.PandaModules import *
from string import lower

class DirectLight(NodePath):
    
    def __init__(self, light, parent):
        NodePath.__init__(self)
        self.light = light
        self.assign(parent.attachNewNode(self.light))

    
    def getName(self):
        return self.light.getName()

    
    def getLight(self):
        return self.light



class DirectLights(NodePath):
    
    def __init__(self, parent = render):
        NodePath.__init__(self)
        self.assign(parent.attachNewNode('DIRECT Lights'))
        self.lightDict = { }
        self.ambientCount = 0
        self.directionalCount = 0
        self.pointCount = 0
        self.spotCount = 0

    
    def __getitem__(self, name):
        return self.lightDict.get(name, None)

    
    def __len__(self):
        return len(self.lightDict)

    
    def delete(self, light):
        del self.lightDict[light.getName()]
        self.setOff(light)
        light.removeNode()

    
    def deleteAll(self):
        for light in self:
            self.delete(light)
        

    
    def asList(self):
        return map(lambda n, s = self: s[n], self.getNameList())

    
    def getNameList(self):
        nameList = map(lambda x: x.getName(), self.lightDict.values())
        nameList.sort()
        return nameList

    
    def create(self, type):
        type = type.lower()
        if type == 'ambient':
            self.ambientCount += 1
            light = AmbientLight('ambient-' + repr(self.ambientCount))
            light.setColor(VBase4(0.29999999999999999, 0.29999999999999999, 0.29999999999999999, 1))
        elif type == 'directional':
            self.directionalCount += 1
            light = DirectionalLight('directional-' + repr(self.directionalCount))
            light.setColor(VBase4(1))
        elif type == 'point':
            self.pointCount += 1
            light = PointLight('point-' + repr(self.pointCount))
            light.setColor(VBase4(1))
        elif type == 'spot':
            self.spotCount += 1
            light = Spotlight('spot-' + repr(self.spotCount))
            light.setColor(VBase4(1))
            light.setLens(PerspectiveLens())
        else:
            print 'Invalid light type'
            return None
        directLight = DirectLight(light, self)
        self.lightDict[directLight.getName()] = directLight
        self.setOn(directLight)
        messenger.send('DIRECT_addLight', [
            directLight])
        return directLight

    
    def createDefaultLights(self):
        self.create('ambient')
        self.create('directional')

    
    def allOn(self):
        for light in self.lightDict.values():
            self.setOn(light)
        
        render.setMaterial(Material())

    
    def allOff(self):
        for light in self.lightDict.values():
            self.setOff(light)
        

    
    def toggle(self):
        if render.node().hasAttrib(LightAttrib.getClassType()):
            self.allOff()
        else:
            self.allOn()

    
    def setOn(self, directLight):
        render.setLight(directLight)

    
    def setOff(self, directLight):
        render.clearLight(directLight)



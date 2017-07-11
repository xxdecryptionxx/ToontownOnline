# File: d (Python 2.4)

from pandac.PandaModules import *
import types

class Rope(NodePath):
    showRope = base.config.GetBool('show-rope', 1)
    
    def __init__(self, name = 'Rope'):
        self.ropeNode = RopeNode(name)
        self.curve = NurbsCurveEvaluator()
        self.ropeNode.setCurve(self.curve)
        NodePath.__init__(self, self.ropeNode)
        self.name = name

    
    def setup(self, order, verts, knots = None):
        self.order = order
        self.verts = verts
        self.knots = knots
        self.recompute()

    
    def recompute(self):
        if not self.showRope:
            return None
        
        numVerts = len(self.verts)
        self.curve.reset(numVerts)
        self.curve.setOrder(self.order)
        defaultNodePath = None
        defaultPoint = (0, 0, 0)
        defaultColor = (1, 1, 1, 1)
        defaultThickness = 1
        useVertexColor = self.ropeNode.getUseVertexColor()
        useVertexThickness = self.ropeNode.getUseVertexThickness()
        vcd = self.ropeNode.getVertexColorDimension()
        vtd = self.ropeNode.getVertexThicknessDimension()
        for i in range(numVerts):
            v = self.verts[i]
            if isinstance(v, types.TupleType):
                (nodePath, point) = v
                color = defaultColor
                thickness = defaultThickness
            else:
                nodePath = v.get('node', defaultNodePath)
                point = v.get('point', defaultPoint)
                color = v.get('color', defaultColor)
                thickness = v.get('thickness', defaultThickness)
            if isinstance(point, types.TupleType):
                if len(point) >= 4:
                    self.curve.setVertex(i, VBase4(point[0], point[1], point[2], point[3]))
                else:
                    self.curve.setVertex(i, VBase3(point[0], point[1], point[2]))
            else:
                self.curve.setVertex(i, point)
            if nodePath:
                self.curve.setVertexSpace(i, nodePath)
            
            if useVertexColor:
                self.curve.setExtendedVertex(i, vcd + 0, color[0])
                self.curve.setExtendedVertex(i, vcd + 1, color[1])
                self.curve.setExtendedVertex(i, vcd + 2, color[2])
                self.curve.setExtendedVertex(i, vcd + 3, color[3])
            
            if useVertexThickness:
                self.curve.setExtendedVertex(i, vtd, thickness)
                continue
        
        if self.knots != None:
            for i in range(len(self.knots)):
                self.curve.setKnot(i, self.knots[i])
            
        
        self.ropeNode.resetBound(self)

    
    def getPoints(self, len):
        result = self.curve.evaluate(self)
        startT = result.getStartT()
        sizeT = result.getEndT() - startT
        numPts = len
        ropePts = []
        for i in range(numPts):
            pt = Point3()
            result.evalPoint(sizeT * i / float(numPts - 1) + startT, pt)
            ropePts.append(pt)
        
        return ropePts



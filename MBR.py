__author__ = "abosi"
__version__ = "2022.03.30"

import Rhino.Geometry as rg
import math

def rebuildPoints(Points,roundDecimal):
    
    """ Rebuilds a list of points to a tolerance decimal """
    
    rebuiltPoints = []
    for i,pt in enumerate(Points):
        
        pt.X = round(pt.X,roundDecimal)
        pt.Y = round(pt.Y,roundDecimal)
        pt.Z = round(pt.Z,roundDecimal)
        
        rebuiltPoints.append(pt)
    
    return rebuiltPoints



def buildHull(points):
    points = sorted(points)
    
    #Check list validity
    if len(points) <= 3:
        print len(points)
        return points
    
    #cross product of 2 vectors for checking clockwise or anit.clockwise rotation
    def cross(o, a, b):
        cr = (a.X - o.X) * (b.Y - o.Y) - (a.Y - o.Y) * (b.X - o.X)
        return cr
    
    lower = []
    for p in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    
    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    
    return lower[:-1] + upper[:-1]

def rotateToAngle(vector, angle):
    v = vector
    a = angle
    newX = v.X * math.cos(a) - v.Y * math.sin(a)
    newY = v.X * math.sin(a) + v.Y * math.cos(a)
    pt = rg.Point3d(newX, newY, 0)
    return pt

def angleToAxis(line):
    delta = rg.Point3d.Subtract(line.From,line.To)
    return -math.atan(delta.Y/delta.X)

def minBoundingRectangle(points):
    minR = 0
    minA = 0
    for i,pt in enumerate(points):
        sg = rg.Line(points[i-1], points[i])
        
        angle = angleToAxis(sg)
        
        top = -float('inf')
        bottom = float('inf')
        right = -float('inf')
        left = float('inf')
        
        for p in points:
            rotatedPoints = rotateToAngle(p, angle)
            
            top = max(top, rotatedPoints.Y)
            bottom = min(bottom, rotatedPoints.Y)
            
            right = max(right, rotatedPoints.X)
            left = min(left, rotatedPoints.X)
        
        rectangle = rg.Rectangle3d(rg.Plane.WorldXY,rg.Point3d(left,bottom,0), rg.Point3d(right,top,0))
        if minR == 0 or minR.Area <= rectangle.Area:
            minR = rectangle
            minA = angle
        
    
    minRectangle = []
    for c in range(4):
        rotC = rotateToAngle(minR.Corner(c), -minA)
        minRectangle.append(rotC)
    
    return minRectangle

if __name__ == "__main__":
  points = rebuildPoints(points,5)
  print(len(points))
  CH = buildHull(points)
  hull, pts, rec = minBoundingRectangle(CH)

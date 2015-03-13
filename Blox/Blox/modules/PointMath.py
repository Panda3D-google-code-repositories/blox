import math

def PointDirection(x1,y1,x2,y2):
    return math.degrees(math.atan2(y2-y1,x2-x1))

def LengthDirX(x,distance,direction):
    return x+math.cos(direction*math.pi/180)*distance
    
def LengthDirY(y,distance,direction):
    return y+math.sin(direction*math.pi/180)*distance

def PointDistance(x1,y1,x2,y2):
    dx = x2 - x1
    dy = y2 - y1
    return math.sqrt(dx**2 + dy**2)

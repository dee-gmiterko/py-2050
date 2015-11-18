import math

class Planet():
    position = None
    size = None
    
    def __init__(self, x, y, size):
        self.position = (x, y)
        self.size = size
    
    def getHeight(self, angleOne):
        
        if not hasattr(self, 'height'):
            return 1.0
        
        ntp = angleOne * len(self.height)
        i1 = int(math.floor(ntp))
        h1 = self.height[i1]
        i2 = int(math.ceil(ntp))
        if i2 >= len(self.height):
            h2 = self.height[0]
        else:
            h2 = self.height[i2]

        d = ntp - i1
        return h1 + ((h2 - h1) * d)
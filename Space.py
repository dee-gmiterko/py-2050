class Space():
    
    seed = None
    blocksLayers = {}
    
    def __init__(self, seed):
        self.seed = seed
    
    def getBlockLayer(self, x, y):
        key = str(x)+','+str(y)
        if key in self.blocksLayers:
            return self.blocksLayers[key]
        else:
            return 0
    
    def setBlockLayer(self, x, y, layer):
        self.blocksLayers[str(x)+','+str(y)] = layer
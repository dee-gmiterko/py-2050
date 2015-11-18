from PIL import ImageDraw
from Tree import Tree
import math

class LayerPlanetsTrees():
    
    MAX_TREES_COUNT = 283
    TREE_SIZE = 0.1
    BUSH_SIZE = 0.04
    
    def init(self, space):
        pass
    
    def generate(self, space, block_x, block_y, random):
        
        if space.getBlockLayer(block_x, block_y) is not 3:
            return
        
        thisPlanetKey = str(block_x) + "," + str(block_y)
        if thisPlanetKey not in space.planets:
            space.setBlockLayer(block_x, block_y, 4)
            return
        thisPlanet = space.planets[thisPlanetKey]
        
        thisPlanet.trees = []
        
        for i in range(int(random() * self.MAX_TREES_COUNT * thisPlanet.size)):
            self.addTree(thisPlanet, random)
        
        space.setBlockLayer(block_x, block_y, 4)
    
    def addTree(self, planet, random):
        
        angleOne = random()
        angle = angleOne * 2 * math.pi
        size = random() * self.TREE_SIZE

        height = planet.getHeight(angleOne)

        s = planet.size / 2 * height
        fx = planet.position[0] + s * math.sin(angle)
        fy = planet.position[1] + s * math.cos(angle)
        
        planet.trees.append(Tree((fx, fy), angle, size))
    
    def render(self, space, im, transition):
        
        draw = ImageDraw.Draw(im)
        
        for planetIndex in space.planets:
            planet = space.planets[planetIndex]
            
            if not hasattr(planet, 'trees'):
                continue
            
            for tree in planet.trees:

                tp = transition(tree.position)
                
                if tree.size > self.BUSH_SIZE:
                    tx = tp[0] + transition(tree.size * math.sin(tree.angle))
                    ty = tp[1] + transition(tree.size * math.cos(tree.angle))
                    cx = tp[0] + transition(1.5 * tree.size * math.sin(tree.angle))
                    cy = tp[1] + transition(1.5 * tree.size * math.cos(tree.angle))
                
                    treeWidth = transition((0.2 * tree.size + 0.016) / 2)
                    draw.line((tp[0], tp[1], tx, ty), fill='#A54E68', width=treeWidth)
                else:
                    cx = tp[0] + transition(0.5 * tree.size * math.sin(tree.angle))
                    cy = tp[1] + transition(0.5 * tree.size * math.cos(tree.angle))
                
                s = transition(tree.size / 2)
                draw.ellipse((cx - s, cy - s, cx + s, cy + s), fill='#77C046')
    
    def get_min_zoom(self):
        return 80
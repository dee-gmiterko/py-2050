from PIL import ImageDraw
from Planet import Planet

class LayerPlanets():
    
    MIN_PLANET_SIZE = 0.06
    MAX_PLANET_SIZE = 1.1
    
    def init(self, space):
        space.planets = {}
    
    def generate(self, space, block_x, block_y, random):
        if space.getBlockLayer(block_x, block_y) == 0:
            size = self.MIN_PLANET_SIZE + (random() * (self.MAX_PLANET_SIZE - self.MIN_PLANET_SIZE))
            space.planets[str(block_x) + "," + str(block_y)] = Planet(block_x + random(), block_y + random(), size)
            space.setBlockLayer(block_x, block_y, 1)
    
    def render(self, space, im, transition):
        
        draw = ImageDraw.Draw(im)
        
        for planetIndex in space.planets:
            planet = space.planets[planetIndex]
            
            p = transition(planet.position)
            s = transition(planet.size / 2.0)
            
            for i in range(6, 1, -1):
                r = s + transition(i * 0.08)
                color = 'hsl(212,68%,'+str((7-i) * 5)+'%)'
                draw.ellipse((p[0] - r, p[1]-r, p[0] + r, p[1] + r), fill=color)
            
            draw.ellipse((p[0] - s, p[1]-s, p[0] + s, p[1] + s), fill='#2B3C4D')
    
    def get_min_zoom(self):
        return 0
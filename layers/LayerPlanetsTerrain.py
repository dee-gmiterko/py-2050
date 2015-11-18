from PIL import ImageDraw
import math
from noise import pnoise2

class LayerPlanetsTerrain():
    
    HEIGHT_RESOLUTION = 42
    MAX_HEIGHT = 0.3
    PLANET_HEIGHT_RADIUS = 2
    PLANET_HEIGHT_OCTAVES = 3
    
    def init(self, space):
        pass
    
    def generate(self, space, block_x, block_y, random):
        
        if space.getBlockLayer(block_x, block_y) is not 2:
            return
        
        thisPlanetKey = str(block_x) + "," + str(block_y)
        if thisPlanetKey not in space.planets:
            space.setBlockLayer(block_x, block_y, 3)
            return
        thisPlanet = space.planets[thisPlanetKey]
        
        planetsAroundCount = 0
        for dx in range(-1, 1):
            for dy in range(-1, 1):
                thatPlanetKey = str(block_x+dx)+","+str(block_y+dy)
                if thatPlanetKey in space.planets:
                    planetsAroundCount += 1
        
        planetsAroundFactor = (planetsAroundCount + 1)/2
        
        thisPlanet.height = []
        for i in range(0, self.HEIGHT_RESOLUTION):
            
            a = math.pi * 2 * (float(i) / self.HEIGHT_RESOLUTION)
            hx = self.PLANET_HEIGHT_RADIUS * thisPlanet.size * math.sin(a)
            hy = self.PLANET_HEIGHT_RADIUS * thisPlanet.size * math.cos(a)
            h = pnoise2(thisPlanet.position[0] + hx, thisPlanet.position[1] + hy, self.PLANET_HEIGHT_OCTAVES)
            
            thisPlanet.height.append(1.0 + self.MAX_HEIGHT + h * self.MAX_HEIGHT * planetsAroundFactor)
        
        space.setBlockLayer(block_x, block_y, 3)
        
    def render(self, space, im, transition):
        
        draw = ImageDraw.Draw(im)
        
        for planetIndex in space.planets:
            planet = space.planets[planetIndex]
            
            if not hasattr(planet, 'height'):
                continue
            
            p = transition(planet.position)
            
            poly = []
            c = math.pi * 2 / len(planet.height)
            i = 0
            for height in planet.height:
                a = c * i
                i += 1
                
                s = planet.size / 2 * height
                x = transition(s * math.sin(a))
                y = transition(s * math.cos(a))
                
                poly.append((p[0] + x, p[1] + y))
            
            draw.polygon(poly, fill='#2B3C4D')
            
            grassHeight = transition(0.005)
            for i in range(0, len(poly)):
                j = i+1
                if j ==len(poly):
                    j = 0
                draw.line(poly[i]+poly[j], fill='#77C046', width=grassHeight)

    def get_min_zoom(self):
        return 40
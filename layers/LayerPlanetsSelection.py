from PIL import ImageDraw
from noise import pnoise2
import math

class LayerPlanetsSelection():
    
    RENDER = False
    MIN_PLANET_DISTANCE = 1.66
    PLANET_GEN_RANGE = 2
    
    def init(self, space):
        space.removedPlanets = []
    
    def generate(self, space, block_x, block_y, random):
        
        if space.getBlockLayer(block_x, block_y) is not 1:
            return
        
        for dx in range(-1 * self.PLANET_GEN_RANGE, self.PLANET_GEN_RANGE):
            for dy in range(-1 * self.PLANET_GEN_RANGE, self.PLANET_GEN_RANGE):
                if space.getBlockLayer(block_x + dx, block_y + dy) < 1:
                    return
        
        thisPlanetKey = str(block_x) + "," + str(block_y)
        if thisPlanetKey not in space.planets:
            space.setBlockLayer(block_x, block_y, 2)
            return
        thisPlanet = space.planets[thisPlanetKey]
        
        #PLANETS TOO CLOSE
        for dx in range(-1 * self.PLANET_GEN_RANGE, self.PLANET_GEN_RANGE):
            for dy in range(-1 * self.PLANET_GEN_RANGE, self.PLANET_GEN_RANGE):
                if dx == 0 and dy == 0:
                    continue
                thatPlanetKey = str(block_x+dx)+","+str(block_y+dy)
                if thatPlanetKey not in space.planets:
                    continue
                thatPlanet = space.planets[thatPlanetKey]
                
                x1, y1 = thisPlanet.position
                x2, y2 = thatPlanet.position
                xd = x1-x2
                yd = y1-y2
                
                distance = math.sqrt(xd*xd+yd*yd)
                
                if distance < self.MIN_PLANET_DISTANCE:
                    if self.selectPlanetForDestruction(space.seed, thisPlanet, thatPlanet, random):
                        space.removedPlanets.append(thisPlanet.position)
                        del space.planets[thisPlanetKey]
                        
                        space.setBlockLayer(block_x, block_y, 2)
                        return
                    else:
                        space.removedPlanets.append(thatPlanet.position)
                        del space.planets[thatPlanetKey]

        space.setBlockLayer(block_x, block_y, 2)
    
    def selectPlanetForDestruction(self, seed, thisPlanet, thatPlanet, random):
        r = pnoise2(seed + thisPlanet.position[0] / 51, seed + thisPlanet.position[1] / 51, 7)
        if r < 0:
            return thatPlanet.size > thisPlanet.size # remove smaller planet
        else:
            return thatPlanet.size < thisPlanet.size # remove larger planet
    
    def render(self, space, im, transition):
        
        if self.RENDER:
            draw = ImageDraw.Draw(im)

            for removedPlanet in space.removedPlanets:

                p = transition(removedPlanet)
                s = transition(0.06)
                w = transition(0.03)
                draw.line((p[0] - s, p[1]-s, p[0] + s, p[1] + s), fill='#A54E68', width=w)
                draw.line((p[0] + s, p[1]-s, p[0] - s, p[1] + s), fill='#A54E68', width=w)

    def get_min_zoom(self):
        return 0
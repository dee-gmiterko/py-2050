from PIL import ImageDraw

class LayerPlanetsLife():
    
    PLANET_GEN_RANGE = 3
    MIN_TREES = 1000
    
    def init(self, space):
        space.removedPlanets = []
    
    def generate(self, space, block_x, block_y, random):
        
        for dx in range(-1 * self.PLANET_GEN_RANGE, self.PLANET_GEN_RANGE):
            for dy in range(-1 * self.PLANET_GEN_RANGE, self.PLANET_GEN_RANGE):
                if space.getBlockLayer(block_x + dx, block_y + dy) < 4:
                    return
        
        thisPlanetKey = str(block_x) + "," + str(block_y)
        if thisPlanetKey not in space.planets:
            space.setBlockLayer(block_x, block_y, 5)
            return
        thisPlanet = space.planets[thisPlanetKey]
        
        #SUITABLE FOR LIFE
        totalTrees = 0
        for dx in range(-1 * self.PLANET_GEN_RANGE, self.PLANET_GEN_RANGE):
            for dy in range(-1 * self.PLANET_GEN_RANGE, self.PLANET_GEN_RANGE):
                thatPlanetKey = str(block_x+dx)+","+str(block_y+dy)
                if thatPlanetKey not in space.planets:
                    continue
                thatPlanet = space.planets[thatPlanetKey]
                
                totalTrees += len(thatPlanet.trees)
        
        thisPlanet.life = totalTrees > self.MIN_TREES
        
        space.setBlockLayer(block_x, block_y, 5)
    
    def render(self, space, im, transition):
        
        draw = ImageDraw.Draw(im)

        for planet in space.planets.values():

            if not hasattr(planet, 'life'):
                continue

            if planet.life:
                p = transition(planet.position)
                s = transition(planet.size / 2)
                w = transition(0.05)
                draw.ellipse((p[0] - s, p[1]-s, p[0] + s, p[1] + s), fill='#A54E68')

    def get_min_zoom(self):
        return 80
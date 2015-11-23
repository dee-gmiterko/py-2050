#!/usr/bin/python
from PIL import Image
from Space import Space
import layers

WIDTH = 1920
HEIGHT = 1080
ZOOM = 100
SEED = 96
RENDER_PER_STEP = False
RENDER_PER_LAYER = False
BACKGROUND = 'black'
MAX_LAYERS = None
SHOW = False

from optparse import OptionParser
parser = OptionParser()
parser.add_option("-W", "--width",
                  metavar="NUMBER", type="int",
                  dest="width", default=WIDTH,
                  help="Width of image")
parser.add_option("-H", "--height",
                  metavar="NUMBER", type="int",
                  dest="height", default=HEIGHT,
                  help="Height of image")
parser.add_option("-z", "--zoom",
                  metavar="NUMBER", type="int",
                  dest="zoom", default=ZOOM,
                  help="Zoom represents diameter of largest planet in pixels")
parser.add_option("-s", "--seed",
                  metavar="NUMBER", type="int",
                  dest="seed", default=SEED,
                  help="Seed used to generate image")
parser.add_option('-S', "--steps",
                  action="store_true", dest="steps", default=False,
                  help="Render each step separately")
parser.add_option('-L', "--layers",
                  action="store_true", dest="layers", default=False,
                  help="Render each layer separately")
parser.add_option("-t", "--temporary",
                  action="store_true", dest="temporary", default=False,
                  help="Store image result in temporary file and display result.")
options, optionsValues = parser.parse_args()

WIDTH = options.width
HEIGHT = options.height
ZOOM = options.zoom
SEED = options.seed
RENDER_PER_STEP = options.steps
RENDER_PER_LAYER = options.layers
SHOW = options.temporary

import random
random.seed(SEED)

usedLayers = [layers.LayerPlanets(), layers.LayerPlanetsSelection(), layers.LayerPlanetsTerrain(), layers.LayerPlanetsTrees(), layers.LayerPlanetsLife()]

im = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND)
space = Space(SEED)

def saveImage(image, steps, layers):
    if SHOW:
        image.show()
    else:
        name = "out"
        if steps != None:
            name += "-s" + str(steps)
        if layers != None:
            name += "-l" + str(layers)
        name += ".png"
        image.save(name, 'PNG')
        print("Image saved as " + name)

for layer in usedLayers:
    layer.init(space)

#
# GENERATE LAYERS
#
requiredLayersCount = 0
for layer in usedLayers:
    if layer.get_min_zoom() <= ZOOM:
        requiredLayersCount += 1

if MAX_LAYERS and requiredLayersCount > MAX_LAYERS:
    requiredLayersCount = MAX_LAYERS

allSuccess = False
range = 0
while not allSuccess:
    allSuccess = True
    range += 1
    for layerIndex in xrange(0, requiredLayersCount):
        layer = usedLayers[layerIndex]
        for x in xrange(-1 * range, range):
            for y in xrange(-1 * range, range):
                layer.generate(space, x, y, random.random)

    w = int(WIDTH / 2 / ZOOM) + 1
    h = int(HEIGHT / 2 / ZOOM) + 1
    for x in xrange(-1 * w, w):
        for y in xrange(-1 * h, h):
            if space.getBlockLayer(x, y) < requiredLayersCount:
                allSuccess = False

    #
    # RENER LAYERS
    #
    def transition(coords):
        scalar = type(coords) not in (tuple, list)
        if scalar:
            coords = (coords,)
            scalar = True
        #zoom
        coords = [x * ZOOM for x in coords]
        
        #offset
        if len(coords) == 2:
            coords[0] += WIDTH / 2
            coords[1] += HEIGHT / 2
        
        #round
        coords = [int(x) for x in coords]

        if scalar:
            return coords[0]
        else:
            return coords

    if RENDER_PER_STEP:
        im.paste(BACKGROUND, (0, 0, WIDTH, HEIGHT))
        li = 0
        for layer in usedLayers:
            layer.render(space, im, transition)
            if RENDER_PER_LAYER:
                saveImage(im, range, li)
                li += 1
        if not RENDER_PER_LAYER:
            saveImage(im, range, None)

if not RENDER_PER_STEP:
    li = 0
    for layer in usedLayers:
        layer.render(space, im, transition)
        if RENDER_PER_LAYER:
            saveImage(im, None, li)
            li += 1
    if not RENDER_PER_LAYER:
        saveImage(im, None, None)
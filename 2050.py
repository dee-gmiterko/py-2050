#!/usr/bin/python
from PIL import Image
from Space import Space
import layers
import math

WIDTH = 1920
HEIGHT = 1080
ZOOM = 100
SEED = 96
RENDER_PER_STEP = False
RENDER_PER_LAYER = False
BACKGROUND = 'black'
MAX_LAYERS = None

import random
random.seed(SEED)

usedLayers = [layers.LayerPlanets(), layers.LayerPlanetsSelection(), layers.LayerPlanetsTerrain(), layers.LayerPlanetsTrees(), layers.LayerPlanetsLife()]

im = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND)
space = Space(SEED)

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
            coords = (coords, )
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
        for layer in usedLayers:
            layer.render(space, im, transition)
            if RENDER_PER_LAYER:
                im.show()
        if not RENDER_PER_LAYER:
            im.show()

if not RENDER_PER_STEP:
    for layer in usedLayers:
        layer.render(space, im, transition)
        if RENDER_PER_LAYER:
            im.show()
    if not RENDER_PER_LAYER:
        im.show()
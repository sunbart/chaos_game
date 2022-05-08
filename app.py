from math import ceil, floor
import random, time

from common import midpoint, PointMap, presets

# Config
preset_name = 3
scale = 2_000
iters = 1_000_000

# Setup
width, height, anchors = presets[preset_name]
width = ceil(width * scale)
height = ceil(height * scale)
anchors = [(floor(anchor[0] * scale), floor(anchor[1] * scale)) for anchor in anchors]

current_point = (random.random() * width, random.random() * height)
pm = PointMap(width, height)

start = time.time()

# Generate point map
try:
    for iter_no in range(iters + 1):
        current_point = midpoint(random.choice(anchors), current_point)
        pm.add(*current_point)
except KeyboardInterrupt:
    pass

print(time.time() - start)

# Save image
pm.normalize().save(f"{preset_name}_{iter_no}.png")

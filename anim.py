from math import ceil, floor
import random

from common import midpoint, PointMap, presets


# Config
preset_name = 5
scale = 1_000
iters = 10_000
frame_count = 240

# Setup
frames = []
width, height, anchors = presets[preset_name]
width = ceil(width * scale)
height = ceil(height * scale)
anchors = [(floor(anchor[0] * scale), floor(anchor[1] * scale)) for anchor in anchors]
current_point = (random.random() * width, random.random() * height)
pm = PointMap(width, height)

# Generate frames
try:
    for frame_no in range(frame_count):
        print(f"Generating frame {frame_no}", end="\r")
        for _ in range(iters):
            current_point = midpoint(random.choice(anchors), current_point)
            pm.add(*current_point)
        frames.append(pm.copy())

except KeyboardInterrupt:
    pass

# Save frames
print("                                           ", end="\r")
max_value = max(frames[-1].data)
for frame_no, frame in enumerate(frames):
    print(f"Saving frame {frame_no}", end="\r")
    frame.normalize(max_value).save(f"anim/{frame_no}.png")
    frame.normalize().save(f"anim/in/{frame_no}.png")

print("Done                               ")

from itertools import repeat
from math import floor
from PIL import Image
import random


def make_scaler(from_min, from_max, to_min, to_max):
    from_size = from_max - from_min

    def scaler(value):
        return (((value - from_min) / from_size) * to_max) + to_min

    return scaler


class PointMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.data = list(repeat(0, self.width * self.height))

    def save(self, path):
        img = Image.new("L", (self.width, self.height))
        img.putdata(self.data)
        img.save(path)

    def normalize(self, max_value=None):
        if max_value is None:
            max_value = max(self.data)

        new_pm = PointMap(self.width, self.height)
        new_pm.data = list(map(make_scaler(0, max_value, 0, 255), self.data))
        return new_pm

    def copy(self):
        new_pm = PointMap(self.width, self.height)
        new_pm.data = self.data.copy()
        return new_pm

    def add(self, x, y):
        self.data[floor(y) * self.width + floor(x)] += 1

    def print(self):
        print(self.data)


def midpoint(point_1, point_2):
    return tuple((coord_1 + coord_2) / 2 for coord_1, coord_2 in zip(point_1, point_2))


presets = {
    3: [1.14, 1, [(0.57, 0.05), (0.05, 0.95), (1.09, 0.95)]],
    4: [1, 1, [(0.05, 0.05), (0.05, 0.95), (0.95, 0.95), (0.95, 0.05)]],
    5: [
        1.046,
        1,
        [(0.5, 0.05), (0.95, 0.393), (0.816, 0.95), (0.23, 0.95), (0.05, 0.393)],
    ],
    6: [
        1.14,
        1,
        [
            (0.829, 0.05),
            (1.09, 0.5),
            (0.829, 0.95),
            (0.31, 0.95),
            (0.05, 0.5),
            (0.31, 0.05),
        ],
    ],
    7: [
        1.023,
        1,
        [
            (0.511, 0.05),
            (0.882, 0.228),
            (0.973, 0.629),
            (0.717, 0.95),
            (0.306, 0.95),
            (0.05, 0.629),
            (0.141, 0.228),
        ],
    ],
    "arrow": [
        1,
        1,
        [(0.05, 0.05), (0.95, 0.5), (0.05, 0.95), (0.2, 0.5)],
    ],
}

presets["random"] = [1, 1, []]
for _ in range(4):
    presets["random"][2].append((random.random(), random.random()))

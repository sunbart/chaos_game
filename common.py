from itertools import repeat
from math import floor, log10, sin, cos, pi
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


def log_interpoint(point_1, point_2, pre_num, post_num):
    return tuple(
        coord_2 + (coord_1 - coord_2) * log10(pre_num / post_num)
        for coord_1, coord_2 in zip(point_1, point_2)
    )


def mean_interpoint(point_1, point_2, pre_num, post_num):
    return tuple(
        (coord_1 * pre_num + coord_2 * post_num) / (pre_num + post_num)
        for coord_1, coord_2 in zip(point_1, point_2)
    )


def relation_interpoint(point_1, point_2, pre_num, post_num):
    return tuple(
        (coord_1 * pre_num + coord_2 * post_num) / (pre_num + post_num)
        for coord_1, coord_2 in zip(point_1, point_2)
    )


def anchor_generator(count, middle=(0.5, 0.5), radius=0.45):
    return [
        (
            middle[0] + radius * cos(2 * i * pi / count),
            middle[1] + radius * sin(2 * i * pi / count),
        )
        for i in range(count)
    ]


presets = {
    "arrow": [
        1,
        1,
        [(0.05, 0.05), (0.95, 0.5), (0.05, 0.95), (0.2, 0.5)],
    ],
}

presets["random"] = [1, 1, []]
for _ in range(4):
    presets["random"][2].append((random.random(), random.random()))


for count in range(3, 8):
    presets[count] = [1, 1, anchor_generator(count)]

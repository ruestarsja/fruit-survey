default_resolution = 1200
color = {
    "background": (230, 190, 110),
    "harvester": (225, 225, 225),
    "rock": (175, 170, 160),
    "henna": (210, 60, 90),
    "sweet": (220, 170, 40),
    "ajilenakh": (153, 165, 58),
    "weasel": (150, 86, 30),
    "tricolor_jelly": (255, 255, 255),
}
# exteding color dict, reusing existing colors
color = {**color, **{
    "trapped_henna_1": color["henna"],
    "trapped_sweet_1": color["sweet"],
    "trapped_ajilenakh_1": color["ajilenakh"],
    "trapped_henna_2": color["henna"],
    "trapped_sweet_2": color["sweet"],
    "trapped_ajilenakh_2": color["ajilenakh"],
    "digging_weasel": color["weasel"],
}}

class Sprite():
    def __init__(self, img_path:str):
        self.__path = img_path
    def path(self):
        return self.__path
    def load(self):
        import pygame as pg
        image = pg.image.load(self.__path)
        del pg
        return image

itemfromid = [
    "rock",                # 0
    "henna",               # 1
    "sweet",               # 2
    "ajilenakh",           # 3
    "trapped_henna_1",     # 4
    "trapped_sweet_1",     # 5
    "trapped_ajilenakh_1", # 6
    "trapped_henna_2",     # 7
    "trapped_sweet_2",     # 8
    "trapped_ajilenakh_2", # 9
    "weasel",              # 10
    "digging_weasel",      # 11
    "tricolor_jelly",      # 12
    "harvester"            # -1
]

from math import sqrt

sqrt2 = sqrt(2)

del sqrt
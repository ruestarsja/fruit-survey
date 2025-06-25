default_resolution = 1200
color = {
    "background": (230, 190, 110),
    "harvester": (225, 225, 225),
    "rock": (175, 170, 160),
    "henna": (210, 60, 90),
    "sweet": (240, 190, 60),
    "ajilenakh": (153, 165, 58)
}

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
    "rock",
    "henna",
    "sweet",
    "ajilenakh",
    "trapped_henna_1",
    "trapped_sweet_1",
    "trapped_ajilenakh_1",
    "trapped_henna_2",
    "trapped_sweet_2",
    "trapped_ajilenakh_2",
    "weasel",
    "digging_weasel",
    "tricolor_jelly",
    "harvester"
]
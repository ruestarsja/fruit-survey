import os
import pygame as pg
import constants as k

class Game():
    def __init__(self):
        pg.init()

        self.__levels:dict = self.__load_levels_json()
        self.__current_level:str = None
        resolution = (k.default_resolution, 0.75*k.default_resolution)
        self.__window = pg.display.set_mode(resolution)
        self.__grid_size = 0.8*min(resolution)
        self.__grid_offset = (0.5*(0.25*k.default_resolution) + 0.5*(0.2*min(resolution)), 0.1*min(resolution))
    
    def run(self):
        self.__running = True
        self.__clock = pg.time.Clock()
        
        
        while self.__running:
            self.__clock.tick(30)

            # TEMP below
            self.__load_level("l1")
            # TEMP above

            for event in pg.event.get():
                if event.type == pg.MOUSEBUTTONDOWN:
                    mousepos = pg.mouse.get_pos
                    self.__process_click(mousepos)
                if event.type == pg.QUIT:
                    self.__running = False
            self.__update_display()
        
        pg.quit()


    def __load_levels_json(self):
        import json
        with open("levels.json", "r") as fin:
            levels = json.load(fin)
        del json
        return levels
    
    def __load_level(self, level:str):
        self.__current_level = self.__levels[level]
    
    def __process_click(self, mousepos):
        pass

    def __update_display(self):
        self.__window.fill(k.color["background"])
        if self.__current_level is not None:
            grid_square_size = self.__grid_size // len(self.__current_level["board"])
            for r, row in enumerate(self.__current_level["board"]):
                for c, cell in enumerate(row):
                    rect = (
                        self.__grid_offset[0] + c*grid_square_size,
                        self.__grid_offset[1] + r*grid_square_size,
                        grid_square_size,
                        grid_square_size
                    )
                    sprite = self.__fetch_sprite(k.itemfromid[cell])
                    try:
                        self.__window.blit(sprite.load(), rect)
                    except FileNotFoundError:
                        color = k.color[k.itemfromid[cell]]
                        self.__window.fill(color, rect)
        pg.display.update()

    def __fetch_sprite(self, item:str):
        return k.Sprite("images" + os.sep + item + ".png")

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
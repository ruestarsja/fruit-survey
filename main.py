import os
import pygame as pg
import constants as k

class Game():
    def __init__(self):
        pg.init()

        self.__levels:dict = self.__load_levels_json()
        self.__current_level:dict|None = None
        self.__board:list|None = None
        self.__harvester_location:tuple|None = None
        self.__trail_head_location:tuple|None = None
        self.__trail:list|None = None
        self.__trail_type:str|None = None

        resolution = (k.default_resolution, 0.75*k.default_resolution)
        self.__window:pg.Surface = pg.display.set_mode(resolution)
        self.__grid_size:int|float = 0.8*min(resolution)
        self.__grid_offset:tuple = (0.5*(0.25*k.default_resolution) + 0.5*(0.2*min(resolution)), 0.1*min(resolution))
    
    def run(self):
        self.__running = True
        self.__clock = pg.time.Clock()
        
        # TEMP below
        self.__load_level("test")
        # TEMP above
        
        while self.__running:
            self.__clock.tick(30)


            for event in pg.event.get():
                if event.type == pg.MOUSEBUTTONDOWN:
                    mousepos = pg.mouse.get_pos()
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
        lvl = self.__current_level = self.__levels[level]
        board = self.__board = lvl["board"]
        i = 0
        while i < len(board) and self.__harvester_location is None:
            j = 0
            while j < len(board[i]) and self.__harvester_location is None:
                if board[i][j] == -1:
                    self.__harvester_location = (i, j)
                j += 1
            i += 1
        self.__trail_head_location = self.__harvester_location
        self.__trail = [self.__harvester_location]
    
    def __unload_level(self):
        self.__current_level = None
        self.__board = None
        self.__harvester_location = None
        self.__trail_head_location = None
        self.__trail = None
    
    def __process_click(self, mousepos):
        clicked = self.__get_object_from_pos(mousepos)
        if clicked[0] == "grid_square":
            grid_square_loc = clicked[1]
            if self.__is_adjacent_to_trail_head(grid_square_loc):
                print("Clicked adjacent to trail head!")
                if grid_square_loc in self.__trail:
                    print("Already visited space.")
                else:
                    print("New space!")
                    new:str = k.itemfromid[self.__board[grid_square_loc[0]][grid_square_loc[1]]]
                    blacklist = [
                        "rock",
                        "trapped_henna_1",
                        "trapped_sweet_1",
                        "trapped_ajilenakh_1",
                        "trapped_henna_2",
                        "trapped_sweet_2",
                        "trapped_ajilenakh_2"
                    ]
                    whitelist = [
                        "weasel",
                        "digging_weasel"
                        "tricolor_jelly"
                    ]
                    trail_types = [
                        "henna",
                        "sweet",
                        "ajilenakh"
                    ]
                    if self.__trail_type is None:
                        if new not in blacklist:
                            self.__trail_head_location = grid_square_loc
                            self.__trail.append(self.__trail_head_location)
                            if new in trail_types:
                                self.__trail_type = new
                                print(f"New trail type: {new}")
                            else:
                                print("No new trail type.")
                        else:
                            print("Cannot use that type of grid square.")
                    elif self.__trail_type == new or new in whitelist:
                        self.__trail_head_location = grid_square_loc
                        self.__trail.append(self.__trail_head_location)
                        if new == "tricolor_jelly":
                            self.__trail_type = None
                            print("Tricolor jelly!!")
                        else:
                            print("Moving to new matching fruit!")
                    else:
                        print("Wrong type of space for this trail type.")
                print(self.__trail)
            elif grid_square_loc == self.__trail_head_location:
                if grid_square_loc == self.__harvester_location:
                    print("Can't undo further: reached harvester location.")
                else:
                    self.__trail.pop()
                    print(self.__trail)
                    print(self.__trail[-1])
                    self.__trail_head_location = self.__trail[-1]
                    print(self.__trail_head_location)
                    current = k.itemfromid[self.__board[self.__trail_head_location[0]][self.__trail_head_location[1]]]
                    if current in ("harvester", "tricolor_jelly"):
                        self.__trail_type = None
                        print("Backed onto tricolor jelly or harvester!")
                    else:
                        print("Undone.")
                        print(self.__trail)
                        print(self.__trail_head_location)
            else:
                print("Clicked on non-adjacent grid square.")
        else:
            print("Clicked on nothing.")

    def __get_object_from_pos(self, pos):
        if self.__current_level == None:
            return ("unknown",)
        else:
            in_grid_pos = (pos[0] - self.__grid_offset[0], pos[1] - self.__grid_offset[1])
            if max(in_grid_pos) > self.__grid_size or min(in_grid_pos) < 0:
                return ("unknown",)
            else:
                grid_square_size = self.__grid_size // len(self.__current_level["board"])
                grid_square = (int(in_grid_pos[1] // grid_square_size), int(in_grid_pos[0] // grid_square_size))
                return ("grid_square", grid_square)
    
    def __is_adjacent_to_trail_head(self, grid_square):
        if grid_square == self.__trail_head_location:
            return False
        elif abs(grid_square[0] - self.__trail_head_location[0]) > 1 or abs(grid_square[1] - self.__trail_head_location[1]) > 1:
            return False
        else:
            return True

    def __update_display(self):
        self.__window.fill(k.color["background"])
        if self.__current_level is None:
            # menu display goes here
            pass
        else:
            grid_square_size = self.__grid_size // len(self.__current_level["board"])
            
            # RENDER TRAIL VISUALIZATION
            # NOTE: the following code only allows for the trail to be one color (whatever type of
            # trail is currently tracked at the trail head. The trail should be split at any
            # tricolor jelly spaces and have each piece (including the tcj space in both pieces)
            # render a separate trail visualization of the appropriate color.
            trail_coords = []
            for grid_square in self.__trail:
                # self.__trail points are stored as (row, col), which is (y, x), but these coords need to be (x, y)
                coords = (
                    grid_square[1] * grid_square_size + self.__grid_offset[0] + 0.5*grid_square_size,
                    grid_square[0] * grid_square_size + self.__grid_offset[1] + 0.5*grid_square_size
                )
                trail_coords.append(coords)

            i = 0
            while i < len(trail_coords) - 1:
                trail_color = ( k.color[self.__trail_type] ) if ( self.__trail_type is not None ) else ( (0, 0, 0) )
                trail_width = ( 20 ) if ( trail_coords[i][0] == trail_coords[i+1][0] or trail_coords[i][1] == trail_coords[i+1][1] ) else ( int(20 * k.sqrt2) )
                pg.draw.line(
                    surface   = self.__window,
                    color     = trail_color,
                    start_pos = trail_coords[i],
                    end_pos   = trail_coords[i + 1],
                    width     = trail_width
                )
                i += 1

            # RENDER GRID ITEMS
            for r, row in enumerate(self.__current_level["board"]):
                for c, cell in enumerate(row):
                    rect = (
                        self.__grid_offset[0] + c*grid_square_size - (10 if k.itemfromid[cell] == "harvester" else 0),
                        self.__grid_offset[1] + r*grid_square_size - (90 if k.itemfromid[cell] == "harvester" else 0),
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
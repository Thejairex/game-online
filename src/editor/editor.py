import pygame as pg

from config import Colors, Config
from src.editor.grid import Grid

import os

class MapEditor():
    def __init__(self):
        self.grid = Grid()
        pg.init()
        self.screen = pg.display.set_mode((Config.WIN_WIDTH, Config.WIN_HEIGHT))
        self.clock = pg.time.Clock()
        
    def run(self):
        # verificar si se ha guardado el mapa
        if os.path.exists("map.json"):
            self.grid.load_map("map.json")

        while True:
            self.events()
            self.update()
            self.draw()
    
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                # save map
                self.grid.save_map("map.json")
                pg.quit()
                quit()

            if event.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()
                # print(pos)
                self.handle_click(pos)
    
        keys = pg.key.get_pressed()
        if keys[pg.K_p]:
            self.grid.load_map("map.json")
            
    def update(self):
        pass

    def draw(self):
        self.screen.fill(Colors.BLACK)
        self.grid.draw(self.screen)
        pg.display.flip()

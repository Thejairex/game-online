import pygame as pg

from config import Colors, Config

class Tile():
    def __init__(self, x, y, solid= False):
        self.x = x
        self.y = y
        self.solid = solid
        self.color = Colors.BLACK
        
    def change_color(self, color):
        self.color = color
    
    def toggle_solid(self):
        self.solid = not self.solid
        
    def draw(self, surface):
        rect = pg.Rect(self.x * Config.TILE_SIZE, self.y * Config.TILE_SIZE, Config.TILE_SIZE, Config.TILE_SIZE)
        pg.draw.rect(surface, self.color, rect)
        pg.draw.rect(surface, Colors.BLACK, rect, 1)
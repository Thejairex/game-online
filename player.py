import pygame as pg

from config import *

class Player:
    """
    Model of the player in the game 
    """
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size

    def update(self):
        pass

    def draw(self, surface):
        pg.draw.rect(surface, Colors.RED, (self.x, self.y, self.size, self.size))
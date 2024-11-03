import pygame as pg

from config import *

class Player:
    """
    Model of the player in the game 
    """
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.speed = 5
        self.size = size
        self.color = Colors.RED
        self.last_action = None

    def move(self, keys):
        x_before = self.x
        y_before = self.y
        if keys[pg.K_UP]:
            self.y -= self.speed
        if keys[pg.K_DOWN]:
            self.y += self.speed
        if keys[pg.K_LEFT]:
            self.x -= self.speed
        if keys[pg.K_RIGHT]:
            self.x += self.speed
            
        if x_before != self.x or y_before != self.y:
            self.last_action = "move"

    def draw(self, surface):
        pg.draw.rect(surface, self.color, (self.x, self.y, self.size, self.size))
        
    def to_dict(self):
        return {"x": self.x, "y": self.y, "color": self.color}
    
    def from_dict(self, data):
        self.x = data["x"]
        self.y = data["y"]
        self.color = data["color"]
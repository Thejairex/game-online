import pygame as pg

from config import *

class Player:
    """
    Model of the player in the game 
    """
    def __init__(self, x, y, size):
        """
        Initializes the player
        """
        self.x = x
        self.y = y
        self.speed = 5
        self.size = size
        self.color = Colors.RED
        self.last_action = None

    def move(self, keys):
        """
        Calculates the movement of the player if the keys are pressed.
        
        Args:
            keys (list): List of pressed keys
        """
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
        
        # Check if the player moved 
        if x_before != self.x or y_before != self.y:
            self.last_action = "move"

    def draw(self, surface):
        """
        Draws the player on the screen.
        
        Args:
            surface (Surface): Surface to draw on
        """
        pg.draw.rect(surface, self.color, (self.x, self.y, self.size, self.size))
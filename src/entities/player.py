import pygame as pg

from config import Colors, Config

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
        
    def can_move(self, x, y):
        """
        Check if the player can move to the new position
        
        args:
            x (int): x position
            y (int): y position
        """
        return x >= 0 and x < Config.WIN_WIDTH and y >= 0 and y < Config.WIN_HEIGHT 

    def move(self, keys):
        """
        Calculates the movement of the player if the keys are pressed.
        
        Args:
            keys (list): List of pressed keys
        """
        x_before, y_before = self.x, self.y
        if keys[pg.K_UP] and self.can_move(self.x, self.y - self.speed):
            self.y -= self.speed
        if keys[pg.K_DOWN] and self.can_move(self.x, self.y + self.speed):
            self.y += self.speed
        if keys[pg.K_LEFT] and self.can_move(self.x - self.speed, self.y):
            self.x -= self.speed
        if keys[pg.K_RIGHT] and self.can_move(self.x + self.speed, self.y):
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
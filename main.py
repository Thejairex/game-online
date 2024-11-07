import pygame as pg
import asyncio

from src.entities.player import Player
from client import Client
from config import OPCODES
from config import *


class Game:
    """
    Class that represents the game with the players
    """
    def __init__(self):
        pg.init()
        """
        Initializes the game
        """
        self.screen = pg.display.set_mode((800, 600))
        self.players = {
            0: Player(0, 0, 50),
            1: Player(100, 0, 50),
            2: Player(200, 0, 50),
            3: Player(300, 0, 50),
        }
        self.clock = pg.time.Clock()
        self.fps = 120
        self.client = Client()
        
        self.player = None
        self.connected = False
        self.running = True
        
        self.queue = asyncio.Queue()
        self.events_task = []

    async def run(self):
        """
        Starts the game loop
        """
        while self.running:
            await self.events()
            await self.process_queue()
            await self.update()
            self.draw()
            await asyncio.sleep(0.01)  # Sleep for 0.01 seconds to reduce CPU usage

    async def events(self):
        """
        Handles the events of the game
        """
        
        # Close the game
        for event in pg.event.get():
            if event.type == pg.QUIT:
                await self.client.disconnect()
                self.running = False

        # Get the pressed keys
        keys = pg.key.get_pressed()
        
        # Online
        if keys[pg.K_ESCAPE]:
            if not self.connected:
                await self.client.send({"operation": OPCODES.CONNECT, "player": (0, 0)})
                asyncio.create_task(self.client.receive(self.queue))  # Pasa la cola a la tarea
                self.connected = True
        
        # Offline
        if keys[pg.K_SPACE] and not self.connected:
            self.player = 0
            self.players[self.player].color = Colors.GREEN
            self.connected = True
        
        # Move the player
        if self.player is not None:
            self.players[self.player].move(keys)
                
    async def process_queue(self):
        """
        Processes the queue of the server and sends the data to the players
        """
        while not self.queue.empty():
            data = await self.queue.get() # returns the next item in the queue
            
            # Process the data
            if data["operation"] == OPCODES.CONNECT:
                """
                Receives the player index and color from the server and data of the players
                """
                
                # Set the player
                if self.player is None:
                    self.player = data["player"]
                    
                # Set the color of the players
                for player_data in data["players"]:
                    index = player_data["index"]
                    color = player_data["color"]
                    self.players[index].color = color
                
            elif data["operation"] == OPCODES.MOVE:
                """
                Gets the movement of the player from the server
                """
                player, x, y = data["player"], data["x"], data["y"]
                self.players[player].x, self.players[player].y = x, y
                

    async def update(self):
        """
        Update the game state and send the data to the server
        """
        if self.player is not None:
            
            # Send the last action to the server
            if self.players[self.player].last_action == "move":
                self.players[self.player].last_action = None
                data = {"operation": OPCODES.MOVE, "player": self.player, "x": self.players[self.player].x, "y": self.players[self.player].y}
                await self.client.send(data)
        
        # Frame rate control
        self.clock.tick(self.fps)

    def draw(self):
        """
        Draws the game on the screen
        """
        
        self.screen.fill(Colors.BLACK)

        for player in self.players.values():
            player.draw(self.screen)

        pg.display.flip()
        
if __name__ == "__main__":
    game = Game()
    asyncio.run(game.run())
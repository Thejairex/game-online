import pygame as pg

from player import Player
from config import *
from client import Client
import asyncio

import pickle

from config import OPCODES

class Game:
    def __init__(self):
        pg.init()
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
        while self.running:
            await self.events()
            await self.process_queue()
            await self.update()
            self.draw()
            await asyncio.sleep(0.01)  # Evita el uso intensivo de CPU

    async def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                await self.client.disconnect()
                self.running = False

        keys = pg.key.get_pressed()
        if keys[pg.K_ESCAPE]:
            if not self.connected:

                await self.client.send({"operation": OPCODES.CONNECT, "player": (0, 0)})
                asyncio.create_task(self.client.receive(self.queue))  # Pasa la cola a la tarea
                self.connected = True
                
        if self.player is not None:
            self.players[self.player].move(keys)
                
    async def process_queue(self):
        while not self.queue.empty():
            data = await self.queue.get() # retorna el pickle
            # print("""Result: """, result)
            print(data)
            if data["operation"] == OPCODES.CONNECT:
                if self.player is None:
                    self.player = data["player"]
                for player_data in data["players"]:
                    index = player_data["index"]
                    color = player_data["color"]
                    
                    # Asegúrate de que el jugador esté en la lista `self.players`
                    
                    # Actualiza la posición y el color del jugador
                    self.players[index].color = color
                
            elif data["operation"] == OPCODES.MOVE:
                player, x, y = data["player"], data["x"], data["y"]
                self.players[player].x, self.players[player].y = x, y
                

    async def update(self):
        
        if self.player is not None:
            if self.players[self.player].last_action == "move":
                self.players[self.player].last_action = None
                data = {"operation": OPCODES.MOVE, "player": self.player, "x": self.players[self.player].x, "y": self.players[self.player].y}
                await self.client.send(data)
        
        self.clock.tick(self.fps)

    def draw(self):
        self.screen.fill(Colors.BLACK)

        for player in self.players.values():
            player.draw(self.screen)

        pg.display.flip()
        
if __name__ == "__main__":
    game = Game()
    asyncio.run(game.run())
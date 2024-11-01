import pygame as pg

from player import Player
from config import *
from client import Client
import asyncio

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
        self.connected = False
        self.running = True
        self.queue = asyncio.Queue()

    async def run(self):
        while self.running:
            await self.events()
            await self.process_queue()
            self.update()
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
                self.client = Client()
                await self.client.send({"operation": OPCODES.CONNECT, "player": (0, 0)})
                asyncio.create_task(self.client.receive(self.queue))  # Pasa la cola a la tarea
                self.connected = True
                
    async def process_queue(self):
        while not self.queue.empty():
            result = await self.queue.get()
            print("""Result: """, result)        
        
    def update(self):
        pass

    def draw(self):
        self.screen.fill(Colors.BLACK)

        for player in self.players.values():
            player.draw(self.screen)

        pg.display.flip()
        
if __name__ == "__main__":
    game = Game()
    asyncio.run(game.run())
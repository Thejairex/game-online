import pygame as pg
from config import Colors, Config

import os
import pickle

from src.editor.tile import Tile

class Grid:
    def __init__(self):
        self.cols = Config.WIN_WIDTH // Config.TILE_SIZE
        self.rows = Config.WIN_HEIGHT // Config.TILE_SIZE
        self.tiles = [[Tile(col, row) for col in range(self.cols)] for row in range(self.rows)]

    def save_map(self, path):
        """
        Guarda un mapa de tiles en un archivo JSON
        
        args:
            path: la ubicación del archivo JSON
        """
        with open(path, 'wb') as f:
            # Crea un diccionario con los datos del mapa
            map_data = {
                "width": Config.WIN_WIDTH,
                "height": Config.WIN_HEIGHT,
                "tiles": []
            }
            
            # Agrega los datos de los tiles al diccionario
            for row in self.tiles:
                for tile in row:
                    map_data["tiles"].append({
                        "x": tile.x,
                        "y": tile.y,
                        "color": tile.color
                    })
            print(type(map_data))
            # Guarda el diccionario en el archivo
            pickle.dump(map_data, f)

    def load_map(self, path):
        """
        Carga un mapa de tiles desde un archivo JSON
        
        args:
            path: la ubicación del archivo JSON
        """
        if not os.path.exists(path):
            return
        
        # Lee el archivo JSON
        with open(path, 'rb') as f:
            map_data = pickle.load(f)
            # Crea un diccionario con los datos del mapa
            self.cols = map_data["width"] // Config.TILE_SIZE
            self.rows = map_data["height"] // Config.TILE_SIZE
            self.tiles = [[Tile(col, row) for col in range(self.cols)] for row in range(self.rows)]
            
            # Carga los datos de los tiles al diccionario
            for tile_data in map_data["tiles"]:
                self.tiles[tile_data["y"]][tile_data["x"]].color = tile_data["color"]
    
    def handle_click(self, pos):
        x, y = pos
        col = x // Config.TILE_SIZE
        row = y // Config.TILE_SIZE
        self.grid.tiles[row][col].color = Colors.BLUE if self.grid.tiles[row][col].color == Colors.BLACK else Colors.BLACK
        self.grid.tiles[row][col].toggle_solid()
            
        
    def draw(self, surface: pg.Surface):
        """
        Dibuja el mapa de tiles en una superficie
        
        args:
            surface: la superficie en la que se dibuja el mapa
        """
        for row in self.tiles:
            for tile in row:
                tile.draw(surface)
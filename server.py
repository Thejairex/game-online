import socket
import pickle
import threading
import asyncio

from config import OPCODES, Colors

class UDPServer:
    def __init__(self, host='127.0.0.1', port=5555):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.bind((host, port))
        self.server.setblocking(False)  # Importante para usar con asyncio
        self.clients = {}
        self.running = True

    async def handle_client(self):
        print("Server is running...")
        print("ip:", self.server.getsockname()[0], "port:", self.server.getsockname()[1])
        while self.running:
            try:
                # Recibe datos sin bloquear con asyncio
                data, addr = await asyncio.get_event_loop().sock_recvfrom(self.server, 1024)

                if addr not in self.clients:
                    self.clients[addr] = {
                        "addr": addr,
                        "player": None,
                    }
                    print(f"New client: {addr}")

                if not data:
                    continue

                # Intenta deserializar los datos
                try:
                    data = pickle.loads(data)
                    print("Received data:", data)
                except Exception as e:
                    print("Failed to deserialize data:", e)
                    continue  # Ignora y pasa al siguiente ciclo si falla

                # print(data)
                if data.get("operation") == OPCODES.CONNECT:
                    self.clients[addr]["player"] = data["player"]
                    index = list(self.clients.keys()).index(addr)
                    color = [Colors.GREEN, Colors.BLUE, Colors.YELLOW, Colors.PURPLE][index%4]
                    
                    self.clients[addr]["color"] = color
                    # Envía el índice al cliente
                    players_data = [
                        {
                            "index": list(self.clients.keys()).index(client_addr),
                            "color": client_data["color"],
                        }
                        for client_addr, client_data in self.clients.items()
                    ]

                    response = {
                        "operation": OPCODES.CONNECT,
                        "player": index,
                        "players": players_data
                    }
                    
                    # await asyncio.get_event_loop().sock_sendto(self.server, pickle.dumps(response), addr)
                    for client in self.clients:
                        await asyncio.get_event_loop().sock_sendto(self.server, pickle.dumps(response), client)

                elif data.get("operation") == OPCODES.DISCONNECT:
                    print(f"Client disconnected: {addr}")
                    del self.clients[addr]
                
                elif data["operation"] == OPCODES.MOVE:
                    self.clients[addr]["player"] = data["player"]
                    self.clients[addr]["x"] = data["x"]
                    self.clients[addr]["y"] = data["y"]

                    # Enviará los datos al cliente con la ubicación actualizada menos la direccion del cliente
                    response = {
                        "operation": OPCODES.MOVE,
                        "player": data["player"],
                        "x": data["x"],
                        "y": data["y"],
                    }
                    
                    for client in self.clients:
                        if client != addr:
                            await asyncio.get_event_loop().sock_sendto(self.server, pickle.dumps(response), client)
                            
            except BlockingIOError:
                await asyncio.sleep(0.01)
                
            except Exception as e:
                print("Error:", e)

    def close(self):
        self.server.close()

    async def run(self):
        await self.handle_client()

if __name__ == '__main__':
    server = UDPServer()
    asyncio.run(server.run())

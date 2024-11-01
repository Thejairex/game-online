import socket
import pickle
import threading
import asyncio

from config import OPCODES

class UDPServer:
    def __init__(self, host='127.0.0.1', port=5555):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.bind((host, port))
        self.server.setblocking(False)  # Importante para usar con asyncio
        self.clients = {}
        self.running = True

    async def handle_client(self):
        print("Server is running...")
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

                data = pickle.loads(data)

                print(data)
                if data["operation"] == OPCODES.CONNECT:
                    self.clients[addr]["player"] = data["player"]

                    # Envía el índice al cliente
                    index = list(self.clients.keys()).index(addr)
                    await asyncio.get_event_loop().sock_sendto(self.server, pickle.dumps(index), addr)

                elif data["operation"] == OPCODES.DISCONNECT:
                    print(f"Client disconnected: {addr}")
                    del self.clients[addr]
                
            except Exception as e:
                print("Error:", e)

    def close(self):
        self.server.close()

    async def run(self):
        await self.handle_client()

if __name__ == '__main__':
    server = UDPServer()
    asyncio.run(server.run())

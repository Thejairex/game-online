import socket
import pickle
import asyncio

from config import OPCODES

class Client:
    def __init__(self, host='127.0.0.1', port=5555):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client.connect((host, port))
        self.running = True
        self.client.setblocking(False)

    async def send(self, data):
        try:
            data = pickle.dumps(data)
            await asyncio.get_event_loop().sock_sendall(self.client, data)
        except Exception as e:
            print("Error en envío:", e)
            self.running = False
            self.close()

    async def disconnect(self):
        data = {
            "operation": OPCODES.DISCONNECT,
        }
        await self.send(data  # Asegúrate de enviar la desconexión
        self.close()

    async def receive(self, queue):  # Acepta la cola como argumento
        while self.running:
            try:
                data = self.client.recv(1024)
                if data:
                    data = pickle.loads(data)
                    await queue.put(data)  # Poner el resultado en la cola
            except BlockingIOError:
                await asyncio.sleep(0.01)
            except Exception as e:
                print(e)
                break

    def close(self):
        self.client.close()
        self.running = False
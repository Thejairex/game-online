import socket
import pickle
import asyncio
import argparse
import os

from config import OPCODES, Colors


class UDPServer:
    """
    Class to handle the server UDP socket and clients connections.

    args:
        host (str): IP address of the server
        port (int): Port of the server
    """

    def __init__(self, host='0.0.0.0', port=None):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Get the port from the environment variable
        self.port = port if port else int(os.environ.get('PORT', 5555))

        self.server.bind((host, self.port))
        self.clients = {}
        self.running = True
        self.server.setblocking(False)  # set the socket to non-blocking mode

    async def handle_client(self):
        """
        Controls the clients connections and sends data to them.
        """
        print("Server is running...")
        print("ip:", self.server.getsockname()[
              0], "port:", self.server.getsockname()[1])
        while self.running:
            try:
                # receive data from the client with pickle and asyncio
                data, addr = await asyncio.get_event_loop().sock_recvfrom(self.server, 1024)

                # Checks if the client is new
                if addr not in self.clients:
                    self.clients[addr] = {
                        "addr": addr,
                        "player": None,
                    }
                    print(f"New client: {addr}")

                if not data:
                    continue

                # Try to decode the data
                try:
                    data = pickle.loads(data)
                except Exception as e:
                    continue  # Ignore invalid data

                # Process the data starting with the operation
                if data.get("operation") == OPCODES.CONNECT:
                    """Connects the client to the server and sends the player index and color to the client."""

                    # Set the player index and color for the client
                    self.clients[addr]["player"] = data["player"]
                    index = list(self.clients.keys()).index(addr)
                    color = [Colors.GREEN, Colors.BLUE,
                             Colors.YELLOW, Colors.PURPLE][index % 4]
                    self.clients[addr]["color"] = color

                    # Send the player index and color to the client and all the other clients
                    players_data = [
                        {
                            "index": list(self.clients.keys()).index(client_addr),
                            "color": client_data["color"],
                        }
                        for client_addr, client_data in self.clients.items()
                    ]

                    # Generate the response with the player index and color
                    response = {
                        "operation": OPCODES.CONNECT,
                        "player": index,
                        "players": players_data
                    }

                    # Send the response to all the clients
                    for client in self.clients:
                        await asyncio.get_event_loop().sock_sendto(self.server, pickle.dumps(response), client)

                elif data.get("operation") == OPCODES.DISCONNECT:
                    """Disconnects the client from the server."""
                    print(f"Client disconnected: {addr}")
                    del self.clients[addr]

                elif data["operation"] == OPCODES.MOVE:
                    """Updates the player location."""
                    # Get the player index and location
                    self.clients[addr]["player"] = data["player"]
                    self.clients[addr]["x"] = data["x"]
                    self.clients[addr]["y"] = data["y"]

                    # Send the player location to all the other clients
                    response = {
                        "operation": OPCODES.MOVE,
                        "player": data["player"],
                        "x": data["x"],
                        "y": data["y"],
                    }

                    # Send the response to all the clients except the sender
                    for client in self.clients:
                        if client != addr:
                            await asyncio.get_event_loop().sock_sendto(self.server, pickle.dumps(response), client)

            # If there is no data, sleep for 0.01 seconds
            except BlockingIOError:
                await asyncio.sleep(0.01)

            # If there is an error, print it

            except Exception as e:
                print("Error:", e)

    def close(self):
        """
        Closes the server socket.
        """
        self.server.close()
        self.running = False

    async def run(self):
        """
        Runs the server.
        """
        await self.handle_client()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Example: python server.py --host 127.0.0.1 --port 5555")
    parser.add_argument('--host', type=str,
                        default='127.0.0.1', help="Host IP the server")
    parser.add_argument('--port', type=int, default=5555,
                        help="Port of the server")
    args = parser.parse_args()

    # Start the server
    server = UDPServer(args.host, args.port)
    asyncio.run(server.run())

import socket
import pickle
import asyncio

from config import OPCODES

class Client:
    """
    Class to connect and send data to the server (UDP)
    Using asyncio for non-blocking operations
    
    args:
        host (str): IP address of the server
        port (int): Port of the server
    """
    def __init__(self, host='0.0.0.0', port=5555):
        """
        Initializes the client socket and starts the connection
        """
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client.connect((host, port))
        self.running = True
        # set the socket to non-blocking mode
        self.client.setblocking(False)

    async def send(self, data):
        """
        Sends data to the server (UDP) with pickle encoding.
        If an error occurs, the connection is closed.
        
        args:
            data (dict): Data to send
        """
        try:
            data = pickle.dumps(data)

            # Sends the data to the server
            await asyncio.get_event_loop().sock_sendall(self.client, data)
            
        except Exception as e:
            print("Error in sending (code 1):", e)
            self.running = False
            self.close()

    async def disconnect(self):
        """
        Disconnects from the server (UDP) and closes the connection
        """
        # send the disconnect message
        data = {
            "operation": OPCODES.DISCONNECT,
        }
        await self.send(data) 
        
        # close the connection
        self.close()

    async def receive(self, queue: asyncio.Queue):
        """
        Receives data from the server (UDP) with pickle decoding and puts it in the queue.
        If an error occurs, the connection is closed.
        
        args:
            queue (asyncio.Queue): Queue to put the data in
        """
        
        while self.running:
            try:
                # Receives data from the server
                data = await asyncio.get_event_loop().sock_recv(self.client, 1024)
                
                # Checks if data was received
                if data:
                    data = pickle.loads(data)
                    # Puts the data in the queue
                    await queue.put(data)  
            
            # Sleeps if no data was received      
            except BlockingIOError:
                await asyncio.sleep(0.01)
                
            except ConnectionResetError:
                print("Connection reset by server (code 2)")
                self.running = False
                self.close()
                
            except Exception as e:
                print("Error en envío (code 3):", e)
                self.running = False
                self.close()

    def close(self):
        """
        Closes the connection to the server
        """
        self.client.close()
        print("Connection closed...")
        self.running = False
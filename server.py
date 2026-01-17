import websockets
import datetime
import asyncio

class Server:
    def __init__(self, local_host = "0.0.0.0", port = 8080):
        self.local_host = local_host
        self.port = port
        self.clients = {}

    async def client_messages(self, websocket):
        try:
            now = datetime.datetime.now().strftime("%d/%m%Y %H:%M")
            async for message in websocket:
                print(f"{websocket.remote_address} - {now}: {message}")
        except websocket.exceptions.ConnectionClosed:
            print("Connection was lost")
    
    async def server_messages(self, websocket):
            try:
                while True:
                    message = websocket.to_thread(input, f"{self.local_host}")
                    now = datetime.datetime.now().strftime("%d/%m%Y %H:%M")
                    await websocket.send(f"{now}: {message}")
            except websocket.exceptions.ConnectionClosed:
                print("Connection was lost")

    async def handle_connections(self, websocket, path):
        print(f"new connection from {websocket.remote_address}\n Type here to send a message...")
        try:
            await asyncio.gather(
                self.server_messages(websocket), 
                self.client_messages(websocket)
                )
        except Exception as e:
            print(e)
    
    async def server_start(self):
        async with websockets.serve(self.handle_connections, self.local_host, self.port):
            print(f"Server has started on {self.local_host}:{self.port}")
            await asyncio.Future()

if __name__ == "__main__":
    server = Server()
    asyncio.run(server.server_start())

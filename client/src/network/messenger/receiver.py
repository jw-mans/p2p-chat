from ...utils import log
from ...account import Account
from ...models import Message, Peer

import asyncio
from typing import Callable, Awaitable

class Receiver:

    def __init__(self, username: str, host: str, port: int, callback: (Callable[[str], Awaitable])):
        self.username = username
        self.host = host
        self.port = port
        self.callback = callback
        self.server = None

    async def handle_client(self, reader: asyncio.StreamReader,
                            writer: asyncio.StreamWriter
                            ):
        addr = writer.get_extra_info('peername') # getting (<host>: str, <port>: int) tuple
        try:
            data = await reader.read(1024)
            message = data.decode()
            log.info(f"Received message from {addr}: {message}")
            await self.callback(Message( # send to callback
                sender=Peer(username="Unknown", host=addr[0], port=addr[1]),
                receiver=self,
                data=message
                ))
        except Exception as ex:
            log.error(f"Error handling client {addr}: {ex}")
        finally:
            writer.close()
            await writer.wait_closed()
            log.debug(f"Connection closed {addr}")

    async def start(self):
        """
        TCP server launch for listening incoming messages
        """
        self.server = await asyncio.start_server(self.handle_client, self.host, self.port)
        async with self.server:
            await self.server.serve_forever()
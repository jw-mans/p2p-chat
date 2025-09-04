import asyncio
from ..core.logging import log

log.basicConfig(level=log.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


async def tcp_server(host: str, port: int):
    async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        addr = writer.get_extra_info("peername")
        log.info(f"New connection from {addr}")

        try:
            data = await reader.read(1000)
            message = data.decode().strip()
            if message:
                log.info(f"Message received from {addr}: {message}")
            else:
                log.warning(f"Empty message received from {addr}")
        except Exception as e:
            log.exception(f"Error handling client {addr}: {e}")
        finally:
            writer.close()
            await writer.wait_closed()
            log.info(f"Connection closed {addr}")

    server = await asyncio.start_server(handle_client, host, port)
    addr = ", ".join(str(sock.getsockname()) for sock in server.sockets)
    log.info(f"Server listening on {addr}")

    async with server:
        await server.serve_forever()

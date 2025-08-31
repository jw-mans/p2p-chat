import asyncio
import logging as log

log.basicConfig(level=log.INFO)

async def send(peer_host: str, peer_port: int, msg: str):
    try:
        _, writer = await asyncio.open_connection(peer_host, peer_port)
        log.debug(f"Connection opened ({peer_host}:{peer_port})")

        writer.write(msg.encode())
        await writer.drain()
        log.info(f"Message sent ({peer_host}:{peer_port})")
        log.debug(f"Sent content: {msg}")

        writer.close()
        await writer.wait_closed()
        log.debug(f"Connection closed ({peer_host}:{peer_port})")

    except (ConnectionRefusedError, TimeoutError) as e:
        log.error(f"Failed to connect to {peer_host}:{peer_port} ({type(e).__name__}): {e}")
    except Exception as e:
        log.exception(f"Unexpected error while sending message to {peer_host}:{peer_port}")

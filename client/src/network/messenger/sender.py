import asyncio
import requests

from ...utils.logging import log
from ...models import Message
from ...config import DISCOVERY_URL

class Sender:
    @staticmethod
    async def send(message: Message):
        receiver = message.receiver
        content = message.data

        try: # try to open straight P2P connection
            _, writer = await asyncio.open_connection(receiver.host, receiver.port)
            log.debug(f"Connection opened ({receiver.socket_string})")

            writer.write(content.encode())
            await writer.drain()
            log.info(f"Message sent directly ({receiver.socket_string})")

            writer.close()
            await writer.wait_closed()
            log.debug(f"Connection closed ({receiver.socket_string})")

        except (ConnectionRefusedError, TimeoutError) as ex:
            log.warning(f"P2P send failed ({receiver.socket_string}). \nFallback to server: {ex}")


            async def fallback(): # send fallback to discovery server
                try:
                    url = f"{DISCOVERY_URL}/send/"
                    response = requests.post(url, json=message.to_json())

                    if response.status_code <= 200:
                        response_data = response.json()
                        log.info(f"Message sent via server to {receiver.to_string()}")
                        log.debug(f"Details: {response_data.get('detail')}")

                    else:
                        log.error(f"Server returned error {response.status_code}: {response.text}")

                except requests.RequestException as re: 
                    log.error(f"Server fallback failed for {receiver.to_string()}: {re}")
            
            fallback()

            
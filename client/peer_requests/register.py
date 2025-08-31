from core.config import DISCOVERY_URL
import httpx
import logging as log

log.basicConfig(level=log.INFO)

async def register(username: str, host: str, port: int):
    async with httpx.AsyncClient() as client:
        peer_data = {"username": username, "host": host, "port": port}
        try:
            response = await client.post(f"{DISCOVERY_URL}/register/", json=peer_data)

            if response.status_code == 200:
                data = response.json()
                log.info(f"Success in POST[/register] ({username}:{port})")
                print("Success!")
                return data
            else:
                log.warning(f"Failed in POST[/register] ({username}:{port}) ")
                log.debug(f"(Status {response.status_code}): {response.text}")
                return None

        except httpx.RequestError as re:
            log.error(f"Failed in POST[/register] ({username}:{port})")
            log.debug(f"{re}")
            return None

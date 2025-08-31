from core.config import DISCOVERY_URL
import httpx
import logging as log

async def available_peers():
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{DISCOVERY_URL}/available")

            if response.status_code == 200:
                peers = response.json()
                log.info("Success in GET[/available]")
                print("Available peers:", str('\n'.join([peer_.username for peer_ in peers])))
                return peers
            
            else:
                log.warning("Failed in GET[/available]")
                log.debug(f"Status {response.status_code}: {response.text}")
                return []
            
        except httpx.RequestError as re:
            log.error("Failed in GET[/available]")
            log.debug(f"{re}")
            return []
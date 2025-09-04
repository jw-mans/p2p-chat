from ...config import DISCOVERY_URL
from ...models.peer import Peer
from ...core.logging import log
import httpx

async def available():
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{DISCOVERY_URL}/available")

            if response.status_code == 200:
                peers = response.json()
                log.info("Success in GET[/available]")
                log.info("Available peers:\n" + '\n'.join([peer_["username"] for peer_ in peers]))
                return peers
            
            else:
                log.warning("Failed in GET[/available]")
                log.debug(f"Status {response.status_code}: {response.text}")
                return []
            
        except httpx.RequestError as re:
            log.error("Failed in GET[/available]")
            log.debug(f"{re}")
            return []

async def register(username_or_peer, host=None, port=None):
    username = None
    if isinstance(username_or_peer, Peer):
        username, host, port = \
            username_or_peer.username, \
            username_or_peer.host, \
            username_or_peer.port
    else:
        username = username_or_peer
        if host is None or port is None:
            log.error(f"Failed in POST[/register] ({host}: {port})")
            log.debug("Host and post must be specified here")
            return None
        
    async with httpx.AsyncClient() as client:
        peer_data = {"username": username, "host": host, "port": port}
        try:
            response = await client.post(f"{DISCOVERY_URL}/register/", json=peer_data)

            if response.status_code == 200:
                data = response.json()
                log.info(f"Success in POST[/register] ({host}:{port})")
                return data
            else:
                log.warning(f"Failed in POST[/register] ({host}:{port}) ")
                log.debug(f"(Status {response.status_code}): {response.text}")
                return None

        except httpx.RequestError as re:
            log.error(f"Failed in POST[/register] ({host}:{port})")
            log.debug(f"{re}")
            return None
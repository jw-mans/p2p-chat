from ..config import DISCOVERY_URL
from ..models.peer import Peer
from ..utils.logging import log
import httpx

async def available():
    """
    Retrieve the list of available peers from the discovery server.
    
    Makes an asynchronous GET request to the discovery service to fetch
    the current list of registered peers that are available for messaging.
    
    Returns:
        list: List of peer dictionaries on success, empty list on failure
        
    Raises:
        httpx.RequestError: If network request fails (handled internally)
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{DISCOVERY_URL}/available")

            if response.status_code <= 299:
                peers = response.json()
                log.info("Success in GET[/available]")
                log.info("Available peers:\n" + '\n'.join([peer_["username"] for peer_ in peers]))
                return peers
            
            else:
                log.error("Failed in GET[/available]")
                log.debug(f"Status {response.status_code}: {response.text}")
                return []
            
        except httpx.RequestError as re:
            log.error("Failed in GET[/available]")
            log.debug(f"{re}")
            return []

async def register(peer: Peer):
    """
    Register a peer with the discovery server.
    
    Registers a user account or peer information with the discovery service
    to make it available to other peers on the network.
    
    Args:
        username_or_peer: Either a Peer object or username string
        host: IP address or hostname (required if username is string)
        port: Port number (required if username is string)
        
    Returns:
        dict: Registration response data on success, None on failure
        
    Raises:
        ValueError: If host/port are missing when username is provided as string
        httpx.RequestError: If network request fails (handled internally)
    """
    
    async with httpx.AsyncClient() as client:
        peer_data = peer.to_json()
        try:
            response = await client.post(f"{DISCOVERY_URL}/register/", json=peer_data)

            if response.status_code <= 299:
                data = response.json()
                log.info(f"Success in POST[/register] ({peer.to_string()})")
                log.debug(f"{data}")
                return
            else:
                log.warning(f"Failed in POST[/register] ({peer.to_string()}) ")
                log.debug(f"(Status {response.status_code}): {response.text}")
                return None

        except httpx.RequestError as re:
            log.error(f"Failed in POST[/register] ({peer.to_string()})")
            log.debug(f"{re}")
            return None
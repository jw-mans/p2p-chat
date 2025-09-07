from pydantic import BaseModel, Field

class Peer(BaseModel):
    """
    Represents a network peer with connection information.
    
    Attributes:
        username: Unique identifier/username of the peer
        host: IP address or hostname where the peer is reachable
        port: Network port number for connecting to the peer (1024-65535)
    
    Raises:
        ValidationError: If any field fails validation
    """
    username: str = Field(..., description="Unique identifier for the peer")
    host: str = Field(..., description="IP address or hostname")
    port: int = Field(..., ge=1024, le=65535, description="Valid port number range: 1024-65535")

    @classmethod
    def from_dict(cls, data: dict) -> "Peer":
        return cls.model_validate(data)

    def to_json(self) -> dict:
        """
        Returns:
            dict: a dict (JSON-compatible) representation of Peer instance
        """
        return self.model_dump()
    
    @property
    def socket_string(self) -> str:
        """
        Returns:
            str: a string "host:port" representation of Peers socket
        """
        return f"{self.host}:{self.port}"
    
    def to_string(self) -> str:
        """
        Returns:
            str: a string "username (host:port)" representation of Peer info
        """
        return f"{self.username} ({self.socket_string})"
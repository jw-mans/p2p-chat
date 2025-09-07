from .peer import Peer
from pydantic import BaseModel, Field

class Message(BaseModel):
    """
    Represents a message sent from one peer to another.
    
    Attributes:
        sender (Peer): The peer who sends the message
        receiver (Peer): The peer who receives the message
        data (str): The textual content of the message
    """
    sender: Peer = Field(..., description="The peer sending the message")
    receiver: Peer = Field(..., description="The peer receiving the message")
    data: str = Field(..., description="The content of the message")

    def to_json(self) -> dict:
        """
        Returns:
            dict: a dict (JSON-compatible) representation of Peer instance
        """
        return self.model_dump()
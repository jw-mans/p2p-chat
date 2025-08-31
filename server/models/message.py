from pydantic import BaseModel
from models.peer import Peer

class Message(BaseModel):
    sender: Peer
    receiver: Peer
    content: str

    def dict(self):
        return {
            "sender": self.sender, 
            "receiver": self.receiver, 
            "content": self.content
            }
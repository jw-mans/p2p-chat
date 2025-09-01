from pydantic import BaseModel

class Peer(BaseModel):
    username: str
    host: str
    port: int
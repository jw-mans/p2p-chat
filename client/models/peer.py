from pydantic import BaseModel
from sqlalchemy import Column, Integer, String

class Peer(BaseModel):
    username: str
    host: str
    port: int

    def __init__(self, username, host, port):
        self.username = username
        self.host = host
        self.port = port
    
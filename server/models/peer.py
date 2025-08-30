from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from database.database import Base

class PeerDB(Base):
    __tablename__ = "peers"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    host = Column(String, nullable=False)
    port = Column(Integer, nullable=False)

class Peer(BaseModel):
    username: str
    host: str
    port: int

    def to_db(self) -> PeerDB:
        return PeerDB (
            username=self.username,
            host=self.host,
            port=self.port
        )

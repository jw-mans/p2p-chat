import uvicorn
from fastapi import FastAPI
from core.config import settings
from database.database import Base, engine
from routers import peers

Base.metadata.create_all(bind=engine)

app = FastAPI(title="P2P Discovery Server")
app.include_router(peers.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.API_HOST, port=settings.API_PORT, reload=True)

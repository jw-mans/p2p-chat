from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.peer import Peer, PeerDB
from database.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register/")
def register(peer: Peer, db: Session = Depends(get_db)):
    db_peer = peer.to_db()
    db.add(db_peer)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")
    db.refresh(db_peer)
    return db_peer

@router.get("/available")
def available_peers(db: Session = Depends(get_db)):
    return db.query(PeerDB).all()

@router.delete("/unregister/{username}")
def unregister(username: str, db: Session = Depends(get_db)):
    peer = db.query(PeerDB).filter(PeerDB.username == username).first()
    if not peer:
        raise HTTPException(status_code=404, detail="Peer not found!")
    db.delete(peer)
    db.commit()
    return {"detail": f"Peer {username} unregistered"}

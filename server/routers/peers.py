import requests
import logging as log
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from models.peer import Peer, PeerDB
from models.message import Message
from database.database import SessionLocal

router = APIRouter()
log.basicConfig(level=log.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register/")
def register(peer: Peer, db: Session = Depends(get_db)):
    log.info(f"Registering new peer: {peer.username}@{peer.host}:{peer.port}")
    db_peer = peer.to_db()
    db.add(db_peer)
    try:
        db.commit()
        db.refresh(db_peer)
        log.info(f"Peer registered successfully: {peer.username}")
        return db_peer
    except Exception as e:
        db.rollback()
        log.error(f"Failed to register peer {peer.username}: {e}")
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")


@router.get("/available/", response_model=List[Peer])
def available_peers(db: Session = Depends(get_db)):
    peers = db.query(PeerDB).all()
    log.info(f"Available peers requested. Found: {len(peers)}")
    return peers


@router.post("/send/")
def send_message(message: Message, db: Session = Depends(get_db)):
    log.info(f"Sending message from {message.sender.username} "
             f"to {message.receiver.username}")

    recvr_db = db.query(PeerDB).filter(PeerDB.username == message.receiver.username).first()
    if not recvr_db:
        log.warning(f"Receiver {message.receiver.username} not found")
        raise HTTPException(status_code=404, detail="Receiver not found")

    url = f"http://{recvr_db.host}:{recvr_db.port}/receive/"
    try:
        response = requests.post(url, json=message.dict())
        response.raise_for_status()
        log.info(f"Message delivered to {recvr_db.username}@{recvr_db.host}:{recvr_db.port}")
    except requests.RequestException as re:
        log.error(f"Failed to send message to {recvr_db.username}: {re}")
        raise HTTPException(status_code=400, detail=f"Failed to send message: {str(re)}")

    return {"detail": "Success: message sent"}


@router.delete("/unregister/{username}")
def unregister(username: str, db: Session = Depends(get_db)):
    log.info(f"Unregister request for peer: {username}")
    peer = db.query(PeerDB).filter(PeerDB.username == username).first()
    if not peer:
        log.warning(f"Peer {username} not found for unregister")
        raise HTTPException(status_code=404, detail="Peer not found")

    db.delete(peer)
    db.commit()
    log.info(f"Peer {username} unregistered successfully")
    return {"detail": f"Peer {username} unregistered"}

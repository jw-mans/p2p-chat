import json
import os
from models.peer import Peer
from core.config import ACCOUNT_FILE

class Account(Peer):
    def __init__(self, peer: Peer, save_flag=True):
        super().__init__(**peer.__dict__)
        if save_flag:
            with open(ACCOUNT_FILE, "w") as f:
                json.dump(self.__dict__, f, indent=4)
    
    @classmethod 
    def load(cls):
        if os.path.exists(ACCOUNT_FILE):
            with open(ACCOUNT_FILE, "r") as f:
                data = json.load(f)
                return cls(Peer(**data), save_flag=False)
        return None
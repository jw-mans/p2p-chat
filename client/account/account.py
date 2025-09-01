import json
import os
import logging as log
from ..models.peer import Peer
from ..core.config import ACCOUNT_FILE


class Account(Peer):
    @classmethod
    def create(cls, username: str, host: str, port: int):
        acc = cls(username=username, host=host, port=port)
        with open(ACCOUNT_FILE, "w") as f:
            json.dump(acc.model_dump(), f, indent=4)
        return acc

    @classmethod
    def load(cls):
        if os.path.exists(ACCOUNT_FILE):
            try:
                with open(ACCOUNT_FILE, "r") as f:
                    data = json.load(f)
                    return cls(**data)
            except (json.JSONDecodeError, TypeError):
                return None
        return None

    @classmethod
    def auth(cls):
        acc = cls.load()
        if not acc:
            username = input("Enter your username: ")
            host = "127.0.0.1"
            port = int(input("Enter your port: "))
            acc = cls.create(username=username, host=host, port=port)
            log.info("Account created")
        else:
            log.info(f"Loaded account: {acc.username} ({acc.host}:{acc.port})")
        return acc

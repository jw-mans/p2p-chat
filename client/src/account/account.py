import json
import os
from ..core.logging import log
from ..models.peer import Peer
from ..config import ACCOUNT_FILE
from PySide6.QtWidgets import QApplication
import asyncio

class Account(Peer):
    @classmethod
    def _read_file(cls):
        if os.path.exists(ACCOUNT_FILE):
            try:
                with open(ACCOUNT_FILE, "r") as f:
                    data = json.load(f)
                    return data if isinstance(data, list) else []
            except (json.JSONDecodeError, TypeError):
                return []
        return []

    @classmethod
    def _write_file(cls, accounts_list):
        with open(ACCOUNT_FILE, "w") as f:
            json.dump(accounts_list, f, indent=4)

    @classmethod
    def create(cls, username: str, host: str, port: int):
        acc = cls(username=username, host=host, port=port)
        accounts = cls._read_file()
        if not any(a["username"] == username for a in accounts):
            accounts.append(acc.model_dump())
            cls._write_file(accounts)
            log.info(f"Account '{username}' created")
        else:
            log.info(f"Account '{username}' already exists")
        return acc

    @classmethod
    def load(cls, username=None):
        accounts = cls._read_file()
        if not accounts:
            return None
        if username:
            acc_data = next((a for a in accounts if a["username"] == username), None)
            return cls(**acc_data) if acc_data else None
        return cls(**accounts[0])

    @classmethod
    async def auth(cls):
        app = QApplication.instance()
        if app is None:
            app = QApplication([])

        from ..gui.widgets.account_selector import AccountSelector

        selector = AccountSelector()
        loop = asyncio.get_running_loop()
        future = loop.create_future()

        def finish():
            if selector._selected_ is not None and not future.done():
                future.set_result(selector._selected_)

        selector.select_btn.clicked.connect(finish)
        selector.create_btn.clicked.connect(finish)

        selector.show()
        selected_acc = await future
        selector.close()
        return selected_acc


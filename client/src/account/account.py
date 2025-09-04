import json
import os
from ..core.logging import log
from ..models.peer import Peer
from ..config import ACCOUNT_FILE
from PySide6.QtWidgets import QApplication
from qasync import QEventLoop
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

        #app_created = False
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
            #app_created = True

        loop = QEventLoop(app)
        asyncio.set_event_loop(loop)

        from ..gui.widgets.account_selector import AccountSelector # to avoid the circular import

        selector = AccountSelector()
        selector.show()

        # wait while user does not select or create account

        async def wait_selection():
            while selector._selected_ is None:
                await asyncio.sleep(0.1)
            return selector._selected_

        with loop:
            selected_account = loop.run_until_complete(wait_selection())

        return selected_account

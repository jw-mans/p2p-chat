from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QInputDialog
)
from ...account.account import Account
from ...core.logging import log

from .app_widgets import (
    ChatAsyncButton, ChatAsyncListWidget,
    ChatAsyncLabel
)

class AccountSelector(QWidget):

    def select_(self):
        selected = self.list_widget.currentRow()
        if selected < 0: return
        acc_data = self.accounts[selected]
        self._selected_ = Account(**acc_data)
        log.info(f"Selected account: {self._selected_.username}")

    def create_(self):
        username, ok = QInputDialog.getText(self, "New account", "Enter username: ")
        if not ok or not username.strip(): return

        host = "127.0.0.1"
        port, ok = QInputDialog.getInt(self, "New account", "Enter port: ", minValue=1024, maxValue=65535)
        if not ok: return

        self._selected_ = Account.create(username.strip(), host, port)
        log.info(f"Created new account: {self._selected_.username} ({self._selected_.host}:{self._selected_.port})")

    def __init__(self):
        super().__init__()
        self._selected_ = None
        self.accounts = Account._read_file()

        self.setWindowTitle("Select Account")
        self.setGeometry(300, 300, 300, 300)

        layout = QVBoxLayout()
        layout.addWidget(ChatAsyncLabel("Select an account:"))

        self.list_widget = ChatAsyncListWidget()
        for ac in self.accounts:
            self.list_widget.addItem(f"{ac['username']} ({ac['host']}:{ac['port']})")
        layout.addWidget(self.list_widget)

        self.select_btn = ChatAsyncButton("Select account", self.select_, layout=layout)
        self.create_btn = ChatAsyncButton("Create new account", self.create_, layout=layout)
        self.setLayout(layout)


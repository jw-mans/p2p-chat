from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QListWidget,
    QPushButton, QLineEdit, QInputDialog
)
from ...account.account import Account
from ...core.logging import log

class AccountSelector(QWidget):

    def select_(self):
        selected = self.list_widget.currentRow()
        if selected < 0: return

        acc_data = self.accounts[selected]
        self._selected_ = Account(**acc_data)
        log.info(f"Selected account: {self._selected_.username}")
        self.close()

    def create_(self):
        username, ok = QInputDialog.getText(self, "New account", "Enter username: ")
        if not ok or not username.strip(): return

        host = "127.0.0.1"

        port, ok = QInputDialog.getInt(self, "New account", "Enter port: ", minValue=1024, maxValue=65535)
        if not ok: return

        self._selected_ = Account.create(username.strip(), host, port)
        log.info(f"Created new account: {self._selected_.username} ({self._selected_.host}:{self._selected_.port})")
        self.close()


    def __init__(self):
        super().__init__()
        self._selected_ = None
        self.accounts = Account._read_file()

        self.setWindowTitle("Select Account")
        self.setGeometry(300, 300, 300, 300)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Select an account:"))

        self.list_widget = QListWidget()
        for ac in self.accounts:
            self.list_widget.addItem(f"{ac['username']} ({ac['host']}:{ac['port']})")
        layout.addWidget(self.list_widget)

        self.select_btn = QPushButton("Select")
        self.select_btn.clicked.connect(self.select_)
        layout.addWidget(self.select_btn)

        self.new_acc_btn = QPushButton("Create new account")
        self.new_acc_btn.clicked.connect(self.create_)
        layout.addWidget(self.new_acc_btn)

        self.setLayout(layout)


from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QLabel, QPushButton, QListWidget, 
    QLineEdit, QTextEdit
)
from PySide6.QtCore import QTimer
from qasync import QEventLoop

import sys
import asyncio

from ..account.account import Account
from ..network import available, register, send
from ..core.logging import log

class ClientGUI(QWidget):
    async def available_peers_(self):
        self.peers = await available() or []
        self.peer_list.clear()
        for p_ in self.peers:
            if p_["username"] != self.acc.username:
                self.peer_list.addItem(
                    f'{p_["username"]} ({p_["host"]}:{p_["port"]})'
                    )
                
    # some tasks

    async def register_(self):
        await register(self.acc)

    async def send_(self):
        selected_items = self.peer_list.selectedItems()
        if not selected_items:
            self.chat_area.append("Select a peer to send the message.")
            return
        peer_text = selected_items[0].text()
        username = peer_text.split(" ")[0]
        peer = next((p for p in self.peers if p["username"] == username), None)
        if not peer:
            self.chat_area.append("Selected peer not found.")
            return
        msg = self.msg_input.text().strip()
        if not msg:
            return
        await send(peer["host"], peer["port"], f"{self.acc.username}: {msg}")
        self.chat_area.append(f"You -> {username}: {msg}")
        self.msg_input.clear()

    # GUI create
    def __init__(self, account: Account):
        super().__init__()
        self.acc = account
        self.peers = []

        # window set
        self.setWindowTitle("P2P Chat (by jwmans)")
        self.setGeometry(200, 200, 500, 400)

        layout = QVBoxLayout()

        # acc info
        self.account_label = QLabel(f"Username: {self.acc.username} | {self.acc.host}:{self.acc.port}")
        layout.addWidget(self.account_label)
        
        # refresh peers button
        self.refresh_btn = QPushButton("Refresh peers")
        self.refresh_btn.clicked.connect(
            lambda: asyncio.create_task(self.available_peers_())
        )
        layout.addWidget(self.refresh_btn)

        # peer list
        self.peer_list = QListWidget()
        layout.addWidget(self.peer_list)

        # message input
        self.msg_input = QLineEdit()
        self.msg_input.setPlaceholderText("Type your message here...")
        layout.addWidget(self.msg_input)

        # send button
        self.send_btn = QPushButton("Send message")
        self.send_btn.clicked.connect(
            lambda: asyncio.create_task(self.send_())
        )
        layout.addWidget(self.send_btn)

        # chat area
        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)
        layout.addWidget(self.chat_area)
        
        self.setLayout(layout)
"""
The error was in: 

if __name__ == "__main__":

    async def build_gui():
        acc = await Account.auth()
        gui = ClientGUI(acc)
        gui.show()
        await gui.register_()
        await gui.available_peers_()

    app = QApplication(sys.argv)

    loop = QEventLoop(app)
   
    with loop:
        loop.create_task(build_gui())
        loop.run_forever()
"""
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout
)
from qasync import QEventLoop

import sys
import asyncio

from ..account.account import Account
from ..network import available, register, send
from ..core.logging import log
from .widgets.app_widgets import (
    ChatAsyncButton, ChatAsyncTextEdit,
    ChatAsyncListWidget, ChatAsyncLabel,
    ChatAsyncLineEdit
)

class ClientGUI(QWidget):
    async def available_(self):
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
        self.account_label = ChatAsyncLabel(f"Username: {self.acc.username} | {self.acc.host}:{self.acc.port}")
        layout.addWidget(self.account_label)
        
        # refresh peers button
        self.refresh_btn = ChatAsyncButton("Refresh peers", 
            lambda: asyncio.create_task(self.available_()), 
            layout=layout)

        # peer list
        self.peer_list = ChatAsyncListWidget()
        layout.addWidget(self.peer_list)

        # message input
        self.msg_input = ChatAsyncLineEdit()
        self.msg_input.setPlaceholderText("Type your message here...")
        layout.addWidget(self.msg_input)

        # send button
        self.send_btn = ChatAsyncButton("Send message", 
            lambda: asyncio.create_task(self.send_()), 
            layout=layout)

        # chat area
        self.chat_area = ChatAsyncTextEdit()
        self.chat_area.setReadOnly(True)
        layout.addWidget(self.chat_area)
        
        self.setLayout(layout)

if __name__ == "__main__":

    async def build_gui():
        acc = await Account.auth()
        gui = ClientGUI(acc)
        gui.show()
        await gui.register_()
        await gui.available_()

    app = QApplication(sys.argv)

    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
   
    with loop:
        loop.create_task(build_gui())
        loop.run_forever()

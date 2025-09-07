from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout
)
from PySide6.QtGui import QCloseEvent
from qasync import QEventLoop

import sys
import asyncio

from ..models import Peer, Message
from ..account import Account
from .scenes import auth
from ..network import available, register, Sender, Receiver
from ..utils.logging import log
from .widgets import (
    ChatAsyncButton, ChatAsyncTextEdit,
    ChatAsyncListWidget, ChatAsyncLabel,
    ChatAsyncLineEdit
)

class ClientGUI(QWidget):
    """
    Main GUI window for the P2P chat client application.
    
    Provides a graphical interface for peer-to-peer messaging including:
    - Account information display
    - Peer list management
    - Message sending and receiving
    - Chat history display
    
    Attributes:
        acc (Account): The authenticated user account
        peers (list): List of available peers for messaging
        account_label (ChatAsyncLabel): Displays account information
        refresh_btn (ChatAsyncButton): Button to refresh peer list
        peer_list (ChatAsyncListWidget): List widget showing available peers
        msg_input (ChatAsyncLineEdit): Input field for typing messages
        send_btn (ChatAsyncButton): Button to send messages
        chat_area (ChatAsyncTextEdit): Read-only area displaying chat history
    """
    
    async def available_(self):
        """
        Refresh and display the list of available peers.
        
        Fetches the list of available peers from the network and updates
        the peer list widget. Excludes the current user from the list.
        
        Returns:
            None: Updates the UI directly
        """
        self.peers = await available() or []
        self.peer_list.clear()
        for p_ in self.peers:
            if p_["username"] != self.acc.username:
                self.peer_list.addItem(
                        f"{p_['username']}@{p_['host']}:{p_['port']}"
                    )

    async def register_(self):
        """
        Register the current account on the network.
        
        Makes the current user account available to other peers
        by registering it with the network service.

        Returns:
        None: sends request only
        """
        await register(self.acc)

    async def send_(self):
        """
        Send a message to the selected peer.
        
        Validates peer selection and message content, then sends the message
        via network. Updates the chat area with sent message confirmation.
        
        Returns:
            None: Updates the UI and clears input on successful send
        """
        # check if there is at least one peer
        selected_items = self.peer_list.selectedItems()
        if not selected_items:
            self.chat_area.append("Select a peer to send the message.")
            return
        
        peer_text = selected_items[0].text() # gets "username (host:port)" text
        username = peer_text.split(" ")[0]

        # in self.peers find the dict with this username
        peer_dict = next((p for p in self.peers if p["username"] == username), None)
        if not peer_dict:
            self.chat_area.append("Selected peer not found.")
            return
        
        receiver = Peer(**peer_dict)
        
        # get message text from input space
        msg_text = self.msg_input.text().strip()
        if not msg_text:
            return
        
        
        await Sender.send(message=Message(
            sender=self.acc,
            receiver=receiver,
            data=msg_text
        ))
        self.chat_area.append(f"You -> {username}: {msg_text}")
        self.msg_input.clear()

    async def on_msg_(self, msg: Message):
        """
        Callback from incoming messages from receiver
        
        Args:
            msg (Message): incoming message

        Returns: 
            None: Updates the UI
        """
        self.chat_area.append(f"{msg.sender.username} -> You: {msg.data}")

    # GUI create
    def __init__(self, account: Account):
        """
        Initialize the chat client GUI with the specified account.
        
        Args:
            account (Account): The authenticated user account to use for chatting
            
        Sets up the window, layout, and all UI components for the chat interface.
        """
        super().__init__()
        self.acc = account
        self.peers = []

        # window set
        self.setWindowTitle("P2P Chat (by jwmans)")
        self.setGeometry(200, 200, 500, 400)

        layout = QVBoxLayout()

        # acc info
        self.account_label = ChatAsyncLabel(f"Username: {self.acc.to_string()}")
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

        # receiver init
        self.receiver = Receiver(
            username=self.acc.username,
            host=self.acc.host,
            port=self.acc.port,
            callback=self.on_msg_
        )
        asyncio.create_task(self.receiver.start())

    def closeEvent(self, event: QCloseEvent):
        """
        Correct receiver stop when closing the window

        Args:
            event (QCloseEvent): describes the close event
        """
        asyncio.create_task(self.receiver.stop())
        event.accept()

if __name__ == "__main__":
    """
    Main entry point for the chat application.
    
    Initializes the Qt application, sets up asynchronous event loop,
    and launches the GUI with account authentication.
    """

    async def build_gui():
        """
        Build and launch the GUI application.
        
        Performs account authentication, creates the main window,
        registers the account, and refreshes the peer list.
        """
        acc = await auth()
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
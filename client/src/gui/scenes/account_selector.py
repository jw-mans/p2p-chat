from typing import List

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QInputDialog,
    QApplication
)

import asyncio

from ...account.account import Account
from ...utils.logging import log
from ..widgets.app_widgets import (
    ChatAsyncButton, ChatAsyncListWidget,
    ChatAsyncLabel
)

class AccountSelector(QWidget):
    """
    A widget for selecting or creating user accounts in the chat application.
    
    Provides a graphical interface for users to choose an existing account
    or create a new one. The selected account is stored in the _selected_ attribute.
    """

    def __select(self):
        """
        Handle account selection from the list.
        
        Reads the currently selected row from the list widget and creates
        an Account instance from the corresponding account data.
        """
        selected = self.list_widget.currentRow()
        if selected < 0: return
        self._selected_ = self.accounts[selected]
        log.info(f"Selected account: {self._selected_.username}")

    def __create(self):
        """
        Handle new account creation via dialog.
        
        Shows input dialogs to get username and port for a new account.
        Creates the account using Account.create().
        
        Uses 127.0.0.1 as default host. Validates port range (1024-65535).
        """
        username, ok = QInputDialog.getText(self, "New account", "Enter username: ")
        if not ok or not username.strip(): return

        host = "127.0.0.1"
        port, ok = QInputDialog.getInt(self, "New account", "Enter port: ", minValue=1024, maxValue=65535)
        if not ok: return

        self._selected_ = Account.create(username.strip(), host, port)
        log.info(f"Created new account: {self._selected_.username} ({self._selected_.host}:{self._selected_.port})")

    def __init__(self):
        """
        Initialize the account selector widget.
        
        Sets up the UI with account list, selection button, and creation button.
        Loads existing accounts from persistent storage and populates the list.
        """
        super().__init__()
        self._selected_ = None

        self.setWindowTitle("Select Account")
        self.setGeometry(300, 300, 300, 300)

        layout = QVBoxLayout()
        layout.addWidget(ChatAsyncLabel("Select an account:"))

        self.accounts = Account.get_accounts_from_file() # get available accounts list from file

        self.list_widget = ChatAsyncListWidget() # account list widget
        for ac in self.accounts:
            self.list_widget.addItem(f"{ac.to_string()}")
        layout.addWidget(self.list_widget)

        self.select_btn = ChatAsyncButton("Select account", self.__select, layout=layout)
        self.create_btn = ChatAsyncButton("Create new account", self.__create, layout=layout)
        self.setLayout(layout)

async def auth():
    """
    Display GUI dialog for account selection/creation.
    
    Returns:
        Account: Selected or created account instance
        
    Notes:
        This is an asynchronous method that must be awaited.
        Requires a running Qt event loop.
    """
    app = QApplication.instance()
    if app is None:
        app = QApplication([])

    selector = AccountSelector() # select account widget 
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
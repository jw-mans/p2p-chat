from PySide6.QtWidgets import (
    QWidget, QPushButton, QTextEdit,
    QListWidget, QLabel, QLineEdit
)
import asyncio

from client.src.gui.widgets.widget_mixin import WidgetMixin

class ChatAsyncWidget(QWidget, WidgetMixin):
    def __init__(self, *args, layout=None, **kwargs):
        super().__init__(*args, layout=layout, **kwargs)

class ChatAsyncTextEdit(QTextEdit, WidgetMixin):
    def __init__(self, *args, layout=None, **kwargs):
        super().__init__(*args, layout=layout, **kwargs)

class ChatAsyncListWidget(QListWidget, WidgetMixin):
    def __init__(self, *args, layout=None, **kwargs):
        super().__init__(*args, layout=layout, **kwargs)

class ChatAsyncLabel(QLabel, WidgetMixin):
    def __init__(self, *args, layout=None, **kwargs):
        super().__init__(*args, layout=layout, **kwargs)

class ChatAsyncLineEdit(QLineEdit, WidgetMixin):
    def __init__(self, *args, layout=None, **kwargs):
        super().__init__(*args, layout=layout, **kwargs)

class ChatAsyncButton(QPushButton, WidgetMixin):
    def __init__(self, text: str, callback=None, *args, layout=None, **kwargs):
        QPushButton.__init__(self, text, *args, **kwargs)
        WidgetMixin.__init__(self, layout=layout)
        if callback:
            self.clicked.connect(callback)


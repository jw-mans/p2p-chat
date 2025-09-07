from PySide6.QtWidgets import (
    QWidget, QPushButton, QTextEdit,
    QListWidget, QLabel, QLineEdit
)

from client.src.gui.widgets.widget_mixin import WidgetMixin

class ChatAsyncWidget(QWidget, WidgetMixin):
    """
    A base widget for chat application with automatic layout support.
    
    Args:
        layout: QLayout to automatically add this widget to
        *args: Positional arguments passed to QWidget
        **kwargs: Keyword arguments passed to QWidget
    """
    def __init__(self, *args, layout=None, **kwargs):
        super().__init__(*args, layout=layout, **kwargs)

class ChatAsyncTextEdit(QTextEdit, WidgetMixin):
    """
    A text edit widget for chat messages with layout support.
    
    Args:
        layout: QLayout to automatically add this widget to
        *args: Positional arguments passed to QTextEdit
        **kwargs: Keyword arguments passed to QTextEdit
    """
    def __init__(self, *args, layout=None, **kwargs):
        super().__init__(*args, layout=layout, **kwargs)

class ChatAsyncListWidget(QListWidget, WidgetMixin):
    """
    A list widget for chat participants or messages with layout support.
    
    Args:
        layout: QLayout to automatically add this widget to
        *args: Positional arguments passed to QListWidget
        **kwargs: Keyword arguments passed to QListWidget
    """
    def __init__(self, *args, layout=None, **kwargs):
        super().__init__(*args, layout=layout, **kwargs)

class ChatAsyncLabel(QLabel, WidgetMixin):
    """
    A label widget for chat interface with layout support.
    
    Args:
        layout: QLayout to automatically add this widget to
        *args: Positional arguments passed to QLabel
        **kwargs: Keyword arguments passed to QLabel
    """
    def __init__(self, *args, layout=None, **kwargs):
        super().__init__(*args, layout=layout, **kwargs)

class ChatAsyncLineEdit(QLineEdit, WidgetMixin):
    """
    A line edit widget for chat input fields with layout support.
    
    Args:
        layout: QLayout to automatically add this widget to
        *args: Positional arguments passed to QLineEdit
        **kwargs: Keyword arguments passed to QLineEdit
    """
    def __init__(self, *args, layout=None, **kwargs):
        super().__init__(*args, layout=layout, **kwargs)

class ChatAsyncButton(QPushButton, WidgetMixin):
    """
    A button widget for chat actions with automatic callback connection.
    
    Args:
        text: Button display text
        callback: Callback function to connect to clicked signal
        layout: QLayout to automatically add this widget to
        *args: Positional arguments passed to QPushButton
        **kwargs: Keyword arguments passed to QPushButton
    """
    def __init__(self, text: str, callback=None, *args, layout=None, **kwargs):
        QPushButton.__init__(self, text, *args, **kwargs)
        WidgetMixin.__init__(self, layout=layout)
        if callback:
            self.clicked.connect(callback)
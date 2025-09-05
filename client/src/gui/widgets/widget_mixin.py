from PySide6.QtWidgets import QLayout

class WidgetMixin:
    def __init__(self, *args, layout: QLayout = None, **kwargs):
        super().__init__(*args, **kwargs)
        if layout is not None:
            layout.addWidget(self)
from PySide6.QtWidgets import QLayout

class WidgetMixin:
    """
    A mixin class for automatic widget layout management.
    
    This mixin simplifies widget creation and layout assignment by automatically
    adding the widget to a specified layout during initialization.
    
    Args:
        layout (QLayout, optional): The layout to which the widget will be added.
            If provided, the widget is automatically added to this layout.
        *args: Variable length argument list passed to parent class.
        **kwargs: Arbitrary keyword arguments passed to parent class.
    
    Inheriting Classes:
        Should call super().__init__() to ensure proper mixin functionality.
    """
    
    def __init__(self, *args, layout: QLayout = None, **kwargs):
        """
        Initialize the widget and optionally add it to a layout.
        
        Args:
            *args: Positional arguments passed to the parent widget constructor
            layout: QLayout instance to automatically add this widget to
            **kwargs: Keyword arguments passed to the parent widget constructor
            
        Notes:
            The layout parameter must be passed as a keyword argument.
            The parent class must support QWidget-like initialization.
        """
        super().__init__(*args, **kwargs)
        if layout is not None:
            layout.addWidget(self)
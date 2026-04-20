"""
Custom message box implementation for the Truck Scale Weighing System.
Provides a consistent dialog interface that works reliably across different environments.
"""

import tkinter as tk
from tkinter import ttk
from typing import Optional, List, Tuple


class CustomMessageBox:
    """
    A custom message box implementation using Toplevel window to avoid issues with 
    standard messagebox functions in certain environments.
    """

    def __init__(self, parent: tk.Tk):
        """Initialize the CustomMessageBox with a parent window."""
        self.parent = parent

    def showinfo(self, title: str, message: str) -> None:
        """Show an information dialog."""
        self._create_dialog(title, message, "info", [("OK", "ok")])

    def showerror(self, title: str, message: str) -> None:
        """Show an error dialog."""
        self._create_dialog(title, message, "error", [("OK", "ok")])

    def showwarning(self, title: str, message: str) -> None:
        """Show a warning dialog."""
        self._create_dialog(title, message, "warning", [("OK", "ok")])

    def askyesno(self, title: str, message: str) -> bool:
        """Show a yes/no dialog and return True if Yes is clicked."""
        result = self._create_dialog(title, message, "question", [("Yes", "yes"), ("No", "no")])
        return result == "yes"

    def askquestion(self, title: str, message: str, buttons: Optional[List[Tuple[str, str, callable]]] = None) -> str:
        """
        Show a question dialog with custom buttons.
        
        Args:
            title: Dialog title
            message: Dialog message
            buttons: List of tuples (text, return_value, callback_function)
        
        Returns:
            The return value of the clicked button
        """
        if buttons is None:
            buttons = [("Yes", "yes", None), ("No", "no", None)]
        
        # Convert to the internal format
        internal_buttons = [(text, value) for text, value, _ in buttons]
        result = self._create_dialog(title, message, "question", internal_buttons)
        
        # Call the callback function if it exists
        for text, value, callback in buttons:
            if result == value and callback:
                callback()
        
        return result

    def _create_dialog(self, title: str, message: str, message_type: str, buttons: List[Tuple[str, str]]) -> str:
        """
        Create and display a dialog window.
        
        Args:
            title: Dialog title
            message: Dialog message
            message_type: Type of message ("info", "error", "warning", "question")
            buttons: List of tuples (button_text, return_value)
        
        Returns:
            The return value of the clicked button
        """
        dialog = tk.Toplevel(self.parent)
        dialog.title(title)
        dialog.transient(self.parent)
        dialog.grab_set()
        
        # Make the dialog modal
        dialog.focus_set()
        
        # Center the dialog
        dialog.geometry("+%d+%d" % (
            self.parent.winfo_rootx() + (self.parent.winfo_width() // 2 - 150),
            self.parent.winfo_rooty() + (self.parent.winfo_height() // 2 - 100)
        ))
        
        # Set minimum size
        dialog.minsize(300, 150)
        
        # Add icon if available
        try:
            if hasattr(self.parent, 'icon_path') and self.parent.icon_path:
                dialog.iconbitmap(self.parent.icon_path)
        except:
            pass
        
        # Create main frame
        main_frame = ttk.Frame(dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Add message label with appropriate icon
        message_frame = ttk.Frame(main_frame)
        message_frame.pack(fill=tk.BOTH, expand=True)
        
        # Add icon based on message type
        icon_text = {
            "info": "ℹ",
            "error": "✖", 
            "warning": "⚠",
            "question": "?"
        }.get(message_type, "")
        
        if icon_text:
            icon_label = ttk.Label(message_frame, text=icon_text, font=("Arial", 16))
            icon_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # Add message text
        message_label = ttk.Label(message_frame, text=message, wraplength=350, justify=tk.LEFT)
        message_label.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Add buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=(10, 0))
        
        result = None
        
        def button_click(btn_result: str):
            """Handle button click."""
            nonlocal result
            result = btn_result
            dialog.destroy()
        
        # Create buttons
        for btn_text, btn_value in buttons:
            btn = ttk.Button(button_frame, text=btn_text, command=lambda r=btn_value: button_click(r))
            btn.pack(side=tk.LEFT, padx=5)
        
        # Handle window close
        def on_close():
            """Handle window close event."""
            nonlocal result
            if result is None:
                result = buttons[-1][1] if buttons else "cancel"
            dialog.destroy()
        
        dialog.protocol("WM_DELETE_WINDOW", on_close)
        
        # Wait for dialog to close
        dialog.wait_window()
        
        return result or "cancel"

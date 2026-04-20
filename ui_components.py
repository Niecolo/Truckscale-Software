"""
UI components and utilities for the Truck Scale Weighing System.
Provides reusable UI components and helper functions.
"""

import tkinter as tk
from tkinter import ttk
import logging
from typing import Dict, Any, Optional, Callable, List, Tuple


class UIHelper:
    """Helper class for common UI operations and components."""
    
    @staticmethod
    def create_label_entry_frame(parent: tk.Widget, label_text: str, 
                            entry_var: tk.StringVar, width: int = 20,
                            label_width: int = 15) -> ttk.Frame:
        """
        Create a frame with a label and entry widget.
        
        Args:
            parent: Parent widget
            label_text: Text for the label
            entry_var: StringVar for the entry
            width: Width of the entry widget
            label_width: Width of the label
            
        Returns:
            Frame containing label and entry
        """
        frame = ttk.Frame(parent)
        label = ttk.Label(frame, text=label_text, width=label_width)
        label.pack(side=tk.LEFT, padx=5)
        
        entry = ttk.Entry(frame, textvariable=entry_var, width=width)
        entry.pack(side=tk.LEFT, padx=5)
        
        return frame
    
    @staticmethod
    def create_label_combobox_frame(parent: tk.Widget, label_text: str,
                                 combobox_var: tk.StringVar, values: List[str],
                                 width: int = 15, label_width: int = 15) -> ttk.Frame:
        """
        Create a frame with a label and combobox widget.
        
        Args:
            parent: Parent widget
            label_text: Text for the label
            combobox_var: StringVar for the combobox
            values: List of values for the combobox
            width: Width of the combobox
            label_width: Width of the label
            
        Returns:
            Frame containing label and combobox
        """
        frame = ttk.Frame(parent)
        label = ttk.Label(frame, text=label_text, width=label_width)
        label.pack(side=tk.LEFT, padx=5)
        
        combobox = ttk.Combobox(frame, textvariable=combobox_var, 
                              values=values, width=width, state="readonly")
        combobox.pack(side=tk.LEFT, padx=5)
        
        return frame
    
    @staticmethod
    def create_button_frame(parent: tk.Widget, buttons: List[Tuple[str, Callable]]) -> ttk.Frame:
        """
        Create a frame with multiple buttons.
        
        Args:
            parent: Parent widget
            buttons: List of tuples (text, command)
            
        Returns:
            Frame containing buttons
        """
        frame = ttk.Frame(parent)
        
        for text, command in buttons:
            button = ttk.Button(frame, text=text, command=command)
            button.pack(side=tk.LEFT, padx=5)
        
        return frame
    
    @staticmethod
    def create_scrollable_frame(parent: tk.Widget, height: int = 400, 
                             width: int = 600) -> Tuple[ttk.Frame, tk.Canvas]:
        """
        Create a scrollable frame.
        
        Args:
            parent: Parent widget
            height: Height of the scrollable area
            width: Width of the scrollable area
            
        Returns:
            Tuple of (scrollable_frame, canvas)
        """
        # Create canvas with scrollbar
        canvas = tk.Canvas(parent, height=height, width=width)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack widgets
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        return scrollable_frame, canvas
    
    @staticmethod
    def center_window(window: tk.Toplevel, parent: tk.Tk = None):
        """
        Center a window on the screen or relative to parent.
        
        Args:
            window: Window to center
            parent: Parent window (optional)
        """
        window.update_idletasks()
        
        if parent:
            # Center relative to parent
            x = parent.winfo_x() + (parent.winfo_width() // 2) - (window.winfo_width() // 2)
            y = parent.winfo_y() + (parent.winfo_height() // 2) - (window.winfo_height() // 2)
        else:
            # Center on screen
            x = (window.winfo_screenwidth() // 2) - (window.winfo_width() // 2)
            y = (window.winfo_screenheight() // 2) - (window.winfo_height() // 2)
        
        window.geometry(f"+{x}+{y}")
    
    @staticmethod
    def create_treeview_with_scrollbars(parent: tk.Widget, columns: List[str],
                                    show_headings: bool = True) -> ttk.Treeview:
        """
        Create a Treeview with scrollbars.
        
        Args:
            parent: Parent widget
            columns: List of column identifiers
            show_headings: Whether to show column headings
            
        Returns:
            Configured Treeview widget
        """
        # Create treeview
        tree = ttk.Treeview(parent, columns=columns, show="headings" if show_headings else "tree")
        
        # Add scrollbars
        vsb = ttk.Scrollbar(parent, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(parent, orient="horizontal", command=tree.xview)
        
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Grid layout
        tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        
        # Configure grid weights
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)
        
        return tree
    
    @staticmethod
    def create_status_bar(parent: tk.Tk) -> ttk.Frame:
        """
        Create a status bar at the bottom of the window.
        
        Args:
            parent: Parent window
            
        Returns:
            Status bar frame
        """
        status_frame = ttk.Frame(parent)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Create status label
        status_label = ttk.Label(status_frame, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        status_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2, pady=2)
        
        return status_frame, status_label


class TabManager:
    """Manages notebook tabs and their content."""
    
    def __init__(self, parent: tk.Widget):
        """
        Initialize the tab manager.
        
        Args:
            parent: Parent widget for the notebook
        """
        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(expand=True, fill="both")
        self.tabs = {}
    
    def add_tab(self, tab_name: str, widget_class: type, *args, **kwargs) -> tk.Widget:
        """
        Add a new tab to the notebook.
        
        Args:
            tab_name: Name of the tab
            widget_class: Class to instantiate for the tab content
            *args: Arguments for the widget class
            **kwargs: Keyword arguments for the widget class
            
        Returns:
            Created widget instance
        """
        # Create frame for the tab
        tab_frame = ttk.Frame(self.notebook)
        
        # Create the widget
        widget = widget_class(tab_frame, *args, **kwargs)
        
        # Add tab to notebook
        self.notebook.add(tab_frame, text=tab_name)
        self.tabs[tab_name] = (tab_frame, widget)
        
        return widget
    
    def get_tab(self, tab_name: str) -> Optional[Tuple[ttk.Frame, tk.Widget]]:
        """
        Get a tab by name.
        
        Args:
            tab_name: Name of the tab
            
        Returns:
            Tuple of (frame, widget) or None if not found
        """
        return self.tabs.get(tab_name)
    
    def remove_tab(self, tab_name: str) -> bool:
        """
        Remove a tab by name.
        
        Args:
            tab_name: Name of the tab to remove
            
        Returns:
            True if removed, False if not found
        """
        if tab_name in self.tabs:
            tab_frame, _ = self.tabs[tab_name]
            self.notebook.forget(tab_frame)
            del self.tabs[tab_name]
            return True
        return False
    
    def enable_tab(self, tab_name: str, enabled: bool = True):
        """
        Enable or disable a tab.
        
        Args:
            tab_name: Name of the tab
            enabled: Whether to enable the tab
        """
        if tab_name in self.tabs:
            tab_frame, _ = self.tabs[tab_name]
            state = "normal" if enabled else "disabled"
            
            # Find the tab index
            for i, tab_id in enumerate(self.notebook.tabs()):
                if self.notebook.tab(tab_id, "text") == tab_name:
                    self.notebook.tab(i, state=state)
                    break


class FormValidator:
    """Helper class for form validation."""
    
    @staticmethod
    def validate_required(field_name: str, value: str, 
                       error_callback: Optional[Callable[[str], None]] = None) -> bool:
        """
        Validate that a required field is not empty.
        
        Args:
            field_name: Name of the field
            value: Field value
            error_callback: Callback for error messages
            
        Returns:
            True if valid, False otherwise
        """
        if not value or not value.strip():
            error_msg = f"{field_name} is required"
            if error_callback:
                error_callback(error_msg)
            return False
        return True
    
    @staticmethod
    def validate_numeric(field_name: str, value: str,
                      error_callback: Optional[Callable[[str], None]] = None) -> bool:
        """
        Validate that a field contains a numeric value.
        
        Args:
            field_name: Name of the field
            value: Field value
            error_callback: Callback for error messages
            
        Returns:
            True if valid, False otherwise
        """
        try:
            float(value)
            return True
        except ValueError:
            error_msg = f"{field_name} must be a number"
            if error_callback:
                error_callback(error_msg)
            return False
    
    @staticmethod
    def validate_range(field_name: str, value: str, min_val: float, max_val: float,
                     error_callback: Optional[Callable[[str], None]] = None) -> bool:
        """
        Validate that a numeric value is within a range.
        
        Args:
            field_name: Name of the field
            value: Field value
            min_val: Minimum allowed value
            max_val: Maximum allowed value
            error_callback: Callback for error messages
            
        Returns:
            True if valid, False otherwise
        """
        try:
            num_value = float(value)
            if min_val <= num_value <= max_val:
                return True
            else:
                error_msg = f"{field_name} must be between {min_val} and {max_val}"
                if error_callback:
                    error_callback(error_msg)
                return False
        except ValueError:
            error_msg = f"{field_name} must be a number"
            if error_callback:
                error_callback(error_msg)
            return False


class ProgressDialog:
    """A simple progress dialog for long-running operations."""
    
    def __init__(self, parent: tk.Tk, title: str = "Progress", 
                 message: str = "Working..."):
        """
        Initialize the progress dialog.
        
        Args:
            parent: Parent window
            title: Dialog title
            message: Progress message
        """
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Make dialog modal
        self.dialog.focus_set()
        
        # Center the dialog
        UIHelper.center_window(self.dialog, parent)
        
        # Create content
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Message label
        self.message_label = ttk.Label(main_frame, text=message)
        self.message_label.pack(pady=10)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var,
                                        maximum=100, length=300)
        self.progress_bar.pack(pady=10)
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="")
        self.status_label.pack(pady=5)
        
        # Prevent resizing
        self.dialog.resizable(False, False)
    
    def update_progress(self, value: float, status: str = None):
        """
        Update the progress bar and status.
        
        Args:
            value: Progress value (0-100)
            status: Status message (optional)
        """
        self.progress_var.set(value)
        if status:
            self.status_label.config(text=status)
        self.dialog.update_idletasks()
    
    def close(self):
        """Close the progress dialog."""
        self.dialog.destroy()


class ConfirmDialog:
    """A customizable confirmation dialog."""
    
    def __init__(self, parent: tk.Tk, title: str, message: str,
                 buttons: List[Tuple[str, str]] = None):
        """
        Initialize the confirmation dialog.
        
        Args:
            parent: Parent window
            title: Dialog title
            message: Dialog message
            buttons: List of tuples (button_text, return_value)
        """
        self.parent = parent
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        UIHelper.center_window(self.dialog, parent)
        
        # Create content
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Message
        message_label = ttk.Label(main_frame, text=message, wraplength=300)
        message_label.pack(pady=20)
        
        # Buttons
        if buttons is None:
            buttons = [("Yes", "yes"), ("No", "no")]
        
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)
        
        for text, value in buttons:
            button = ttk.Button(button_frame, text=text,
                             command=lambda v=value: self._on_button_click(v))
            button.pack(side=tk.LEFT, padx=5)
        
        # Handle window close
        self.dialog.protocol("WM_DELETE_WINDOW", self._on_close)
    
    def _on_button_click(self, value: str):
        """Handle button click."""
        self.result = value
        self.dialog.destroy()
    
    def _on_close(self):
        """Handle window close."""
        if self.result is None:
            self.result = "cancel"
        self.dialog.destroy()
    
    def show(self) -> str:
        """
        Show the dialog and wait for response.
        
        Returns:
            The button value that was clicked
        """
        self.dialog.wait_window()
        return self.result or "cancel"

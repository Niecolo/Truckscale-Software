"""
Truck Scale Weighing System - Main Entry Point
With Global Exception Handling
"""

import sys
import os
import logging
import traceback
from datetime import datetime
from typing import Optional

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Application constants
APP_NAME = "Truck Scale Weighing System"
APP_VERSION = "1.0.0"
LOG_FOLDER = "logs"
LOG_FILE_PREFIX = "weighing_scale"


# ==================== Global Exception Handler ====================

class GlobalExceptionHandler:
    """
    Global exception handler that catches unhandled exceptions
    and provides graceful error handling.
    """
    
    def __init__(self, log_file: str = None):
        self.log_file = log_file
        self.logger = logging.getLogger("GlobalExceptionHandler")
        self._original_excepthook = sys.excepthook
    
    def install(self) -> None:
        """Install the global exception handler."""
        sys.excepthook = self.handle_exception
        self.logger.info("Global exception handler installed")
    
    def uninstall(self) -> None:
        """Uninstall the global exception handler."""
        sys.excepthook = self._original_excepthook
        self.logger.info("Global exception handler uninstalled")
    
    def handle_exception(self, exc_type, exc_value, exc_traceback):
        """
        Handle uncaught exceptions.
        """
        # Ignore KeyboardInterrupt (allow normal exit)
        if issubclass(exc_type, KeyboardInterrupt):
            self._original_excepthook(exc_type, exc_value, exc_traceback)
            return
        
        # Format the exception
        error_msg = self._format_exception(exc_type, exc_value, exc_traceback)
        
        # Log the error
        self.logger.critical(
            f"Unhandled exception: {exc_type.__name__}: {exc_value}\n{error_msg}",
            exc_info=(exc_type, exc_value, exc_traceback)
        )
        
        # Write to log file if available
        if self.log_file:
            try:
                self._write_to_log_file(error_msg)
            except Exception as e:
                self.logger.error(f"Failed to write to log file: {e}")
        
        # Show error message to user if in GUI mode
        if hasattr(sys, 'gui_app'):
            self._show_error_dialog(exc_type, exc_value, error_msg)
    
    def _format_exception(self, exc_type, exc_value, exc_traceback) -> str:
        """Format exception information."""
        lines = [
            "=" * 60,
            f"UNHANDLED EXCEPTION",
            f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Exception Type: {exc_type.__name__}",
            f"Exception Value: {exc_value}",
            "",
            "Traceback:",
            "-" * 40
        ]
        
        # Add traceback
        tb_lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        lines.extend(tb_lines)
        lines.append("=" * 60)
        
        return "\n".join(lines)
    
    def _write_to_log_file(self, message: str) -> None:
        """Write error to log file."""
        if not self.log_file:
            return
        
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(message)
                f.write("\n\n")
        except Exception:
            pass
    
    def _show_error_dialog(self, exc_type, exc_value, error_msg: str) -> None:
        """Show error dialog to user."""
        try:
            import tkinter as tk
            from tkinter import messagebox
            
            root = tk.Tk()
            root.withdraw()
            
            messagebox.showerror(
                f"Application Error - {exc_type.__name__}",
                f"An unexpected error occurred:\n\n{exc_value}\n\n"
                f"The error has been logged. Please restart the application."
            )
            
            root.destroy()
        except Exception:
            print(f"\nERROR: {exc_type.__name__}: {exc_value}", file=sys.stderr)
            print("Please check the log file for details.", file=sys.stderr)


# ==================== Logging Setup ====================

def setup_logging(log_folder: str = LOG_FOLDER) -> str:
    """
    Set up application logging.
    
    Returns:
        Path to the main log file
    """
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)
    
    timestamp = datetime.now().strftime("%Y%m%d")
    log_file = os.path.join(log_folder, f"{LOG_FILE_PREFIX}_{timestamp}.log")
    
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info(f"Logging initialized: {log_file}")
    
    return log_file


# ==================== Main Entry Point ====================

def get_icon_path() -> Optional[str]:
    """
    Get the path to the application icon.
    Returns the absolute path to app_icon.ico or None if not found.
    """
    possible_paths = [
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "app_icon.ico"),
        os.path.join(os.getcwd(), "assets", "app_icon.ico"),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "app_icon.ico"),
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return os.path.abspath(path)
    
    return None


def main():
    """Main entry point."""
    log_file = setup_logging()
    
    logger = logging.getLogger(__name__)
    logger.info(f"{APP_NAME} v{APP_VERSION} starting...")
    
    # Install global exception handler
    exception_handler = GlobalExceptionHandler(log_file=log_file)
    exception_handler.install()
    
    try:
        from weighing_scale_app import TruckScaleApp
        import tkinter as tk
        from PIL import Image, ImageTk
        
        logger.info("Launching GUI application...")
        
        root = tk.Tk()
        
        # Set app icon IMMEDIATELY after creating root window
        icon_path = get_icon_path()
        if icon_path:
            try:
                root.iconbitmap(default=icon_path)
                logger.info(f"Icon set successfully: {icon_path}")
            except Exception as e:
                logger.warning(f"Failed to set iconbitmap: {e}")
                try:
                    icon_image = Image.open(icon_path)
                    icon_photo = ImageTk.PhotoImage(icon_image)
                    root.iconphoto(True, icon_photo)
                    logger.info("Icon set via iconphoto fallback")
                except Exception as e2:
                    logger.warning(f"Failed to set icon via iconphoto: {e2}")
        else:
            logger.warning("Icon file not found in any expected location")
        
        app = TruckScaleApp(root)
        root.mainloop()
        
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received")
        
    except Exception as e:
        logger.critical(f"Fatal error: {e}", exc_info=True)
        
    finally:
        exception_handler.uninstall()
        logger.info("Application shutdown complete")


if __name__ == "__main__":
    main()
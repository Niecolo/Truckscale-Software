"""
PDF generation and printing module for the Truck Scale Weighing System.
Handles all PDF creation, template processing, and printing operations.
"""

import os
import tempfile
import subprocess
import logging
from datetime import datetime
from typing import Dict, Any, Optional, List, Tuple

# Try to import ReportLab for PDF generation
try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4, A6, letter, landscape, portrait
    from reportlab.lib.units import inch
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib import colors
    from reportlab.platypus import Image as RLImage
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
    from reportlab.pdfbase.pdfmetrics import registerFont, stringWidth
    from reportlab.pdfbase.ttfonts import TTFError, TTFont
    from reportlab.pdfbase import pdfmetrics
    from reportlab.lib.fonts import addMapping
    
    # Try to import barcode modules
    try:
        from reportlab.graphics.barcode import code128
        from reportlab.graphics.shapes import Drawing
        from reportlab.graphics import renderPDF
        BARCODE_AVAILABLE = True
    except ImportError:
        BARCODE_AVAILABLE = False
        
    PDF_PRINTING_ENABLED = True
except ImportError as e:
    logging.error(f"ReportLab import failed: {e}. PDF printing will be disabled.")
    PDF_PRINTING_ENABLED = False
    BARCODE_AVAILABLE = False

# Try to import Windows printing libraries
try:
    import sys
    if sys.platform == "win32":
        import win32print
        import win32api
    PRINTING_ENABLED = True
except ImportError:
    PRINTING_ENABLED = False


class PDFPrintManager:
    """Manages PDF generation and printing operations."""
    
    def __init__(self, msg_box=None):
        """
        Initialize the PDF print manager.
        
        Args:
            msg_box: Message box instance for error reporting
        """
        self.msg_box = msg_box
        self.registered_fonts = set()
        
        # Default settings
        self.default_font_family = "Helvetica"
        self.default_font_size = 10
        self.default_page_size = "A6"
        self.default_orientation = "portrait"
        
    def is_pdf_enabled(self) -> bool:
        """Check if PDF generation is enabled."""
        return PDF_PRINTING_ENABLED
    
    def is_printing_enabled(self) -> bool:
        """Check if printing is enabled."""
        return PRINTING_ENABLED
    
    def is_barcode_enabled(self) -> bool:
        """Check if barcode generation is enabled."""
        return BARCODE_AVAILABLE
    
    def generate_pdf_from_template(self, template_content: str, data: Dict[str, Any], 
                                 output_path: str, font_family: str = None,
                                 font_size: int = None, page_size: str = None,
                                 orientation: str = None) -> bool:
        """
        Generate a PDF from a template and data.
        
        Args:
            template_content: Template string with placeholders
            data: Dictionary of data to fill the template
            output_path: Path where the PDF should be saved
            font_family: Font family to use
            font_size: Font size to use
            page_size: Page size (A4, A6, Letter, etc.)
            orientation: Page orientation (portrait, landscape)
            
        Returns:
            True if successful, False otherwise
        """
        if not PDF_PRINTING_ENABLED:
            if self.msg_box:
                self.msg_box.showerror("PDF Error", "PDF generation is not available. Please install ReportLab.")
            return False
        
        try:
            # Use defaults if not provided
            font_family = font_family or self.default_font_family
            font_size = font_size or self.default_font_size
            page_size = page_size or self.default_page_size
            orientation = orientation or self.default_orientation
            
            # Format template with data
            formatted_text = self._format_template(template_content, data)
            
            # Create PDF
            self._create_pdf_document(
                formatted_text, output_path, font_family, 
                font_size, page_size, orientation
            )
            
            return True
            
        except Exception as e:
            error_msg = f"Failed to generate PDF: {e}"
            logging.error(error_msg)
            if self.msg_box:
                self.msg_box.showerror("PDF Error", error_msg)
            return False
    
    def _format_template(self, template: str, data: Dict[str, Any]) -> str:
        """
        Format a template string with data, handling missing keys gracefully.
        
        Args:
            template: Template string with placeholders
            data: Dictionary of data
            
        Returns:
            Formatted string
        """
        class SafeDict(dict):
            """Dictionary that returns empty string for missing keys."""
            def __missing__(self, key):
                return ''
        
        return template.format_map(SafeDict(data))
    
    def _create_pdf_document(self, content: str, output_path: str, 
                           font_family: str, font_size: int, 
                           page_size: str, orientation: str):
        """
        Create the actual PDF document.
        
        Args:
            content: Formatted content to write
            output_path: Output file path
            font_family: Font family to use
            font_size: Font size to use
            page_size: Page size
            orientation: Page orientation
        """
        # Get page size object
        page_size_obj = self._get_page_size(page_size, orientation)
        
        # Create canvas
        c = canvas.Canvas(output_path, pagesize=page_size_obj)
        
        # Set font
        try:
            c.setFont(font_family, font_size)
        except:
            # Fallback to Helvetica if font not found
            c.setFont("Helvetica", font_size)
        
        # Write content
        lines = content.split('\n')
        y_position = page_size_obj[1] - 20  # Start from top with margin
        line_height = font_size + 2
        
        for line in lines:
            if y_position < 20:  # Check if we need a new page
                c.showPage()
                y_position = page_size_obj[1] - 20
                c.setFont(font_family, font_size)
            
            c.drawString(10, y_position, line)
            y_position -= line_height
        
        # Save PDF
        c.save()
    
    def _get_page_size(self, size_name: str, orientation: str) -> Tuple[float, float]:
        """
        Get page size object based on name and orientation.
        
        Args:
            size_name: Name of the page size
            orientation: Page orientation
            
        Returns:
            Tuple of (width, height)
        """
        size_map = {
            "A4": A4,
            "A6": A6,
            "Letter": letter,
        }
        
        page_size = size_map.get(size_name, A6)
        
        if orientation.lower() == "landscape":
            page_size = landscape(page_size)
        else:
            page_size = portrait(page_size)
        
        return page_size
    
    def generate_ticket_pdf(self, transaction_data: Dict[str, Any], 
                         template_content: str, output_path: str,
                         settings: Dict[str, Any] = None) -> bool:
        """
        Generate a specialized ticket PDF with proper formatting.
        
        Args:
            transaction_data: Transaction data
            template_content: Template for the ticket
            output_path: Output file path
            settings: Additional settings for formatting
            
        Returns:
            True if successful, False otherwise
        """
        if not PDF_PRINTING_ENABLED:
            return False
        
        settings = settings or {}
        
        try:
            # Get settings
            font_family = settings.get('font_family', self.default_font_family)
            font_size = settings.get('font_size', self.default_font_size)
            page_size = settings.get('page_size', self.default_page_size)
            orientation = settings.get('orientation', self.default_orientation)
            header_font_size = settings.get('header_font_size', font_size)
            
            # Format template
            formatted_text = self._format_template(template_content, transaction_data)
            
            # Create specialized ticket PDF
            self._create_ticket_pdf(
                formatted_text, output_path, font_family, font_size,
                header_font_size, page_size, orientation, transaction_data
            )
            
            return True
            
        except Exception as e:
            error_msg = f"Failed to generate ticket PDF: {e}"
            logging.error(error_msg)
            if self.msg_box:
                self.msg_box.showerror("PDF Error", error_msg)
            return False
    
    def _create_ticket_pdf(self, content: str, output_path: str,
                          font_family: str, font_size: int, header_font_size: int,
                          page_size: str, orientation: str, transaction_data: Dict[str, Any]):
        """
        Create a specialized ticket PDF with header/detail formatting.
        
        Args:
            content: Formatted content
            output_path: Output file path
            font_family: Font family
            font_size: Regular font size
            header_font_size: Header font size
            page_size: Page size
            orientation: Page orientation
            transaction_data: Transaction data for additional processing
        """
        page_size_obj = self._get_page_size(page_size, orientation)
        c = canvas.Canvas(output_path, pagesize=page_size_obj)
        
        # Set font
        try:
            c.setFont(font_family, font_size)
        except:
            c.setFont("Helvetica", font_size)
        
        # Parse lines and determine header section
        lines = content.split('\n')
        y_position = page_size_obj[1] - 20
        line_height = font_size + 2
        
        # Find where header ends (before TICKET NO line)
        header_end_index = 0
        for i, line in enumerate(lines):
            if 'TICKET NO' in line.upper():
                header_end_index = i
                break
        
        # Draw lines with appropriate font sizes
        for idx, line in enumerate(lines):
            if line.strip():
                # Determine font size based on position
                if idx < header_end_index:
                    # Header line
                    current_font_size = header_font_size
                    current_line_height = header_font_size + 2
                else:
                    # Detail line
                    current_font_size = font_size
                    current_line_height = line_height
                
                # Set font and draw line
                try:
                    c.setFont(font_family, current_font_size)
                except:
                    c.setFont("Helvetica", current_font_size)
                
                c.drawString(10, y_position, line)
                y_position -= current_line_height
            else:
                # Empty line - add spacing
                y_position -= line_height
        
        # Add signature line
        y_position -= 10
        try:
            c.setFont(font_family, font_size)
        except:
            c.setFont("Helvetica", font_size)
        c.drawString(10, y_position, "___________________")
        
        # Save PDF
        c.save()
    
    def print_pdf_file(self, pdf_path: str, printer_name: str = None, 
                     copies: int = 1) -> bool:
        """
        Print a PDF file to the specified printer.
        
        Args:
            pdf_path: Path to the PDF file
            printer_name: Name of the printer (None for default)
            copies: Number of copies to print
            
        Returns:
            True if successful, False otherwise
        """
        if not PRINTING_ENABLED:
            if self.msg_box:
                self.msg_box.showerror("Print Error", "Printing is not available on this system.")
            return False
        
        if not os.path.exists(pdf_path):
            if self.msg_box:
                self.msg_box.showerror("Print Error", f"PDF file not found: {pdf_path}")
            return False
        
        try:
            if sys.platform == "win32":
                return self._print_windows(pdf_path, printer_name, copies)
            else:
                return self._print_linux_mac(pdf_path, printer_name, copies)
        except Exception as e:
            error_msg = f"Failed to print PDF: {e}"
            logging.error(error_msg)
            if self.msg_box:
                self.msg_box.showerror("Print Error", error_msg)
            return False
    
    def _print_windows(self, pdf_path: str, printer_name: str, copies: int) -> bool:
        """Print on Windows using win32print."""
        try:
            # Get default printer if none specified
            if not printer_name:
                printer_name = win32print.GetDefaultPrinter()
            
            # Print the file
            for _ in range(copies):
                win32api.ShellExecute(
                    0, "printto", pdf_path, f'"{printer_name}"', ".", 0
                )
            
            return True
        except Exception as e:
            logging.error(f"Windows printing error: {e}")
            return False
    
    def _print_linux_mac(self, pdf_path: str, printer_name: str, copies: int) -> bool:
        """Print on Linux/Mac using lp command."""
        try:
            cmd = ["lp"]
            if printer_name:
                cmd.extend(["-d", printer_name])
            if copies > 1:
                cmd.extend(["-n", str(copies)])
            cmd.append(pdf_path)
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.returncode == 0
        except Exception as e:
            logging.error(f"Linux/Mac printing error: {e}")
            return False
    
    def generate_barcode(self, data: str, output_path: str = None) -> Optional[bytes]:
        """
        Generate a barcode image.
        
        Args:
            data: Data to encode in the barcode
            output_path: Path to save the barcode (optional)
            
        Returns:
            Barcode image data as bytes, or None if failed
        """
        if not BARCODE_AVAILABLE:
            return None
        
        try:
            # Create barcode
            barcode = code128.Code128(data)
            
            if output_path:
                # Save to file
                from reportlab.graphics import renderPM
                renderPM.drawToFile(barcode, output_path, fmt="PNG")
                return None
            else:
                # Return as bytes
                from reportlab.graphics import renderPM
                import io
                buffer = io.BytesIO()
                renderPM.drawToFile(barcode, buffer, fmt="PNG")
                return buffer.getvalue()
                
        except Exception as e:
            logging.error(f"Barcode generation error: {e}")
            return None
    
    def get_available_printers(self) -> List[str]:
        """
        Get list of available printers.
        
        Returns:
            List of printer names
        """
        if not PRINTING_ENABLED:
            return []
        
        try:
            if sys.platform == "win32":
                return [printer[2] for printer in win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL)]
            else:
                # Try to get printers via lpstat on Linux/Mac
                result = subprocess.run(["lpstat", "-p"], capture_output=True, text=True)
                if result.returncode == 0:
                    printers = []
                    for line in result.stdout.split('\n'):
                        if line.startswith('printer'):
                            printers.append(line.split()[1])
                    return printers
        except Exception as e:
            logging.error(f"Error getting printers: {e}")
        
        return []
    
    def preview_pdf(self, pdf_path: str) -> bool:
        """
        Open a PDF file for preview.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if sys.platform == "win32":
                os.startfile(pdf_path)
            elif sys.platform == "darwin":  # macOS
                subprocess.run(["open", pdf_path])
            else:  # Linux
                subprocess.run(["xdg-open", pdf_path])
            return True
        except Exception as e:
            error_msg = f"Failed to preview PDF: {e}"
            logging.error(error_msg)
            if self.msg_box:
                self.msg_box.showerror("Preview Error", error_msg)
            return False

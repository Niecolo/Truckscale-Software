"""
Constants and configuration for the Truck Scale Weighing System.
"""

import os
import sys
import hashlib

# Directory paths
PROGRAM_DATA_DIR = r"C:\ProgramData\Truck Scale"
CONFIG_FILE = os.path.join(PROGRAM_DATA_DIR, "config.json")
DB_FILE = os.path.join(PROGRAM_DATA_DIR, "database.db")

# Ensure the directory exists
os.makedirs(PROGRAM_DATA_DIR, exist_ok=True)

# Security constants
# WARNING: Default admin password is "password" - CHANGE THIS IMMEDIATELY after first login!
# The system will prompt for password change on first run if configured
ADMIN_PASSWORD_HASH = "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"  # SHA-256 of "password"
ADMIN_USERNAME = "admin"
# WARNING: Activation code is exposed in source - consider using environment variable or secure storage
# For production, use: os.environ.get('ACTIVATION_CODE', 'default_code')
ACTIVATION_CODE = "789123"

# Generate a proper encryption key or load from secure storage
# For production, this should be loaded from a secure key management system
import os
import secrets

def _get_or_create_encryption_key():
    """
    Get encryption key from secure storage or create a new one.
    In production, this should load from a secure key management system.
    """
    key_file = os.path.join(PROGRAM_DATA_DIR, ".encryption_key")
    
    # Try to load existing key
    if os.path.exists(key_file):
        try:
            with open(key_file, 'rb') as f:
                key = f.read()
                if len(key) == 32:
                    return key
        except Exception:
            pass
    
    # Generate a new secure random key
    key = secrets.token_bytes(32)
    
    # Save the key for future use (with restricted permissions)
    try:
        with open(key_file, 'wb') as f:
            f.write(key)
        # On Windows, restrict file access
        if os.name == 'nt':
            import ctypes
            ctypes.windll.kernel32.SetFileAttributesW(key_file, 2)  # FILE_ATTRIBUTE_HIDDEN
    except Exception:
        pass  # Key generation continues even if saving fails
    
    return key

ENCRYPTION_KEY = _get_or_create_encryption_key()  # 32 bytes for AES-256

# Trial and activation periods
EXPIRY_DAYS_INITIAL_TRIAL = 30  # 30 days trial period
EXPIRY_DAYS_ON_ACTIVATION = 1825  # 5 Years Activation

# Weight measurement constants
REQUIRED_WEIGHT_STABILITY = 3
MAX_WEIGHT_DEVIATION = 10.0  # Weight Division

# Default serial communication settings
DEFAULT_BAUD_RATE = 9600
DEFAULT_READ_INTERVAL_MS = 50

# Predefined regex patterns for weight data parsing
PREDEFINED_REGEXES = [
    r"ww(-?\d+)",  # Handle ww-format with optional minus (like ww-0001080)
    r"(-?\d+\.\d+)\s*kg",  # Handle number followed by kg
    r"ST,GS,(\d+\.\d+)",
    r"W=(\d+\.\d+)",
    r"([\+\-]?\d+\.\d+)",  # General signed float
    r"(\d+\.\d+)",
    r"(\d+)",
    r"\+000(\d+)019",  # Keli & Keda format
    "Custom"
]

# Available print placeholders for templates
AVAILABLE_PRINT_PLACEHOLDERS = [
    ("Company", "{company}"),
    ("Ticket Number", "{ticket_no}"),
    ("Truck Plate", "{truck_plate}"),
    ("Product", "{product}"),
    ("Designation", "{designation}"),
    ("Sender", "{sender}"),
    ("Origin", "{origin}"),
    ("Destination", "{destination}"),
    ("Driver", "{driver}"),
    ("Gross Weight", "{gross_weight}"),
    ("Gross Date", "{gross_date}"),
    ("Gross Time", "{gross_time}"),
    ("Tare Weight", "{tare_weight}"),
    ("Tare Date", "{tare_date}"),
    ("Tare Time", "{tare_time}"),
    ("Net Weight", "{net_weight}"),
    ("Net Date", "{net_date}"),
    ("Net Time", "{net_time}"),
    ("Customer Name", "{customer_name}"),
    ("Material Type", "{material_type}"),
    ("Transaction Type", "{transaction_type}"),
    ("Weighing ID", "{weighing_id}"),
    ("First Weight", "{first_weight}"),
    ("First Date", "{first_date}"),
    ("First Time", "{first_time}"),
    ("Second Weight", "{second_weight}"),
    ("Second Date", "{second_date}"),
    ("Second Time", "{second_time}"),
    ("Difference", "{difference}"),
    ("Unit Price", "{unit_price}"),
    ("Total Price", "{total_price}"),
    ("Remarks", "{remarks}"),
    ("Operator", "{operator}"),
    ("Current Date", "{current_date}"),
    ("Current Time", "{current_time}"),
]

# Dummy barcode modules for reportlab compatibility
DUMMY_BARCODE_MODULES = [
    'reportlab.graphics.barcode.usps4s',
    'reportlab.graphics.barcode.code11',
    'reportlab.graphics.barcode.code39',
    'reportlab.graphics.barcode.code93',
    'reportlab.graphics.barcode.ean',
    'reportlab.graphics.barcode.ean13',
    'reportlab.graphics.barcode.ean8',
    'reportlab.graphics.barcode.imperial2of5',
    'reportlab.graphics.barcode.interleaved2of5',
    'reportlab.graphics.barcode.postnet',
    'reportlab.graphics.barcode.qr',
    'reportlab.graphics.barcode.ecc200datamatrix',
    'reportlab.graphics.barcode.lto',
    'reportlab.graphics.barcode.msecode128',
    'reportlab.graphics.barcode.rportuguese',
    'reportlab.graphics.barcode.symbol',
    'reportlab.graphics.barcode.upca',
]

# Price computation constants
DEFAULT_BASE_WEIGHT = 20000  # Base weight for price calculation (kg)
DEFAULT_BASE_PRICE = 150.00  # Base price for base weight
DEFAULT_INCREMENT_WEIGHT = 100  # Additional weight unit (kg)
DEFAULT_INCREMENT_PRICE = 10.00  # Additional price per increment unit

# Window and UI constants
WINDOW_TITLE = "Truck Scale Weighing System"
DEFAULT_WINDOW_GEOMETRY = "1200x700"
MIN_WINDOW_SIZE = (1000, 600)

# Default configuration values
DEFAULT_CONFIG = {
    "initial_trial_start_date": None,
    "expiry_date": None,
    "is_activated": False,
    "has_saved_initial_config": False,
    "admin_password_hash": ADMIN_PASSWORD_HASH,
    "max_weight_deviation": MAX_WEIGHT_DEVIATION,
    "read_loop_interval_ms": DEFAULT_READ_INTERVAL_MS,
    "pdf_print_template_font_family": "Helvetica",
    "pdf_print_template_font_size": 12,
    "pdf_print_template_font_bold": False,
    "pdf_page_size": "A4",
    "pdf_orientation": "portrait",
    "base_weight": DEFAULT_BASE_WEIGHT,
    "base_price": DEFAULT_BASE_PRICE,
    "increment_weight": DEFAULT_INCREMENT_WEIGHT,
    "increment_price": DEFAULT_INCREMENT_PRICE,
    "price_computation_enabled": True,
    "starting_ticket_number": 1000
}

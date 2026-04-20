# 🚛 Truck Scale Weighing System

A comprehensive desktop application for managing truck weighing operations, built with Python and Tkinter.

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.11.9-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)
![License](https://img.shields.io/badge/license-Proprietary-red.svg)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Screenshots](#screenshots)
- [System Requirements](#system-requirements)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [Dependencies](#dependencies)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## 🎯 Overview

The **Truck Scale Weighing System** is a professional-grade desktop application designed for industrial weighing operations. It provides a complete solution for managing truck weighing transactions, from initial weight capture to ticket printing and report generation.

### Key Highlights

- **Real-time Weight Measurement**: Live data streaming from electronic weighing scales
- **Transaction Management**: Complete workflow for one-way and two-way weighing operations
- **Multi-user Support**: Role-based access control with Admin, Operator, and User roles
- **Camera Integration**: Photo capture for transaction documentation
- **PDF Generation**: Customizable weighing tickets with barcode support
- **Price Calculation**: Automatic pricing based on configurable weight parameters

---

## ✨ Features

### Core Functionality

| Feature | Description |
|---------|-------------|
| **One-Way Weighing** | Single weight measurement for simple transactions |
| **Two-Way Weighing** | Gross and tare weight capture with automatic net calculation |
| **Live Weight Display** | Real-time weight streaming with stability detection |
| **Transaction Management** | Create, edit, search, and delete weighing records |
| **Pending Records** | Track incomplete two-way weighing transactions |

### User Interface

- **Modern Tabbed Interface**: Organized workflow with Entry Form, Pending Records, Completed Records, Reports, and Settings tabs
- **Customizable Entry Form**: Configure visible fields and their order
- **Real-time Search**: Filter transactions by company, truck plate, ticket number, and more
- **Date Range Filtering**: View records by specific date periods

### Hardware Integration

- **Serial Communication**: Connect to electronic scales via COM port
- **Multiple Scale Formats**: Support for various weight data protocols
- **Camera Support**: USB camera integration for photo documentation
- **External Display**: Optional big display output for weight viewing
- **Weight Emulator**: Built-in emulator for testing without physical scale

### Reporting & Export

- **PDF Tickets**: Customizable ticket templates with barcode generation
- **CSV Export**: Export transaction data to spreadsheet format
- **Excel Export**: Enhanced export with auto-fitted columns
- **Print Preview**: Preview tickets before printing

### Security & Management

- **User Authentication**: Secure login with password hashing (SHA-256)
  <img width="1365" height="721" alt="image" src="https://github.com/user-attachments/assets/be06461a-84bc-4f0c-b601-de807b717d35" />

- **Role-based Access Control**: Admin, Operator, and User permission levels
  <img width="1365" height="707" alt="image" src="https://github.com/user-attachments/assets/1bccb97c-c3ef-4238-ab5f-f2f8251d319b" />

- **User Management**: Create, edit, and delete user accounts
  <img width="1349" height="301" alt="image" src="https://github.com/user-attachments/assets/2579ccd0-e6ea-4f47-b090-81f9b34fe28e" />

- **Application Activation**: Trial period with activation system
<img width="745" height="207" alt="image" src="https://github.com/user-attachments/assets/0e486639-1bf0-405c-b716-36d2d54834eb" />

---

## 📸 Screenshots

### Main Interface
The application features a modern, intuitive interface with a tabbed layout for efficient workflow management.

### Entry Form
<img width="1365" height="717" alt="image" src="https://github.com/user-attachments/assets/d458728d-3afe-4fa8-9b5c-5598dad7a36f" />

*Primary data entry form with live weight display and camera feed*

### Key Interface Elements

1. **Entry Form Tab**: Transaction data entry with live weight display <img width="1365" height="721" alt="image" src="https://github.com/user-attachments/assets/85b35c65-7989-4b5d-80c2-fd578556beb1" />

2. **Pending Records Tab**: Manage incomplete two-way transactions <img width="1365" height="721" alt="image" src="https://github.com/user-attachments/assets/d41b90cb-7506-4d66-b11d-913a6de70d1b" />

3. **Completed Records Tab**: View and manage finished transactions <img width="1365" height="725" alt="image" src="https://github.com/user-attachments/assets/e1229412-86f9-4ac5-848c-3cd98bbb2880" />

4. **Reports Tab**: Generate and export reports <img width="1365" height="724" alt="image" src="https://github.com/user-attachments/assets/ec760985-b04e-46e1-bad0-be7b3b142bd2" />

5. **Settings Tab**: System configuration and user management <img width="1365" height="714" alt="image" src="https://github.com/user-attachments/assets/51312a39-5a90-4c58-b024-5a08436e9b3f" />


---

## 💻 System Requirements

### Hardware Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **Processor** | Intel Core i3 | Intel Core i5 or higher |
| **RAM** | 4 GB | 8 GB or more |
| **Storage** | 500 MB | 1 GB |
| **Display** | 1366 x 768 | 1920 x 1080 |
| **Serial Port** | RS-232 COM port | USB-to-Serial adapter supported |

### Software Requirements

- **Operating System**: Windows 10/11 (64-bit)
- **Python**: Version 3.11.9 (recommended)
- **Database**: SQLite 3 (included with Python)

### Optional Hardware

- Electronic weighing scale with serial output
- USB webcam or integrated camera
- External weight display
- Thermal/Matrix printer for tickets

---

## 🚀 Installation

### Option 1: From Source (GitHub)

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Leoncio/Truckscale-Application.git
   cd Truckscale-Application
   ```

2. **Create Virtual Environment** (Recommended)
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup Database (First Run Only)**
   ```bash
   python setup_database.py
   ```

5. **Run the Application**
   ```bash
   python main.py
   ```

### Option 2: Portable/Executable

1. Download latest release from [GitHub Releases](https://github.com/Leoncio/Truckscale-Application/releases)
2. Extract the `.zip` package
3. Run `START_APP.bat` or `START_APP.ps1`
4. Application will launch automatically

### Build Executable (Developers)

```bash
# Build production executable
BUILD.bat
```

Executable output will be in the `dist/` directory.

---

## ⚡ Quick Start

### First-Time Setup

1. **Launch the Application**
   - Run `python main.py` or use the provided batch script

2. **Login with Default Credentials**
   - Username: `admin`
   - Password: `password`
   - ⚠️ **Important**: Change the default password immediately!

3. **Configure Serial Port**
   - Navigate to Settings → Comm Ports
   - Select your COM port and baud rate
   - Click "Start Connection"

4. **Configure Printer** (Optional)
   - Go to Settings → Print & Ticket Settings
   - Select your printer from the dropdown

### Basic Weighing Operation

#### One-Way Weighing
1. Select "ONE WAY" weight option
2. Enter transaction details (Company, Truck Plate, Product)
3. Position truck on scale
4. Wait for weight to stabilize
5. Click "Save"
6. Print ticket if needed

#### Two-Way Weighing
1. Select "TWO WAY" weight option
2. Enter transaction details
3. Record **Gross Weight** (loaded truck)
4. Save - transaction will be in "Pending" status
5. After unloading, go to Pending Records
6. Select the transaction and record **Tare Weight**
7. System automatically calculates **Net Weight**

---

## 📖 Usage

### User Roles and Permissions

| Feature | Admin | Operator | User |
|---------|-------|----------|------|
| Weighing Operations | ✅ | ✅ | ✅ |
| View Transactions | ✅ | ✅ | ✅ |
| View Reports | ✅ | ✅ | ✅ |
| Edit Transactions | ✅ | ✅ | ❌ |
| Delete Transactions | ✅ | ✅ | ❌ |
| Master Data Management | ✅ | ✅ | ❌ |
| Serial Port Settings | ✅ | ❌ | ❌ |
| User Management | ✅ | ❌ | ❌ |
| System Activation | ✅ | ❌ | ❌ |

### Entry Form Fields

The following fields can be configured for display:

- Company
- Truck Plate
- Product
- Designation
- Sender
- Origin
- Destination
- Driver
- Total Price (auto-calculated)

### Weight Data Formats

The system supports various scale data formats through configurable regex patterns:

| Format | Regex Pattern |
|--------|---------------|
| WW Format | `ww(-?\d+)` |
| Weight in kg | `(-?\d+\.\d+)\s*kg` |
| Standard | `ST,GS,(\d+\.\d+)` |
| W= Format | `W=(\d+\.\d+)` |
| Decimal | `(\d+\.\d+)` |
| Integer | `(\d+)` |

### Price Calculation

Automatic pricing is calculated based on:

```
If weight ≤ Base Weight:
    Total Price = Base Price

If weight > Base Weight:
    Total Price = Base Price + ((Weight - Base Weight) / Increment Weight × Increment Price)
```

**Default Parameters:**
- Base Weight: 20,000 kg
- Base Price: ₱150.00
- Increment Weight: 100 kg
- Increment Price: ₱10.00

---

## ⚙️ Configuration

### Configuration File Location

Configuration is stored in: `C:\ProgramData\Truck Scale\config.json`

### Key Configuration Options

```json
{
  "port": "COM1",
  "baud": "9600",
  "auto_connect": true,
  "data_format_regex": "ww(-?\\d+)",
  "decimal_places": 0,
  "read_loop_interval_ms": 50,
  "selected_printer": "Default Printer",
  "print_copies": 1,
  "pdf_page_size": "A6",
  "weight_option": "TWO_WAY",
  "price_computation_enabled": true,
  "base_weight": 20000,
  "base_price": 150,
  "increment_weight": 100,
  "increment_price": 10
}
```

### Serial Port Settings

| Setting | Description | Default |
|---------|-------------|---------|
| Port | COM port for scale | COM1 |
| Baud Rate | Communication speed | 9600 |
| Read Interval | Polling frequency (ms) | 50 |
| Max Weight Deviation | Stability threshold | 10.0 |

### Ticket Template Customization

Ticket templates support the following placeholders:

```
{ticket_no}      - Transaction ticket number
{company}        - Company name
{truck_plate}    - Vehicle registration
{product}        - Product type
{gross_weight}   - Gross weight value
{gross_date}     - Gross weighing date
{gross_time}     - Gross weighing time
{tare_weight}    - Tare weight value
{tare_date}      - Tare weighing date
{tare_time}      - Tare weighing time
{net_weight}     - Calculated net weight
{date_printed}   - Current date/time
{logged_in_user} - Operator name
{barcode}        - Barcode placeholder
```

---

## 📁 Project Structure

```
weighing_scale_project/
├── 📄 main.py                    # Application entry point
├── 📄 weighing_scale_app.py      # Main application logic
├── 📄 config.py                  # Configuration constants
├── 📄 database.py                # Database operations
├── 📄 serial_manager.py          # Serial communication
├── 📄 camera_manager.py          # Camera operations
├── 📄 pdf_print_manager.py       # PDF generation
├── 📄 ui_components.py           # UI components
├── 📄 messagebox.py              # Custom dialogs
├── 📄 setup_database.py          # Database initialization
│
├── 📄 requirements.txt           # Python dependencies
├── 📄 pyproject.toml             # Project configuration
├── 📄 TruckScaleApp.spec         # PyInstaller spec
├── 📄 WeighingScaleApp.spec      # PyInstaller spec
│
├── 📄 START_APP.bat              # Windows batch launcher
├── 📄 START_APP.ps1              # PowerShell launcher
├── 📄 BUILD.bat                  # Build script
├── 📄 PORTABLE_SETUP.bat         # Portable setup script
│
├── 📁 assets/                    # Application assets
│   ├── app_icon.ico              # Application icon
│   ├── app_icon.png              # PNG icon
│   └── [other assets]
│
├── 📁 build/                     # Build output
├── 📁 hooks/                     # PyInstaller hooks
├── 📁 logs/                      # Application logs
├── 📁 exports/                   # Exported files
│
├── 📄 transactions.db            # SQLite database
├── 📄 config.json                # Configuration file
└── 📄 README.md                  # This file
```

---

## 📦 Dependencies

### Required Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `pyserial` | >=3.5 | Serial communication |
| `Pillow` | >=8.0.0 | Image processing |
| `reportlab` | >=3.6.0 | PDF generation |
| `opencv-python` | >=4.5.0 | Camera support |
| `openpyxl` | >=3.0.0 | Excel export |

### Optional Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `colorlog` | >=6.0.0 | Colored logging |
| `pystray` | >=0.19.0 | System tray support |
| `pywin32` | - | Windows printing |

### Installing Dependencies

```bash
pip install -r requirements.txt
```

Or install individually:

```bash
pip install pyserial pillow reportlab opencv-python openpyxl pywin32
```

---

## 🔧 Troubleshooting

### Common Issues

#### Scale Not Connecting

1. **Check COM Port**
   ```bash
   # View available ports in Python
   python -c "import serial.tools.list_ports; print([p.device for p in serial.tools.list_ports.comports()])"
   ```

2. **Verify Baud Rate**
   - Ensure baud rate matches scale settings (default: 9600)

3. **Test Connection**
   - Try different COM ports
   - Check cable connections
   - Verify scale is powered on

#### Weight Display Shows "No Source"

- Serial connection not established
- Check Settings → Comm Ports → Start Connection
- Verify regex pattern matches scale output format

#### Camera Not Working

1. Check camera is not in use by another application
2. Verify camera permissions in Windows Settings
3. Try refreshing camera list in Settings

#### PDF Generation Errors

1. Ensure `reportlab` is installed: `pip install reportlab`
2. Check template for invalid placeholders
3. Verify printer is installed and online

#### Database Errors

- Check write permissions for `C:\ProgramData\Truck Scale\`
- Verify SQLite database is not corrupted
- Check available disk space

### Error Messages

| Error | Solution |
|-------|----------|
| "Cannot find usable init.tcl" | Use Python 3.11.9 instead of newer versions |
| "Port already in use" | Close other applications using the COM port |
| "Database locked" | Wait for current operation to complete |
| "No module named 'tkinter'" | Install Python with Tcl/Tk support |

### Log Files

Application logs are stored in: `logs/weighing_scale_YYYYMMDD.log`

Check logs for detailed error information and debugging.

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. **Fork the Repository**
2. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Commit Your Changes**
   ```bash
   git commit -m "Add: Description of your changes"
   ```
4. **Push to Branch**
   ```bash
   git push origin feature/your-feature-name
   ```
5. **Open a Pull Request**

### Code Style

- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings for functions and classes
- Include type hints where appropriate

---

## 📄 License

This project is proprietary software. All rights reserved.

© 2024-2026 Advantechnique. All rights reserved.

For licensing inquiries, please contact: advantechnique@gmail.com

---

## 📞 Contact

**Developer**: Advantechnique

**Email**: advantechnique@gmail.com

**Support**: For technical support, please email with the subject line "Truck Scale Support"

---

## 🙏 Acknowledgments

- Python Software Foundation
- Tkinter Development Team
- ReportLab PDF Library
- OpenCV Community
- All contributors and testers

---

<div align="center">

**Made with ❤️ by Advantechnique**

[⬆ Back to Top](#-truck-scale-weighing-system)

</div>

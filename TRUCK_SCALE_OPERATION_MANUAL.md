# Truck Scale Weighing System - Operation Manual

## Table of Contents
1. [System Overview](#system-overview)
2. [Installation & Setup](#installation--setup)
3. [System Architecture](#system-architecture)
4. [User Interface Navigation](#user-interface-navigation)
5. [Core Operations](#core-operations)
6. [User Management](#user-management)
7. [Configuration Settings](#configuration-settings)
8. [Technical Specifications](#technical-specifications)
9. [Troubleshooting](#troubleshooting)
10. [Maintenance](#maintenance)

---

## System Overview

### Purpose
The Truck Scale Weighing System is a comprehensive desktop application designed to manage truck weighing operations, including weight measurement, transaction recording, user management, and report generation.

### Key Features
- **Real-time Weight Measurement**: Live weight data from electronic scales
- **Transaction Management**: Complete weighing workflow with pending and completed records
- **Multi-user Support**: Role-based access control (Admin, Operator, User)
- **Camera Integration**: Photo capture for transaction documentation
- **PDF Generation**: Customizable weighing tickets and reports
- **Price Calculation**: Automatic pricing based on weight and configured parameters
- **Data Export**: CSV export functionality for reporting
- **Serial Communication**: Support for multiple scale devices and displays

---

## Installation & Setup

### System Requirements
- **Operating System**: Windows 10/11 (64-bit)
- **Python**: Version 3.11.9 or compatible
- **Hardware**: 
  - Electronic weighing scale with serial output
  - Optional: Camera for photo capture
  - Optional: External display for weight viewing
- **Dependencies**: 
  - tkinter (included with Python)
  - PIL/Pillow for image handling
  - pyserial for serial communication
  - reportlab for PDF generation
  - opencv-python for camera support

### Installation Steps
1. **Extract Application**: Unzip the application package to desired location
2. **Install Dependencies**: 
   ```bash
   pip install opencv-python pillow pyserial pywin32 reportlab
   ```
3. **Create Data Directory**: 
   - Application automatically creates `C:\ProgramData\Truck Scale`
   - Ensure write permissions for this directory
4. **Connect Hardware**:
   - Connect weighing scale to COM port
   - Install camera drivers (if using camera)
   - Connect external display (if required)
5. **Launch Application**: Run `main.py` with Python 3.11.9

---

## System Architecture

### Module Structure
```
Truck Scale Weighing System/
├── main.py                 # Application entry point
├── config.py              # Configuration constants
├── database.py            # SQLite database operations
├── serial_manager.py      # Serial communication
├── camera_manager.py      # Camera operations
├── pdf_print_manager.py   # PDF generation and printing
├── ui_components.py       # Reusable UI components
├── messagebox.py          # Custom message dialogs
└── weighing_scale_app.py  # Main application logic
```

### Data Storage
- **Database**: SQLite database at `C:\ProgramData\Truck Scale\database.db`
- **Configuration**: JSON file at `C:\ProgramData\Truck Scale\config.json`
- **Logs**: Daily log files in `logs/` directory
- **Assets**: Icons and images in `assets/` folder

### Core Components

#### 1. Main Application (`main.py`)
- Application initialization and startup
- Icon loading and window setup
- Manager initialization and coordination

#### 2. Configuration (`config.py`)
- System constants and default values
- File paths and security settings
- Price calculation parameters
- Serial communication settings

#### 3. Database Manager (`database.py`)
- SQLite database operations
- Transaction CRUD operations
- User management
- Master data maintenance

#### 4. Serial Manager (`serial_manager.py`)
- Scale communication via serial ports
- Weight data parsing and validation
- Multiple device support (scale, emulator, display)
- Real-time weight streaming

#### 5. Camera Manager (`camera_manager.py`)
- Camera detection and connection
- Photo capture and storage
- Live video feed display
- Image management

#### 6. PDF Print Manager (`pdf_print_manager.py`)
- Custom PDF template generation
- Barcode generation
- Windows printing integration
- Ticket formatting

---

## User Interface Navigation

### Main Interface Layout
The application uses a tabbed interface with five main sections:

#### 1. Entry Form Tab
**Purpose**: Primary data entry for weighing transactions
**Components**:
- **Weight Option**: ONE WAY or TWO WAY weighing selection
- **Transaction Details**: Customizable fields (Company, Truck Plate, Product, etc.)
- **Live Scale Weight**: Real-time weight display from connected scale
- **Camera Feed**: Live video preview and photo capture
- **Action Buttons**: Save, Print, Clear, and Recall functions

#### 2. Pending Records Tab
**Purpose**: View and manage incomplete transactions
**Features**:
- List of pending transactions requiring second weighing
- Filter and search capabilities
- Complete transaction processing
- Delete invalid records

#### 3. Completed Records Tab
**Purpose**: View and manage finished transactions
**Features**:
- Complete transaction history
- Search and filter options
- Edit capabilities (for authorized users)
- Export and print functions

#### 4. Reports Tab
**Purpose**: Generate and view various reports
**Features**:
- Daily/weekly/monthly summaries
- Transaction filtering
- CSV export functionality
- Print report generation

#### 5. Settings Tab
**Purpose**: System configuration and management
**Sub-tabs**:
- **Master Data**: Manage companies, trucks, products, etc.
- **Customize Entry Form**: Configure form fields and layout
- **Comm Ports**: Serial port configuration
- **Print & Ticket Settings**: Template and printer setup
- **Admin Settings**: User management and activation

### Login System
- **Default Admin**: Username `admin`, Password `password`
- **Role-based Access**: Different permissions for Admin, Operator, User
- **Session Management**: Automatic logout after inactivity

---

## Core Operations

### Weighing Workflow

#### One-Way Weighing
1. **Preparation**:
   - Select "ONE WAY" weight option
   - Enter transaction details (Company, Truck Plate, etc.)
   - Ensure scale is connected and displaying live weight

2. **Weighing Process**:
   - Drive truck onto scale
   - Wait for weight to stabilize
   - Verify weight accuracy
   - Capture photo (if required)

3. **Transaction Completion**:
   - Click "Save" to record transaction
   - Print ticket (if required)
   - Transaction moves to Completed Records

#### Two-Way Weighing
1. **First Weighing (Gross)**:
   - Select "TWO WAY" weight option
   - Enter transaction details
   - Drive loaded truck onto scale
   - Record gross weight
   - Save as pending transaction

2. **Second Weighing (Tare)**:
   - Go to Pending Records tab
   - Select the pending transaction
   - Drive empty truck onto scale
   - Record tare weight
   - System calculates net weight automatically

3. **Transaction Completion**:
   - Review calculated net weight
   - Complete transaction
   - Print final ticket

### Price Calculation
The system supports automatic price calculation based on:
- **Base Weight**: Initial weight threshold (default: 20,000 kg)
- **Base Price**: Price for base weight (default: ₱150.00)
- **Increment Weight**: Additional weight unit (default: 100 kg)
- **Increment Price**: Price per increment (default: ₱10.00)

**Formula**:
- If weight ≤ Base Weight: Total Price = Base Price
- If weight > Base Weight: Total Price = Base Price + ((Weight - Base Weight) / Increment Weight × Increment Price)

### Camera Operations
- **Auto-connect**: System automatically detects and connects to available cameras
- **Photo Capture**: Take photos during weighing for documentation
- **Live Preview**: Real-time video feed in Entry Form
- **Image Storage**: Photos saved with transaction records

### Serial Communication
- **Scale Connection**: Connect to electronic weighing scale via COM port
- **Data Parsing**: Automatic parsing of weight data using configurable regex patterns
- **Multiple Formats**: Support for various scale data formats
- **Display Output**: Optional external display for weight viewing

---

## User Management

### User Roles

#### Admin
- **Full Access**: All system features and settings
- **User Management**: Create, edit, delete user accounts
- **System Configuration**: Access to all settings
- **Master Data**: Complete CRUD operations
- **Activation**: System activation and license management

#### Operator
- **Weighing Operations**: Full access to weighing functions
- **Transaction Management**: Create and complete transactions
- **Reports**: View and generate reports
- **Limited Settings**: Cannot access Comm Ports, Activation, or Admin Settings

#### User
- **Basic Operations**: View transactions and reports
- **Data Entry**: Limited form access
- **No Settings**: Cannot access system configuration
- **Read-only**: Cannot modify critical data

### User Creation and Management
1. **Access Admin Settings**: Go to Settings → Admin Settings
2. **Create New User**:
   - Enter username and password
   - Select user role (User, Operator, Admin)
   - Click "Save" to create account
3. **Manage Existing Users**:
   - View user list in "Manage Existing Users" section
   - Edit user details or change passwords
   - Delete user accounts (except currently logged-in admin)

### Security Features
- **Password Hashing**: Secure password storage using SHA-256
- **Role Validation**: System validates permissions for each action
- **Session Management**: Automatic logout after period of inactivity
- **Access Control**: Tab and feature restrictions based on user role

---

## Configuration Settings

### Serial Port Configuration
**Location**: Settings → Comm Ports
**Options**:
- **Main Scale Port**: COM port for primary weighing scale
- **Baud Rate**: Communication speed (default: 9600)
- **Regex Pattern**: Data parsing format for weight extraction
- **Read Interval**: Data polling frequency (default: 50ms)

**Supported Scale Formats**:
- `ww(-?\d+)` - WW format with optional minus
- `(-?\d+\.\d+)\s*kg` - Number followed by "kg"
- `ST,GS,(\d+\.\d+)` - Standard format
- `W=(\d+\.\d+)` - Weight format
- Custom patterns supported

### Master Data Management
**Location**: Settings → Master Data
**Data Types**:
- **Companies**: Transport and business companies
- **Truck Plates**: Vehicle registration information
- **Products**: Types of materials being weighed
- **Designations**: Product categories or types
- **Senders**: Origin points or suppliers
- **Origins**: Source locations
- **Destinations**: Delivery locations
- **Drivers**: Driver information and licenses

### Print and Ticket Settings
**Location**: Settings → Print & Ticket Settings
**Features**:
- **Template Design**: Custom PDF ticket templates
- **Placeholders**: Dynamic data insertion (company, weight, date, etc.)
- **Barcode Generation**: Automatic barcode creation
- **Printer Selection**: Windows printer integration
- **Preview**: Real-time template preview

### Price Calculation Settings
**Location**: Settings → Print & Ticket Settings → Price Computation
**Parameters**:
- **Enable/Disable**: Toggle price calculation on/off
- **Base Weight**: Initial weight threshold
- **Base Price**: Price for base weight
- **Increment Weight**: Additional weight unit
- **Increment Price**: Price per increment unit

### Entry Form Customization
**Location**: Settings → Customize Entry Form
**Options**:
- **Field Selection**: Choose which fields to display
- **Field Order**: Arrange fields in preferred order
- **Default Layout**: Reset to standard configuration
- **Save Configuration**: Preserve custom layout

---

## Technical Specifications

### Database Schema
**Main Tables**:
- **transactions**: Primary weighing records
- **users**: User account information
- **companies**: Company master data
- **trucks**: Vehicle information
- **products**: Product catalog
- **print_templates**: Custom ticket templates

**Transaction Record Fields**:
- id, company, truck_plate, product, designation
- sender, origin, destination, driver
- gross_weight, tare_weight, net_weight
- gross_date, gross_time, tare_date, tare_time
- weight_type, ticket_no, status, operator, timestamp

### File Structure
**Application Files**:
```
C:\ProgramData\Truck Scale\
├── database.db          # SQLite database
├── config.json          # System configuration
├── photos/              # Transaction photos
├── tickets/             # Generated PDF tickets
└── logs/                # Application logs
```

**Asset Files**:
```
assets/
├── app_icon.ico         # Application icon
├── app_icon.png         # PNG version for compatibility
└── [other assets]
```

### Performance Specifications
- **Weight Update Rate**: Up to 20Hz (50ms intervals)
- **Database Capacity**: Supports millions of transactions
- **Concurrent Users**: Single-user desktop application
- **Photo Resolution**: Configurable camera resolution
- **PDF Generation**: < 2 seconds per ticket

### Communication Protocols
- **Serial Communication**: RS-232 standard
- **Baud Rates**: 1200, 2400, 4800, 9600, 19200, 38400
- **Data Formats**: ASCII text, various scale protocols
- **Camera Interface**: USB/Integrated webcams
- **Printing**: Windows printer drivers

---

## Troubleshooting

### Common Issues

#### Scale Connection Problems
**Symptoms**: "No Source" status, no weight display
**Solutions**:
1. Check physical cable connections
2. Verify COM port number in device manager
3. Confirm correct baud rate setting
4. Test with different COM ports
5. Check scale power and operation

#### Weight Display Issues
**Symptoms**: Incorrect weight values, unstable readings
**Solutions**:
1. Adjust regex pattern for scale format
2. Check scale calibration
3. Verify weight stability settings
4. Reduce read interval if data is corrupted
5. Test with different scale if available

#### Camera Problems
**Symptoms**: No camera feed, photo capture failures
**Solutions**:
1. Check camera drivers and connections
2. Verify camera is not used by other applications
3. Test camera with Windows Camera app
4. Restart application after camera connection
5. Check camera permissions in Windows

#### Database Issues
**Symptoms**: Data loss, save failures, slow performance
**Solutions**:
1. Check disk space in ProgramData directory
2. Verify write permissions
3. Rebuild database from backup if corrupted
4. Compact database for performance
5. Check for large photo files affecting performance

#### Printing Problems
**Symptoms**: PDF generation errors, print failures
**Solutions**:
1. Verify printer installation and drivers
2. Check template syntax and placeholders
3. Test with default template
4. Verify sufficient disk space for PDF files
5. Check Windows print spooler service

### Error Messages
- **"Cannot find usable init.tcl"**: Use Python 3.11.9 instead of 3.14
- **"Port already in use"**: Close other applications using COM port
- **"Database locked"**: Wait for current operation to complete
- **"Invalid weight format"**: Adjust regex pattern for scale data
- **"Camera not found"**: Check camera connections and drivers

### Log Analysis
**Log Location**: `logs/weighing_scale_YYYYMMDD.log`
**Key Information**:
- Application startup and shutdown
- Serial connection events
- Database operations
- Error messages and stack traces
- User login/logout events

---

## Maintenance

### Daily Maintenance
- **Backup Database**: Copy `database.db` to backup location
- **Review Logs**: Check for error messages or issues
- **Clear Old Photos**: Remove unnecessary photo files
- **Verify Scale Operation**: Test weight measurement accuracy

### Weekly Maintenance
- **Compact Database**: Optimize SQLite database performance
- **Update Master Data**: Add new companies, trucks, products
- **Review User Accounts**: Remove inactive users
- **Check Disk Space**: Ensure sufficient storage for data

### Monthly Maintenance
- **Full System Backup**: Complete application and data backup
- **Scale Calibration**: Professional scale maintenance
- **Security Review**: Update passwords and user permissions
- **Performance Review**: Analyze system speed and responsiveness

### Annual Maintenance
- **System Update**: Update Python and dependencies
- **Hardware Check**: Verify all equipment functionality
- **Database Archive**: Archive old transactions if needed
- **Training Refresh**: User training and procedure updates

### Backup Procedures
**Critical Files to Backup**:
1. `database.db` - All transaction data
2. `config.json` - System configuration
3. `photos/` directory - Transaction photos
4. Custom templates and reports

**Backup Schedule**:
- **Daily**: Automatic database backup
- **Weekly**: Full system backup
- **Before Updates**: Complete system backup

### Security Maintenance
- **Password Policy**: Regular password updates
- **Access Review**: Periodic user permission audit
- **Log Monitoring**: Review security-related log entries
- **Data Protection**: Ensure proper data encryption and access

---

## Appendix

### Default Configuration Values
- **Base Weight**: 20,000 kg
- **Base Price**: ₱150.00
- **Increment Weight**: 100 kg
- **Increment Price**: ₱10.00
- **Max Weight Deviation**: 10.0
- **Required Weight Stability**: 3 readings
- **Default Baud Rate**: 9600
- **Read Interval**: 50ms

### Keyboard Shortcuts
- **Ctrl+S**: Save current transaction
- **Ctrl+P**: Print ticket
- **Ctrl+E**: Export data to CSV
- **F5**: Refresh data lists
- **Esc**: Cancel current operation

### Support Information
- **Application Version**: Current version information in About dialog
- **Python Version**: 3.11.9 recommended
- **Contact Information**: System administrator for support
- **Documentation**: This manual and in-application help

---

*This manual covers all aspects of the Truck Scale Weighing System operation. For specific technical issues or advanced configuration, consult the system administrator or technical support.*

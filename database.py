"""
Database operations module for the Truck Scale Weighing System.
Handles all SQLite database operations including initialization, CRUD operations,
and data management.
"""

import sqlite3
import logging
from typing import List, Dict, Optional, Tuple, Any
from datetime import datetime

from config import DB_FILE, ADMIN_USERNAME, ADMIN_PASSWORD_HASH


class DatabaseManager:
    """Manages all database operations for the weighing scale application."""
    
    def __init__(self, msg_box=None):
        """Initialize the database manager with an optional message box for error reporting."""
        self.msg_box = msg_box
        self.init_database()
    
    def init_database(self):
        """
        Initializes the SQLite database with the necessary tables if they don't exist.
        This includes the main 'transactions' table, 'users' table, master data tables,
        and a new table for print templates.
        """
        try:
            with sqlite3.connect(DB_FILE) as conn:
                cursor = conn.cursor()
                
                # Create main transactions table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS transactions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        company TEXT, truck_plate TEXT, product TEXT,
                        designation TEXT, sender TEXT, origin TEXT, destination TEXT, driver TEXT,
                        gross_weight REAL, tare_weight REAL, net_weight REAL,
                        gross_date TEXT, gross_time TEXT,
                        tare_date TEXT, tare_time TEXT,
                        weight_type TEXT,
                        ticket_no INTEGER,
                        status TEXT,
                        operator TEXT,
                        operator2 TEXT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Create indexes for better performance
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_truck_plate_status ON transactions (truck_plate, status)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON transactions (timestamp DESC)")
                
                # Create users table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        username TEXT PRIMARY KEY,
                        password_hash TEXT NOT NULL,
                        role TEXT DEFAULT 'user'
                    )
                """)
                
                # Insert default admin user if table is empty
                cursor.execute("SELECT COUNT(*) FROM users")
                if cursor.fetchone()[0] == 0:
                    cursor.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                                   (ADMIN_USERNAME, ADMIN_PASSWORD_HASH, 'admin'))
                    # Don't show success message to avoid OK button before login
                    # if self.msg_box:
                    #     self.msg_box.showinfo("Database", "Default admin user created successfully.")

                # Create master data tables
                master_tables = [
                    ("companies", "name"),
                    ("trucks", "name"),
                    ("products", "name"),
                    ("drivers", "name"),
                    ("origins", "name"),
                    ("destinations", "name"),
                    ("designations", "name"),
                    ("senders", "name")
                ]
                
                for table, column in master_tables:
                    cursor.execute(f"""
                        CREATE TABLE IF NOT EXISTS {table} (
                            name TEXT UNIQUE COLLATE NOCASE,
                            id INTEGER PRIMARY KEY AUTOINCREMENT
                        )
                    """)
                    cursor.execute(f"CREATE INDEX IF NOT EXISTS idx_{table}_name ON {table} (name)")

                # Create print templates table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS print_templates (
                        template_name TEXT PRIMARY KEY,
                        template_content TEXT NOT NULL
                    )
                """)
                
                # Initialize empty templates if table is empty
                cursor.execute("SELECT COUNT(*) FROM print_templates")
                if cursor.fetchone()[0] == 0:
                    cursor.execute("INSERT INTO print_templates (template_name, template_content) VALUES (?, ?)", 
                                   ("ONE_WAY", ""))
                    cursor.execute("INSERT INTO print_templates (template_name, template_content) VALUES (?, ?)", 
                                   ("TWO_WAY", ""))
                
                # Migration: Add operator columns if they don't exist
                cursor.execute("PRAGMA table_info(transactions)")
                columns = [col[1] for col in cursor.fetchall()]
                if 'operator' not in columns:
                    cursor.execute("ALTER TABLE transactions ADD COLUMN operator TEXT")
                if 'operator2' not in columns:
                    cursor.execute("ALTER TABLE transactions ADD COLUMN operator2 TEXT")
                
                # Migration: Add price columns if they don't exist
                if 'unit_price' not in columns:
                    cursor.execute("ALTER TABLE transactions ADD COLUMN unit_price REAL")
                if 'total_price' not in columns:
                    cursor.execute("ALTER TABLE transactions ADD COLUMN total_price REAL")
                if 'gross_total_price' not in columns:
                    cursor.execute("ALTER TABLE transactions ADD COLUMN gross_total_price REAL")
                if 'tare_total_price' not in columns:
                    cursor.execute("ALTER TABLE transactions ADD COLUMN tare_total_price REAL")
                    
                conn.commit()
                
                # Don't show success message to avoid OK button before login
                # if self.msg_box:
                #     self.msg_box.showinfo("Database", "Database initialized successfully.")
        except sqlite3.Error as e:
            error_msg = f"Failed to initialize database: {e}"
            logging.error(error_msg)
            if self.msg_box:
                self.msg_box.showerror("Database Error", error_msg)
            raise

    def save_transaction(self, transaction_data: Dict[str, Any]) -> Optional[int]:
        """
        Save a transaction to the database.
        
        Args:
            transaction_data: Dictionary containing transaction data
            
        Returns:
            The ID of the inserted transaction, or None if failed
        """
        try:
            with sqlite3.connect(DB_FILE) as conn:
                cursor = conn.cursor()
                
                # Prepare the SQL statement based on the data provided
                columns = list(transaction_data.keys())
                placeholders = ', '.join(['?' for _ in columns])
                values = list(transaction_data.values())
                
                sql = f"INSERT INTO transactions ({', '.join(columns)}) VALUES ({placeholders})"
                cursor.execute(sql, values)
                
                transaction_id = cursor.lastrowid
                conn.commit()
                
                return transaction_id
        except sqlite3.Error as e:
            error_msg = f"Failed to save transaction: {e}"
            logging.error(error_msg)
            if self.msg_box:
                self.msg_box.showerror("Database Error", error_msg)
            return None

    def get_transaction(self, transaction_id: int) -> Optional[Dict[str, Any]]:
        """
        Retrieve a specific transaction by ID.
        
        Args:
            transaction_id: The ID of the transaction to retrieve
            
        Returns:
            Dictionary containing transaction data, or None if not found
        """
        try:
            with sqlite3.connect(DB_FILE) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                cursor.execute("SELECT * FROM transactions WHERE id = ?", (transaction_id,))
                row = cursor.fetchone()
                
                if row:
                    return dict(row)
                return None
        except sqlite3.Error as e:
            error_msg = f"Failed to retrieve transaction: {e}"
            logging.error(error_msg)
            if self.msg_box:
                self.msg_box.showerror("Database Error", error_msg)
            return None

    def search_transactions(self, filters: Dict[str, Any] = None, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Search transactions with optional filters.
        
        Args:
            filters: Dictionary of filter conditions
            limit: Maximum number of results to return
            
        Returns:
            List of transaction dictionaries
        """
        try:
            with sqlite3.connect(DB_FILE) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                sql = "SELECT * FROM transactions WHERE 1=1"
                params = []
                
                if filters:
                    for column, value in filters.items():
                        if value:
                            sql += f" AND {column} LIKE ?"
                            params.append(f"%{value}%")
                
                sql += " ORDER BY timestamp DESC LIMIT ?"
                params.append(limit)
                
                cursor.execute(sql, params)
                rows = cursor.fetchall()
                
                return [dict(row) for row in rows]
        except sqlite3.Error as e:
            error_msg = f"Failed to search transactions: {e}"
            logging.error(error_msg)
            if self.msg_box:
                self.msg_box.showerror("Database Error", error_msg)
            return []

    def get_master_data(self, table_name: str) -> List[str]:
        """
        Get all names from a master data table.
        
        Args:
            table_name: Name of the master data table
            
        Returns:
            List of names from the table
        """
        try:
            with sqlite3.connect(DB_FILE) as conn:
                cursor = conn.cursor()
                cursor.execute(f"SELECT name FROM {table_name} ORDER BY name COLLATE NOCASE")
                return [row[0] for row in cursor.fetchall()]
        except sqlite3.Error as e:
            error_msg = f"Failed to get master data from {table_name}: {e}"
            logging.error(error_msg)
            if self.msg_box:
                self.msg_box.showerror("Database Error", error_msg)
            return []

    def add_master_data(self, table_name: str, name: str) -> bool:
        """
        Add a new entry to a master data table.
        
        Args:
            table_name: Name of the master data table
            name: Name to add
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with sqlite3.connect(DB_FILE) as conn:
                cursor = conn.cursor()
                cursor.execute(f"INSERT OR IGNORE INTO {table_name} (name) VALUES (?)", (name,))
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            error_msg = f"Failed to add master data to {table_name}: {e}"
            logging.error(error_msg)
            if self.msg_box:
                self.msg_box.showerror("Database Error", error_msg)
            return False

    def save_print_template(self, template_name: str, template_content: str) -> bool:
        """
        Save a print template to the database.
        
        Args:
            template_name: Name of the template
            template_content: Content of the template
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with sqlite3.connect(DB_FILE) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT OR REPLACE INTO print_templates (template_name, template_content) VALUES (?, ?)",
                    (template_name, template_content)
                )
                conn.commit()
                return True
        except sqlite3.Error as e:
            error_msg = f"Failed to save print template: {e}"
            logging.error(error_msg)
            if self.msg_box:
                self.msg_box.showerror("Database Error", error_msg)
            return False

    def get_print_template(self, template_name: str) -> Optional[str]:
        """
        Get a print template from the database.
        
        Args:
            template_name: Name of the template
            
        Returns:
            Template content, or None if not found
        """
        try:
            with sqlite3.connect(DB_FILE) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT template_content FROM print_templates WHERE template_name = ?",
                    (template_name,)
                )
                row = cursor.fetchone()
                return row[0] if row else None
        except sqlite3.Error as e:
            error_msg = f"Failed to get print template: {e}"
            logging.error(error_msg)
            if self.msg_box:
                self.msg_box.showerror("Database Error", error_msg)
            return None

    def load_print_templates(self) -> dict:
        """
        Load all print templates from the database.
        
        Returns:
            Dictionary with template names as keys and template content as values
        """
        try:
            with sqlite3.connect(DB_FILE) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT template_name, template_content FROM print_templates")
                templates = {}
                for row in cursor.fetchall():
                    templates[row[0]] = row[1]
                return templates
        except sqlite3.Error as e:
            error_msg = f"Failed to load print templates: {e}"
            logging.error(error_msg)
            if self.msg_box:
                self.msg_box.showerror("Database Error", error_msg)
            return {}

    def authenticate_user(self, username: str, password_hash: str) -> Optional[str]:
        """
        Authenticate a user against the database.
        
        Args:
            username: Username to authenticate
            password_hash: Hashed password to verify
            
        Returns:
            User role if authentication successful, None otherwise
        """
        try:
            with sqlite3.connect(DB_FILE) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT role FROM users WHERE username = ? AND password_hash = ?",
                    (username, password_hash)
                )
                row = cursor.fetchone()
                return row[0] if row else None
        except sqlite3.Error as e:
            error_msg = f"Failed to authenticate user: {e}"
            logging.error(error_msg)
            if self.msg_box:
                self.msg_box.showerror("Database Error", error_msg)
            return None

    def update_transaction(self, transaction_id: int, update_data: Dict[str, Any]) -> bool:
        """
        Update a transaction with new data.
        
        Args:
            transaction_id: ID of the transaction to update
            update_data: Dictionary of fields to update
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with sqlite3.connect(DB_FILE) as conn:
                cursor = conn.cursor()
                
                set_clause = ', '.join([f"{key} = ?" for key in update_data.keys()])
                values = list(update_data.values()) + [transaction_id]
                
                cursor.execute(
                    f"UPDATE transactions SET {set_clause} WHERE id = ?",
                    values
                )
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            error_msg = f"Failed to update transaction: {e}"
            logging.error(error_msg)
            if self.msg_box:
                self.msg_box.showerror("Database Error", error_msg)
            return False

    def delete_transaction(self, transaction_id: int) -> bool:
        """
        Delete a transaction from the database.
        
        Args:
            transaction_id: ID of the transaction to delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with sqlite3.connect(DB_FILE) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            error_msg = f"Failed to delete transaction: {e}"
            logging.error(error_msg)
            if self.msg_box:
                self.msg_box.showerror("Database Error", error_msg)
            return False

    def insert_transaction(self, transaction_data: Dict[str, Any]) -> Optional[int]:
        """
        Insert a transaction with validated columns.
        
        Args:
            transaction_data: Dictionary containing transaction data
            
        Returns:
            The ID of the inserted transaction, or None if failed
        """
        # Valid columns for the transactions table
        valid_columns = {
            'company', 'truck_plate', 'product', 'designation', 'sender', 
            'origin', 'destination', 'driver', 'gross_weight', 'tare_weight', 
            'net_weight', 'gross_date', 'gross_time', 'tare_date', 'tare_time',
            'weight_type', 'ticket_no', 'status', 'operator', 'operator2',
            'unit_price', 'total_price', 'gross_total_price', 'tare_total_price',
            'timestamp'
        }
        
        try:
            with sqlite3.connect(DB_FILE) as conn:
                cursor = conn.cursor()
                
                # Filter to only valid columns
                filtered_data = {k: v for k, v in transaction_data.items() if k in valid_columns}
                
                if not filtered_data:
                    logging.error("No valid columns provided for transaction insert")
                    return None
                
                columns = list(filtered_data.keys())
                placeholders = ', '.join(['?' for _ in columns])
                values = list(filtered_data.values())
                
                sql = f"INSERT INTO transactions ({', '.join(columns)}) VALUES ({placeholders})"
                cursor.execute(sql, values)
                
                transaction_id = cursor.lastrowid
                conn.commit()
                
                return transaction_id
        except sqlite3.Error as e:
            error_msg = f"Failed to insert transaction: {e}"
            logging.error(error_msg)
            if self.msg_box:
                self.msg_box.showerror("Database Error", error_msg)
            return None

    def get_transaction_by_ticket(self, ticket_no: int) -> Optional[Dict[str, Any]]:
        """
        Retrieve a specific transaction by ticket number.
        
        Args:
            ticket_no: The ticket number of the transaction to retrieve
            
        Returns:
            Dictionary containing transaction data, or None if not found
        """
        try:
            with sqlite3.connect(DB_FILE) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                cursor.execute("SELECT * FROM transactions WHERE ticket_no = ?", (ticket_no,))
                row = cursor.fetchone()
                
                if row:
                    return dict(row)
                return None
        except sqlite3.Error as e:
            error_msg = f"Failed to retrieve transaction by ticket: {e}"
            logging.error(error_msg)
            if self.msg_box:
                self.msg_box.showerror("Database Error", error_msg)
            return None

    def get_transactions_paginated(
        self, 
        offset: int = 0, 
        limit: int = 50, 
        status: str = None,
        date_from: str = None,
        date_to: str = None,
        search_query: str = None
    ) -> Tuple[List[Dict[str, Any]], int]:
        """
        Get transactions with pagination and filtering.
        
        Args:
            offset: Offset for pagination
            limit: Maximum number of results
            status: Filter by status
            date_from: Start date filter (YYYY-MM-DD)
            date_to: End date filter (YYYY-MM-DD)
            search_query: Search term for truck_plate, company, product
            
        Returns:
            Tuple of (list of transactions, total count)
        """
        try:
            with sqlite3.connect(DB_FILE) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                # Build query
                where_clauses = []
                params = []
                
                if status:
                    where_clauses.append("status = ?")
                    params.append(status)
                
                if date_from:
                    where_clauses.append("gross_date >= ?")
                    params.append(date_from)
                
                if date_to:
                    where_clauses.append("gross_date <= ?")
                    params.append(date_to)
                
                if search_query:
                    search_pattern = f"%{search_query}%"
                    where_clauses.append(
                        "(truck_plate LIKE ? OR company LIKE ? OR product LIKE ? OR driver LIKE ?)"
                    )
                    params.extend([search_pattern] * 4)
                
                where_clause = " AND ".join(where_clauses) if where_clauses else "1=1"
                
                # Get total count
                count_sql = f"SELECT COUNT(*) FROM transactions WHERE {where_clause}"
                cursor.execute(count_sql, params)
                result = cursor.fetchone()
                total_count = result[0] if result else 0
                
                # Get paginated results
                sql = f"""
                    SELECT * FROM transactions 
                    WHERE {where_clause}
                    ORDER BY timestamp DESC 
                    LIMIT ? OFFSET ?
                """
                cursor.execute(sql, params + [limit, offset])
                rows = cursor.fetchall()
                
                return [dict(row) for row in rows], total_count
                
        except sqlite3.Error as e:
            error_msg = f"Failed to get paginated transactions: {e}"
            logging.error(error_msg)
            if self.msg_box:
                self.msg_box.showerror("Database Error", error_msg)
            return [], 0

    def get_transaction_count(self, status: str = None) -> int:
        """
        Get total transaction count.
        
        Args:
            status: Optional status filter
            
        Returns:
            Count of transactions
        """
        try:
            with sqlite3.connect(DB_FILE) as conn:
                cursor = conn.cursor()
                
                if status:
                    cursor.execute("SELECT COUNT(*) FROM transactions WHERE status = ?", (status,))
                else:
                    cursor.execute("SELECT COUNT(*) FROM transactions")
                
                result = cursor.fetchone()
                return result[0] if result else 0
        except sqlite3.Error as e:
            logging.error(f"Failed to get transaction count: {e}")
            return 0

    def get_daily_summary(self, date: str) -> Dict[str, Any]:
        """
        Get summary statistics for a specific date.
        
        Args:
            date: Date in YYYY-MM-DD format
            
        Returns:
            Dictionary with summary statistics
        """
        try:
            with sqlite3.connect(DB_FILE) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT 
                        COUNT(*) as total_transactions,
                        SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) as completed,
                        SUM(CASE WHEN status = 'Cancelled' THEN 1 ELSE 0 END) as cancelled,
                        COALESCE(SUM(net_weight), 0) as total_net_weight
                    FROM transactions 
                    WHERE gross_date = ? OR tare_date = ?
                """, (date, date))
                
                result = cursor.fetchone()
                
                return {
                    "date": date,
                    "total_transactions": result[0] if result else 0,
                    "completed": result[1] if result else 0,
                    "cancelled": result[2] if result else 0,
                    "total_net_weight": result[3] if result else 0.0
                }
        except sqlite3.Error as e:
            logging.error(f"Failed to get daily summary: {e}")
            return {
                "date": date,
                "total_transactions": 0,
                "completed": 0,
                "cancelled": 0,
                "total_net_weight": 0.0
            }

    def get_date_range_summary(self, date_from: str, date_to: str) -> Dict[str, Any]:
        """
        Get summary statistics for a date range.
        
        Args:
            date_from: Start date in YYYY-MM-DD format
            date_to: End date in YYYY-MM-DD format
            
        Returns:
            Dictionary with summary statistics
        """
        try:
            with sqlite3.connect(DB_FILE) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT 
                        COUNT(*) as total_transactions,
                        SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) as completed,
                        SUM(CASE WHEN status = 'Cancelled' THEN 1 ELSE 0 END) as cancelled,
                        COALESCE(SUM(net_weight), 0) as total_net_weight
                    FROM transactions 
                    WHERE gross_date BETWEEN ? AND ?
                """, (date_from, date_to))
                
                result = cursor.fetchone()
                
                return {
                    "date_from": date_from,
                    "date_to": date_to,
                    "total_transactions": result[0] if result else 0,
                    "completed": result[1] if result else 0,
                    "cancelled": result[2] if result else 0,
                    "total_net_weight": result[3] if result else 0.0
                }
        except sqlite3.Error as e:
            logging.error(f"Failed to get date range summary: {e}")
            return {
                "date_from": date_from,
                "date_to": date_to,
                "total_transactions": 0,
                "completed": 0,
                "cancelled": 0,
                "total_net_weight": 0.0
            }

    def get_next_ticket_number(self) -> int:
        """
        Get the next available ticket number.
        
        Returns:
            Next ticket number to use
        """
        try:
            with sqlite3.connect(DB_FILE) as conn:
                cursor = conn.cursor()
                
                # Check if table is empty
                cursor.execute("SELECT COUNT(*) FROM transactions")
                result = cursor.fetchone()
                count = result[0] if result else 0
                
                if count == 0:
                    return 1000  # Default starting number
                
                # Get max ticket number
                cursor.execute("SELECT MAX(ticket_no) FROM transactions")
                result = cursor.fetchone()
                max_ticket = result[0] if result else 0
                
                return (max_ticket or 0) + 1
        except sqlite3.Error as e:
            logging.error(f"Failed to get next ticket number: {e}")
            return int(datetime.now().strftime("%Y%m%d%H%M%S"))  # Fallback

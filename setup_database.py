#!/usr/bin/env python3
"""
Database setup script for the Truck Scale Weighing System.
This script checks the database and creates default users if needed.
"""

import sqlite3
import os
import sys
import hashlib

# Database path
DB_FILE = r"C:\ProgramData\Truck Scale\database.db"

def create_default_users():
    """Create default users in the database."""
    try:
        # Connect to database
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # Check if users table exists
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='users'
        """)
        
        if not cursor.fetchone():
            # Create users table
            cursor.execute("""
                CREATE TABLE users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    role TEXT NOT NULL DEFAULT 'operator',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            print("Created users table")
        
        # Check if any users exist
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        
        if user_count == 0:
            # Create default admin user
            admin_password = "password"
            admin_hash = hashlib.sha256(admin_password.encode()).hexdigest()
            
            cursor.execute("""
                INSERT INTO users (username, password_hash, role) 
                VALUES (?, ?, ?)
            """, ("admin", admin_hash, "admin"))
            
            # Create default operator user
            operator_password = "operator"
            operator_hash = hashlib.sha256(operator_password.encode()).hexdigest()
            
            cursor.execute("""
                INSERT INTO users (username, password_hash, role) 
                VALUES (?, ?, ?)
            """, ("operator", operator_hash, "operator"))
            
            conn.commit()
            print(f"Created default users:")
            print(f"  Admin: username='admin', password='{admin_password}'")
            print(f"  Operator: username='operator', password='{operator_password}'")
        else:
            # List existing users
            cursor.execute("SELECT username, role FROM users")
            users = cursor.fetchall()
            print(f"Existing users ({user_count}):")
            for username, role in users:
                print(f"  {username} ({role})")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"Error setting up database: {e}")
        return False

def main():
    """Main function."""
    print("Database Setup Script")
    print("=" * 50)
    
    # Check if database file exists
    if not os.path.exists(DB_FILE):
        print(f"Database file not found: {DB_FILE}")
        return 1
    
    print(f"Database file found: {DB_FILE}")
    
    # Create default users if needed
    if create_default_users():
        print("\nDatabase setup completed successfully!")
        print("You can now start the application.")
        return 0
    else:
        print("\nDatabase setup failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())

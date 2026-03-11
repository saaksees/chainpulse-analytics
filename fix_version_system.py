#!/usr/bin/env python3
"""
Fix the version management system
"""

import os
import sqlite3
import pandas as pd
from datetime import datetime
import json

def fix_database():
    """Fix and reinitialize the database"""
    print("🔧 FIXING VERSION MANAGEMENT SYSTEM")
    print("=" * 50)
    
    # Database path
    db_path = 'chainpulse.db'
    
    # Remove old database if it exists
    if os.path.exists(db_path):
        os.remove(db_path)
        print("🗑️ Removed old database")
    
    # Create new database
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Create dataset_versions table
    c.execute("""CREATE TABLE dataset_versions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        version_number TEXT NOT NULL,
        filename TEXT NOT NULL,
        uploaded_by TEXT NOT NULL,
        uploaded_at TEXT NOT NULL,
        total_rows INTEGER DEFAULT 0,
        total_revenue REAL DEFAULT 0,
        late_rate REAL DEFAULT 0,
        date_range TEXT DEFAULT '',
        is_active INTEGER DEFAULT 0,
        folder_path TEXT DEFAULT '',
        notes TEXT DEFAULT ''
    )""")
    
    print("✅ Created dataset_versions table")
    
    # Create other tables
    tables = [
        ("orders", """CREATE TABLE orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            version_id INTEGER NOT NULL,
            order_id TEXT,
            order_date TEXT,
            sales REAL,
            customer_id TEXT,
            delivery_status TEXT,
            shipping_mode TEXT,
            category TEXT,
            region TEXT
        )"""),
        
        ("risk_scores", """CREATE TABLE risk_scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            version_id INTEGER NOT NULL,
            order_id TEXT,
            risk_score REAL,
            risk_level TEXT,
            predicted_late INTEGER
        )"""),
        
        ("forecasts", """CREATE TABLE forecasts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            
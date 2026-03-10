import sqlite3
import os
import json
from datetime import datetime

# Get the directory where this file is located (app/)
current_dir = os.path.dirname(os.path.abspath(__file__))
# Go up one level to the project root (supply-chain-analytics/)
project_root = os.path.dirname(current_dir)
# Set database file in project root
DB_FILE = os.path.join(project_root, 'chainpulse.db')

# ── Connection ───────────────────────
def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

# ── Initialize all tables ────────────
def init_db():
    print(f"Initializing database at: {DB_FILE}")
    conn = get_db()
    c = conn.cursor()
    
    # Create tables one by one to avoid issues
    tables = [
        ("dataset_versions", """CREATE TABLE IF NOT EXISTS dataset_versions (
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
        )"""),
        
        ("orders", """CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            version_id INTEGER NOT NULL,
            order_id TEXT,
            order_date TEXT,
            sales REAL,
            customer_id TEXT,
            delivery_status TEXT,
            shipping_mode TEXT,
            category TEXT,
            region TEXT,
            late_delivery_risk INTEGER,
            profit REAL,
            quantity INTEGER,
            FOREIGN KEY (version_id) REFERENCES dataset_versions(id)
        )"""),
        
        ("risk_scores", """CREATE TABLE IF NOT EXISTS risk_scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            version_id INTEGER NOT NULL,
            order_id TEXT,
            risk_level TEXT,
            probability REAL,
            revenue_at_risk REAL,
            shipping_mode TEXT,
            region TEXT,
            category TEXT,
            FOREIGN KEY (version_id) REFERENCES dataset_versions(id)
        )"""),
        
        ("forecasts", """CREATE TABLE IF NOT EXISTS forecasts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            version_id INTEGER NOT NULL,
            category TEXT,
            forecast_date TEXT,
            predicted_sales REAL,
            lower_bound REAL,
            upper_bound REAL,
            FOREIGN KEY (version_id) REFERENCES dataset_versions(id)
        )"""),
        
        ("customer_segments", """CREATE TABLE IF NOT EXISTS customer_segments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            version_id INTEGER NOT NULL,
            customer_id TEXT,
            segment TEXT,
            recency INTEGER,
            frequency INTEGER,
            monetary REAL,
            rfm_score TEXT,
            FOREIGN KEY (version_id) REFERENCES dataset_versions(id)
        )""")
    ]
    
    # Execute each table creation
    for table_name, table_sql in tables:
        try:
            c.execute(table_sql)
            print(f"✅ Created table: {table_name}")
        except Exception as e:
            print(f"❌ Error creating table {table_name}: {e}")
    
    # Create indexes
    indexes = [
        ("idx_orders_version", "CREATE INDEX IF NOT EXISTS idx_orders_version ON orders(version_id)"),
        ("idx_risk_version", "CREATE INDEX IF NOT EXISTS idx_risk_version ON risk_scores(version_id)"),
        ("idx_forecast_version", "CREATE INDEX IF NOT EXISTS idx_forecast_version ON forecasts(version_id)"),
        ("idx_segments_version", "CREATE INDEX IF NOT EXISTS idx_segments_version ON customer_segments(version_id)")
    ]
    
    for index_name, index_sql in indexes:
        try:
            c.execute(index_sql)
            print(f"✅ Created index: {index_name}")
        except Exception as e:
            print(f"❌ Error creating index {index_name}: {e}")
    
    conn.commit()
    conn.close()
    print("✅ Database initialized: chainpulse.db")

# ── Version operations ───────────────
def create_version(filename, uploaded_by, rows, revenue, late_rate, date_range):
    conn = get_db()
    c = conn.cursor()
    
    # Get next version number
    c.execute("""SELECT COUNT(*) FROM dataset_versions""")
    count = c.fetchone()[0]
    version_num = f"v{count + 1}"
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    folder = f"data/versions/{version_num}_{timestamp}"
    
    c.execute("""
        INSERT INTO dataset_versions 
        (version_number, filename, uploaded_by, uploaded_at, total_rows, 
         total_revenue, late_rate, date_range, is_active, folder_path)
        VALUES (?,?,?,?,?,?,?,?,0,?)
    """, (version_num, filename, uploaded_by, 
          datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
          rows, revenue, late_rate, date_range, folder))
    
    version_id = c.lastrowid
    conn.commit()
    conn.close()
    
    # Create version folder
    os.makedirs(folder, exist_ok=True)
    return version_id, version_num, folder

def set_active_version(version_id):
    conn = get_db()
    c = conn.cursor()
    
    # Deactivate all
    c.execute("""UPDATE dataset_versions SET is_active = 0""")
    
    # Activate selected
    c.execute("""UPDATE dataset_versions SET is_active = 1 WHERE id = ?""", (version_id,))
    
    conn.commit()
    conn.close()
    
    # Update current.txt
    os.makedirs('data/versions', exist_ok=True)
    with open('data/versions/current.txt', 'w') as f:
        f.write(str(version_id))

def get_active_version():
    conn = get_db()
    c = conn.cursor()
    c.execute("""
        SELECT * FROM dataset_versions 
        WHERE is_active = 1 
        ORDER BY id DESC LIMIT 1
    """)
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None

def get_all_versions():
    conn = get_db()
    c = conn.cursor()
    c.execute("""SELECT * FROM dataset_versions ORDER BY id DESC""")
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_version_by_id(version_id):
    conn = get_db()
    c = conn.cursor()
    c.execute("""SELECT * FROM dataset_versions WHERE id = ?""", (version_id,))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None

# ── Data insertion ───────────────────
def insert_orders(version_id, df):
    conn = get_db()
    
    # Map columns flexibly
    col_map = {
        'order_id': ['Order Id', 'order_id'],
        'order_date': ['order date (DateOrders)', 'order_date'],
        'sales': ['Sales', 'sales'],
        'customer_id': ['Customer Id', 'customer_id'],
        'delivery_status': ['Delivery Status', 'delivery_status'],
        'shipping_mode': ['Shipping Mode', 'shipping_mode'],
        'category': ['Category Name', 'category'],
        'region': ['Order Region', 'region'],
        'late_delivery_risk': ['Late_delivery_risk', 'late_delivery_risk'],
        'profit': ['Order Profit Per Order', 'profit'],
        'quantity': ['Order Item Quantity', 'quantity']
    }
    
    rows = []
    for _, row in df.iterrows():
        r = {'version_id': version_id}
        for key, possible_cols in col_map.items():
            val = None
            for col in possible_cols:
                if col in df.columns:
                    val = row[col]
                    break
            r[key] = val
        rows.append(r)
    
    conn.executemany("""
        INSERT INTO orders 
        (version_id, order_id, order_date, sales, customer_id, delivery_status,
         shipping_mode, category, region, late_delivery_risk, profit, quantity)
        VALUES 
        (:version_id, :order_id, :order_date, :sales, :customer_id, :delivery_status,
         :shipping_mode, :category, :region, :late_delivery_risk, :profit, :quantity)
    """, rows)
    
    conn.commit()
    conn.close()

def insert_risk_scores(version_id, df):
    conn = get_db()
    rows = []
    for _, row in df.iterrows():
        rows.append({
            'version_id': version_id,
            'order_id': row.get('Order Id', row.get('order_id', '')),
            'risk_level': row.get('Risk_Level', row.get('risk_level', '')),
            'probability': row.get('Risk_Probability', row.get('probability', 0)),
            'revenue_at_risk': row.get('Sales', row.get('sales', 0)),
            'shipping_mode': row.get('Shipping Mode', row.get('shipping_mode', '')),
            'region': row.get('Order Region', row.get('region', '')),
            'category': row.get('Category Name', row.get('category', ''))
        })
    
    conn.executemany("""
        INSERT INTO risk_scores
        (version_id, order_id, risk_level, probability, revenue_at_risk,
         shipping_mode, region, category)
        VALUES
        (:version_id, :order_id, :risk_level, :probability, :revenue_at_risk,
         :shipping_mode, :region, :category)
    """, rows)
    
    conn.commit()
    conn.close()

def insert_forecasts(version_id, df):
    conn = get_db()
    rows = []
    for _, row in df.iterrows():
        rows.append({
            'version_id': version_id,
            'category': row.get('Category', row.get('category', '')),
            'forecast_date': str(row.get('Date', row.get('ds', ''))),
            'predicted_sales': row.get('Predicted_Sales', row.get('yhat', 0)),
            'lower_bound': row.get('Lower_Bound', row.get('yhat_lower', 0)),
            'upper_bound': row.get('Upper_Bound', row.get('yhat_upper', 0))
        })
    
    conn.executemany("""
        INSERT INTO forecasts
        (version_id, category, forecast_date, predicted_sales, lower_bound, upper_bound)
        VALUES
        (:version_id, :category, :forecast_date, :predicted_sales, :lower_bound, :upper_bound)
    """, rows)
    
    conn.commit()
    conn.close()

def insert_segments(version_id, df):
    conn = get_db()
    rows = []
    for _, row in df.iterrows():
        rows.append({
            'version_id': version_id,
            'customer_id': row.get('Customer Id', row.get('customer_id', '')),
            'segment': row.get('Segment', row.get('segment', '')),
            'recency': row.get('Recency', 0),
            'frequency': row.get('Frequency', 0),
            'monetary': row.get('Monetary', 0),
            'rfm_score': row.get('RFM_Score', '')
        })
    
    conn.executemany("""
        INSERT INTO customer_segments
        (version_id, customer_id, segment, recency, frequency, monetary, rfm_score)
        VALUES
        (:version_id, :customer_id, :segment, :recency, :frequency, :monetary, :rfm_score)
    """, rows)
    
    conn.commit()
    conn.close()

# ── Query helpers ────────────────────
def query_version_stats(version_id):
    conn = get_db()
    c = conn.cursor()
    stats = {}
    
    # Orders stats
    c.execute("""
        SELECT COUNT(*) as total,
               SUM(sales) as revenue,
               AVG(CASE WHEN delivery_status LIKE '%Late%' THEN 1.0 ELSE 0.0 END) * 100 as late_rate
        FROM orders WHERE version_id=?
    """, (version_id,))
    row = c.fetchone()
    if row:
        stats['total_orders'] = row['total']
        stats['total_revenue'] = round(row['revenue'] or 0, 2)
        stats['late_rate'] = round(row['late_rate'] or 0, 1)
    
    # Risk stats
    c.execute("""
        SELECT risk_level, COUNT(*) as cnt, SUM(revenue_at_risk) as rev
        FROM risk_scores WHERE version_id=?
        GROUP BY risk_level
    """, (version_id,))
    risk_rows = c.fetchall()
    stats['risk_breakdown'] = {
        r['risk_level']: {
            'count': r['cnt'],
            'revenue': round(r['rev'] or 0, 2)
        } for r in risk_rows
    }
    
    # Segment stats
    c.execute("""
        SELECT segment, COUNT(*) as cnt
        FROM customer_segments WHERE version_id=?
        GROUP BY segment
    """, (version_id,))
    seg_rows = c.fetchall()
    stats['segments'] = {r['segment']: r['cnt'] for r in seg_rows}
    
    conn.close()
    return stats
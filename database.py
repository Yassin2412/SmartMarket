import sqlite3


DATABASE_NAME = "smartmarket.db"


# ===========================
# Database Connection
# ===========================

def get_connection():
    return sqlite3.connect(DATABASE_NAME)


# ===========================
# Create All Tables
# ===========================

def create_database():

    conn = get_connection()
    cursor = conn.cursor()


    # ===========================
    # Users Table
    # ===========================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT UNIQUE NOT NULL,

        password TEXT NOT NULL,

        fullname TEXT,

        role TEXT DEFAULT 'Employee'

    )
    """)


    # ===========================
    # Products Table
    # ===========================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        barcode TEXT UNIQUE,

        name TEXT NOT NULL,

        category TEXT,

        supplier TEXT,

        buy_price REAL DEFAULT 0,

        sell_price REAL DEFAULT 0,

        quantity INTEGER DEFAULT 0,

        min_quantity INTEGER DEFAULT 5,

        image TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)


    # ===========================
    # Customers Table
    # ===========================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT NOT NULL,

        phone TEXT,

        address TEXT,

        points INTEGER DEFAULT 0

    )
    """)


    # ===========================
    # Suppliers Table
    # ===========================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS suppliers (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT NOT NULL,

        phone TEXT,

        company TEXT,

        address TEXT

    )
    """)


    # ===========================
    # Sales Table
    # ===========================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sales (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        invoice_number TEXT UNIQUE,

        customer_id INTEGER,

        total REAL DEFAULT 0,

        payment_method TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)


    # ===========================
    # Sale Items Table
    # ===========================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sale_items (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        sale_id INTEGER,

        product_id INTEGER,

        quantity INTEGER,

        price REAL,

        total REAL

    )
    """)


    # ===========================
    # Settings Table
    # ===========================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS settings (

        id INTEGER PRIMARY KEY,

        market_name TEXT,

        phone TEXT,

        address TEXT,

        tax REAL DEFAULT 0

    )
    """)


    # ===========================
    # Default Admin Account
    # ===========================

    cursor.execute("""
    INSERT OR IGNORE INTO users
    (
        id,
        username,
        password,
        fullname,
        role
    )

    VALUES
    (
        1,
        'admin',
        '1234',
        'Administrator',
        'Admin'
    )
    """)


    # ===========================
    # Default Market Settings
    # ===========================

    cursor.execute("""
    INSERT OR IGNORE INTO settings
    (
        id,
        market_name,
        phone,
        address,
        tax
    )

    VALUES
    (
        1,
        'Smart Market',
        '',
        '',
        0
    )
    """)


    conn.commit()
    conn.close()



# ===========================
# Run Database Setup
# ===========================

if __name__ == "__main__":

    create_database()

    print("==============================")
    print(" Smart Market Database Ready ")
    print("==============================")
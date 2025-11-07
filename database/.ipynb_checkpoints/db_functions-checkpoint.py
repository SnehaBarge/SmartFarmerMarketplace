import sqlite3
import pandas as pd

DB_NAME = 'farmermarket.db'

def init_db():
    """Initializes the database file and creates tables if they don't exist."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Create Tools Table
    c.execute("""CREATE TABLE IF NOT EXISTS tools (
        Farmer TEXT,
        Location TEXT,
        Tool TEXT,
        Rate REAL,
        Contact TEXT,
        Notes TEXT
    )""")

    # Create Crops Table
    c.execute("""CREATE TABLE IF NOT EXISTS crops (
        Farmer TEXT,
        Location TEXT,
        Crop TEXT,
        Quantity TEXT,
        Expected_Price REAL,
        Contact TEXT,
        Listing_Date TEXT
    )""")
    conn.commit()
    conn.close()

def add_data(table_name, data_tuple):
    """Adds a new row of data to the specified SQLite table."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    if table_name == "tools":
        sql = "INSERT INTO tools (Farmer, Location, Tool, Rate, Contact, Notes) VALUES (?, ?, ?, ?, ?, ?)"
    elif table_name == "crops":
        sql = "INSERT INTO crops (Farmer, Location, Crop, Quantity, Expected_Price, Contact, Listing_Date) VALUES (?, ?, ?, ?, ?, ?, ?)"
        
    c.execute(sql, data_tuple)
    conn.commit()
    conn.close()

def get_data(table_name):
    """Retrieves all data from the specified SQLite table and returns a Pandas DataFrame."""
    conn = sqlite3.connect(DB_NAME)
    # Using rowid allows us to uniquely identify rows, essential for update/delete later
    df = pd.read_sql_query(f"SELECT rowid, * FROM {table_name}", conn)
    conn.close()
    return df
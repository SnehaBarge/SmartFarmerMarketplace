import sqlite3
import pandas as pd

# Define the database file name
DB_FILE = 'farmermarket.db'

def view_data_from_db():
    """Connects to the SQLite DB and prints the data from the 'tools' and 'crops' tables."""
    try:
        # 1. Establish connection to the SQLite database file
        conn = sqlite3.connect(DB_FILE)
        
        print("--- Connecting to Database: farmermarket.db ---")
        
        # 2. Read the 'tools' table into a Pandas DataFrame
        tools_df = pd.read_sql_query("SELECT * FROM tools", conn)
        
        print("\n====================================")
        print("📊 TOOLS LISTINGS DATA")
        print("====================================")
        if tools_df.empty:
            print("No tool listings found.")
        else:
            print(tools_df)
            
        # 3. Read the 'crops' table into a Pandas DataFrame
        crops_df = pd.read_sql_query("SELECT * FROM crops", conn)
        
        print("\n====================================")
        print("🌿 CROPS LISTINGS DATA")
        print("====================================")
        if crops_df.empty:
            print("No crop listings found.")
        else:
            print(crops_df)

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        print(f"Ensure the file '{DB_FILE}' exists in this directory.")
    finally:
        # 4. Close the database connection
        if 'conn' in locals() and conn:
            conn.close()

if __name__ == "__main__":
    view_data_from_db()
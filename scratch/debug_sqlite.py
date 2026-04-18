import sqlite3
import os

def test_sqlite():
    db_path = r"D:\PHEME\.cognee_system\databases"
    print(f"Testing DB path: {db_path}")
    print(f"Exists: {os.path.exists(db_path)}")
    print(f"Is Dir: {os.path.isdir(db_path)}")
    
    try:
        # If it's a directory, this WILL fail
        conn = sqlite3.connect(db_path)
        print("Successfully connected to directory?! (This shouldn't happen)")
        conn.close()
    except Exception as e:
        print(f"Error as expected: {e}")

    actual_file = os.path.join(db_path, "cognee_system.db")
    print(f"Testing actual file: {actual_file}")
    try:
        conn = sqlite3.connect(actual_file)
        print("Successfully connected to actual file!")
        conn.close()
    except Exception as e:
        print(f"Failed to connect to actual file: {e}")

if __name__ == "__main__":
    test_sqlite()

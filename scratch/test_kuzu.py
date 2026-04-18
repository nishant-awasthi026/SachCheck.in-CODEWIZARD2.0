import kuzu
import os
import shutil

db_path = os.path.abspath("test_kuzu_standalone")
if os.path.exists(db_path):
    if os.path.isdir(db_path):
        shutil.rmtree(db_path)
    else:
        os.remove(db_path)

try:
    print(f"Opening Kuzu at {db_path}...")
    db = kuzu.Database(db_path)
    conn = kuzu.Connection(db)
    print("Kuzu initialized successfully!")
except Exception as e:
    print(f"Kuzu failed: {e}")

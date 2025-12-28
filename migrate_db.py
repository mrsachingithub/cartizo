import sqlite3

def migrate():
    conn = sqlite3.connect('instance/refundguard.db')
    cursor = conn.cursor()
    
    try:
        # Check if column exists
        cursor.execute("PRAGMA table_info(return_request)")
        columns = [info[1] for info in cursor.fetchall()]
        
        if 'description' not in columns:
            print("Adding description column to return_request...")
            cursor.execute("ALTER TABLE return_request ADD COLUMN description TEXT")
            print("Column added successfully.")
        else:
            print("Column 'description' already exists.")
            
    except Exception as e:
        print(f"Migration error: {e}")
    finally:
        conn.commit()
        conn.close()

if __name__ == '__main__':
    migrate()

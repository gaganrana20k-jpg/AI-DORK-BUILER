import sqlite3

conn = sqlite3.connect("users.db")

cursor = conn.cursor()

# Create users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT NOT NULL,

    email TEXT UNIQUE NOT NULL,

    password TEXT NOT NULL

)
""")

# Create history table
cursor.execute("""
CREATE TABLE IF NOT EXISTS history(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_email TEXT NOT NULL,

    dork TEXT NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS favorites(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_email TEXT NOT NULL,

    dork TEXT NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)
""")

conn.commit()
conn.close()

print("Database created successfully!")
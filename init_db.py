import sqlite3

# This creates a database file called 'passwords.db'
conn = sqlite3.connect('passwords.db')
cursor = conn.cursor()

# This creates the 'passwords' table if it doesn’t exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS passwords (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    password TEXT NOT NULL,
    strength TEXT NOT NULL
)
''')

conn.commit()
conn.close()

print("✅ Database and table created!")

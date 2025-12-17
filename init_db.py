import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS vehicles")

cursor.execute('''
CREATE TABLE vehicles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    number_plate TEXT NOT NULL UNIQUE,
    owner_name TEXT,
    phone_number TEXT
)
''')

sample_data = [
    ('DL8CAF5032', 'Rohan Sharma', '+919876543210'),
    ('MH12AB1234', 'Navya Gupta', '+919560107720'),
    ('UP16AB4521', 'Amit Verma', '+918765432109'),
    ('HR26DK8337', 'Neha Gupta', '+919934567890'),
]

for data in sample_data:
    cursor.execute("INSERT INTO vehicles (number_plate, owner_name, phone_number) VALUES (?, ?, ?)", data)

conn.commit()
conn.close()
print("✅ Database reinitialized successfully with correct columns!")

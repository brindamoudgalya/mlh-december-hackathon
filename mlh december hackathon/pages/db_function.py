import sqlite3
conn = sqlite3.connect("data.db")
c = conn.cursor()

# database
# table
# field/columns
# data type

def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS entrytable(diary_entry TEXT, date_entry TEXT)')

def add_data(diary_entry, date_entry):
    c.execute('INSERT INTO entrytable(diary_entry, date_entry) VALUES (?,?)', (diary_entry, date_entry))
    conn.commit()
              
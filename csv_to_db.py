import csv
import sqlite3

conn = sqlite3.connect('data.db')
cursor = conn.cursor()

tool = 'EURUSD'

with open('data/DAT_NT_EURUSD_M1_201609.csv') as csv_file:
    reader = csv.reader(csv_file, delimiter=';')
    for row in reader:
        datetime = int(row[0].replace(' ', ''))
        open = float(row[1])
        high = float(row[2])
        low = float(row[3])
        close = float(row[4])
        cursor.execute('insert into stock_m1 values(?,?,?,?,?,?)', (tool, datetime, open, high, low, close))
    conn.commit()
conn.close()

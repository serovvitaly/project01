import sqlite3
import redis
import progressbar

conn = sqlite3.connect('data.db')
r = redis.StrictRedis(host='localhost', port=6379, db=0)

"""Загружает оперативные данные в Redis"""


tickets_arr = conn.cursor().execute(
    'SELECT datetime, open, high, low, close '
    'FROM stock_m1'
)
pb = progressbar.ProgressBar(max_value=265887)
i = 1
for row in tickets_arr:
    r.zadd('stock_m1', int(row[0]), {
        'datetime': row[0],
        'open': float(row[1]),
        'high': float(row[2]),
        'low': float(row[3]),
        'close': float(row[4]),
    })
    pb.update(i)
    i += 1

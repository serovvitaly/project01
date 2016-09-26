import csv
import sqlite3
import progressbar
from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer

"""
1. Все открытые позиции должны быть закрыты в течении одного торгового дня
2.

1. Открывать ли дилнную позицию
2. Открывать ли короткую позицию
3. Закрывать ли длинную позицию
4. Закрывать ли короткую позицию
5. Определять общий суточный тренд

Что делать с открытыми позициями под конец торговой сессии,
если нет сигналов на закрытие позиций?
1. Принудительно закрывать все открытые позиции
2. Расчитывать вероятность закрытия позиции в течении торговой сессии,
   и закрывать позицию исходя из этой вероятности

"""

conn = sqlite3.connect('data.db')
cursor = conn.cursor()

def get_inputs_data_from_inputs_tickets_arr(tickets_arr):
    output = ()
    for row in tickets_arr:
        open = float(row[1])
        high = float(row[2])
        low = float(row[3])
        close = float(row[4])
        output += (open,)
        output += (high,)
        output += (low,)
        output += (close,)
    return output

"Количество входов НС"
inputs_count = 3000

"Горизонт предсказания в тикетах"
prediction_horizon = 30  # 30 минут

""
sample_width = inputs_count + prediction_horizon

"Минут в торговом дне"
minutes_in_day = 1438

"Количество месяцев для обучающей выборки"
train_ds_months_count = 4

"Номер месяца для тестовой выборки"
test_month_number = 8  # август

"Коллекция нейронных сетей(НС), для каждой минуты в торговом дне"
nets_arr = {}
for nkey in range(1, minutes_in_day+1):
    nets_arr[nkey] = {
        'net': buildNetwork(inputs_count * 4, 5, 5, 4),
        'ds': SupervisedDataSet(inputs_count * 4, 4)
    }

"""Процесс обучения"""
print('Процесс обучения...')
train_records = cursor.execute('SELECT * FROM stock_m1 limit 1')
bar = progressbar.ProgressBar(max_value=train_records.rowcount*minutes_in_day)
iterator = 0
for row in train_records:
    datetime = int(row[1])
    inputs_tickets_arr = cursor.execute('SELECT * FROM stock_m1 limit 1')
    input_tuple = get_inputs_data_from_inputs_tickets_arr(inputs_tickets_arr)
    for mx in nets_arr:
        mx['ds'].addSample(input_tuple, (open, high, low, close))
    iterator += 1
    bar.update(iterator)

for mx in nets_arr:
    trainer = BackpropTrainer(mx['net'], mx['ds'])
    error = trainer.train()


"""Использование обученной сети"""
print('Использование обученной сети...')
for row in cursor.execute('SELECT * FROM stock_m1 limit 1'):
        print(row)

conn.close()

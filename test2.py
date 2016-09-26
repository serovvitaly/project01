import csv
from datetime import datetime
import sqlite3

import progressbar
from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer

inputs_count = 3000

"Горизонт предсказания в тикетах"
prediction_horizon = 30  # 30 минут

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


net = buildNetwork(inputs_count * 4, 5, 5, 1)

sample_width = inputs_count + prediction_horizon

profit = 0

conn = sqlite3.connect('data.db')
cursor = conn.cursor()

with open('data/DAT_NT_EURUSD_M1_201602.csv') as csv_file:
    reader = csv.reader(csv_file, delimiter=';')
    reader = list(reader)
    bar = progressbar.ProgressBar(max_value=len(reader))
    era_step = 0
    data_set = SupervisedDataSet(inputs_count * 4, 1)
    for key, row in enumerate(reader):
        """Обучение сети"""
        open = float(row[1])
        high = float(row[2])
        low = float(row[3])
        close = float(row[4])
        current_datetime = datetime.strptime(row[0], '%Y%m%d %H%M%S')
        cursor.execute('insert into stock values(?,?,?,?,?,?)', ('EURUSD_M1', current_datetime.strftime('%Y%m%d%H%M%S'),open, high, low, close))
        continue
        if key < sample_width:
            continue
        open = float(row[1])
        high = float(row[2])
        low = float(row[3])
        close = float(row[4])
        inputs_tickets_arr = reader[(key - sample_width):(key - prediction_horizon):1]
        input_tuple = get_inputs_data_from_inputs_tickets_arr(inputs_tickets_arr)
        data_set.addSample(input_tuple, (open,))
        era_step += 1
        if era_step > 10:
            trainer = BackpropTrainer(net, data_set)
            error = trainer.train()
            print(error)
            #result = net.activate(input_tuple)
            #print('Error: ' + str(error) + ', Result: ' + str(result[0]) + ', Target: ' + str(open))
            data_set = SupervisedDataSet(inputs_count * 4, 1)
            era_step = 0
            break
        #bar.update(key)
    conn.commit()
    working_date = 0
    for key, row in enumerate(reader):
        """Использование сети"""
        current_datetime = datetime.strptime(row[0], '%Y%m%d %H%M%S')
        current_date = current_datetime.date()
        print(current_date)
        break
        if key < sample_width:
            continue
        open = float(row[1])
        high = float(row[2])
        low = float(row[3])
        close = float(row[4])
        inputs_tickets_arr = reader[(key - sample_width):(key - prediction_horizon):1]
        input_tuple = get_inputs_data_from_inputs_tickets_arr(inputs_tickets_arr)
        result = net.activate(input_tuple)
        print('Error: ' + str(error) + ', Result: ' + str(result[0]) + ', Target: ' + str(open))

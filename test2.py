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

"Количество входов НС"
inputs_count = 1000


def get_inputs_data_set(datetime):
    tickets_arr = conn.cursor().execute(
        'SELECT open, high, low, close '
        'FROM stock_m1 '
        'WHERE datetime >= ? '
        'ORDER BY datetime LIMIT ?',
        (datetime, inputs_count)
    )
    output = ()
    for row in tickets_arr:
        output += row
    return output

def time_to_int(time):
    """Преобразует время в номер минуты в сутках"""
    hours = int(time[:2])
    minutes = int(time[2:4])
    return hours * 60 + minutes + 1

"Горизонт предсказания в тикетах"
prediction_horizon = 30  # 30 минут

""
sample_width = inputs_count + prediction_horizon

"Минут в торговом дне"
minutes_in_day = 1440

"Количество месяцев для обучающей выборки"
train_ds_months_count = 4

"Номер месяца для тестовой выборки"
test_month_number = 8  # август

"Коллекция нейронных сетей(НС), для каждой минуты в торговом дне"
print('Построение сети...')
nets_arr = {}
for nkey in range(1, minutes_in_day + 1):
    nets_arr[nkey] = {
        'net': buildNetwork(inputs_count * 4, 5, 5, 4),
        'ds': SupervisedDataSet(inputs_count * 4, 4)
    }

"""Процесс обучения"""
print('Сбор данных...')
train_records = conn.cursor().execute('SELECT * FROM stock_m1 LIMIT 1000')
for row in train_records:
    input_tuple = get_inputs_data_set(str(row[1])[:8])
    time_int = time_to_int(str(row[1])[8:])
    nets_arr[time_int]['ds'].addSample(input_tuple, (row[2], row[3], row[4], row[5]))

print('Обучение сети...')
for key, mx in nets_arr.items():
    if len(mx['ds']) < 1:
        continue
    trainer = BackpropTrainer(mx['net'], mx['ds'])
    error = trainer.train()
    print(error)

"""Использование обученной сети"""
print('Использование обученной сети...')
for row in conn.cursor().execute('SELECT * FROM stock_m1 LIMIT 1'):
    #print(row)
    pass

conn.close()

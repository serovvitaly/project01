import sqlite3
import redis
import progressbar
from datetime import datetime, timedelta
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
pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
r = redis.Redis(connection_pool=pool)


def get_train_data(train_datetime, data_set_days_length):
    """
    Возвращает ноборы данных: тренировачный и проверочный
    :param train_datetime: Дата в формате YYYYMMDDHHIISS
    :param data_set_days_length: Размер выбрки данных, в днях
    :return:
    """
    end_datetime = datetime.strptime(str(train_datetime), '%Y%m%d%H%M%S')
    begin_datetime = end_datetime - timedelta(days=data_set_days_length)
    print(train_datetime)
    print(begin_datetime)
    print(end_datetime)
    return
    train_data_set = r.zrangebyscore(
        'stock_m1',
        begin_datetime.strftime('%Y%m%d%H%M%S'),
        end_datetime.strftime('%Y%m%d%H%M%S')
    )
    target_data_set = r.zrangebyscore('stock_m1', train_datetime, train_datetime)
    return [train_data_set, target_data_set]


def train_nn(period_begin, period_end, data_set_length, target_min):
    """
    Тренирует нейронную сеть на определенную минуту
    :param period_begin:  Начало периода обучающей выборки, в формате YYYYMMDDHHII
    :param period_end: Окончание периода обучающей выборки, в формате YYYYMMDDHHII
    :param data_set_length: Длина обучающей выборки
    :param target_min: Номер минуты в сутках, на которую будет проводиться обучение
    :return:
    """
    """Сбор коллекций данных"""
    pb = progressbar.ProgressBar(max_value=period_end - period_begin)
    print('Сбор коллекций данных...')
    i = 0
    for iter_date in range(period_begin, period_end):
        iter_date *= 100
        ds = get_train_data(iter_date, data_set_length)
        pb.update(i)
        i += 1
    print('Тренировка сети...')
    """Тренировка сети"""
    pass

train_nn(201608010000, 201608300000, 30, 1000)

exit()

"Количество входов НС"
inputs_count = 2000


def get_inputs_data_set(datetime):
    tickets_arr = conn.cursor().execute(
        'SELECT open, high, low, close '
        'FROM stock_m1 '
        'WHERE datetime < ? '
        'ORDER BY datetime LIMIT ?',
        (datetime, inputs_count)
    )
    output = ()
    for row in tickets_arr:
        output += row
    return output


def time_to_int(time):
    """Преобразует время в номер минуты в сутках"""
    time = str(time)
    hours = int(time[8:10])
    minutes = int(time[10:12])
    return hours * 60 + minutes + 1


def add_sample_to_net(date_val):
    """Данный метод, тренирует все НС для каждой минуты на данный день"""
    input_data_set = get_inputs_data_set(str(date_val)+'000000')
    #print('Размер входного массива: ' + str(len(input_data_set)))
    output_data_set_cursor = conn.cursor().execute(
        'SELECT datetime, open, high, low, close '
        'FROM stock_m1 '
        'WHERE datetime BETWEEN ? and ?'
        'ORDER BY datetime',
        (str(date_val)+'000000', str(date_val)+'050000')
    )
    for output_data_set in output_data_set_cursor:
        time_int = time_to_int(output_data_set[0])
        nets_arr[time_int]['ds'].addSample(input_data_set, output_data_set[1:])


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
start_date = 20160501
stop_date = 20160832
i = 1
pb = progressbar.ProgressBar(max_value=stop_date-start_date)
for date in range(start_date, stop_date):
    add_sample_to_net(date)
    pb.update(i)
    i += 1

print('\nОбучение сети...')
for key, mx in nets_arr.items():
    if len(mx['ds']) < 1:
        continue
    print('Количество датасетов: ' + str(len(mx['ds'])))
    trainer = BackpropTrainer(mx['net'], mx['ds'])
    error = trainer.train()
    print(error)

"""Использование обученной сети"""
print('Использование обученной сети...')
for row in conn.cursor().execute('SELECT * FROM stock_m1 LIMIT 1'):
    # print(row)
    pass

conn.close()

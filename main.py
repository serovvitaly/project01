from datetime import datetime
import progressbar
import postgresql
from sklearn.neural_network import BernoulliRBM
from sklearn import preprocessing
import numpy

db = postgresql.open('pq://postgres:123@localhost:5432/project01')

limit = 3

train_data_set_rows = db.prepare('SELECT * FROM train LIMIT ' + str(limit))

#print(datetime.now())

X = []

# 74180464
#pbar = progressbar.ProgressBar(widgets=[progressbar.Percentage(), progressbar.Bar()], maxval=limit).start()
row_index = 1
for row in train_data_set_rows:

    p_semana = row[0]
    p_agencia_id = row[1] / 10000
    p_canal_id = row[2] / 100
    p_ruta_sak = row[3]
    p_cliente_id = row[4]
    p_producto_id = row[5]

    #pbar.update(row_index)
    row_index += 1

    X.append([row[0], row[1], row[2], row[3], row[4], row[5]])

    #model = BernoulliRBM(5)
    #X = numpy.array([[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 1]])
    #model.fit(X)

#pbar.finish()
#print(datetime.now())

print(X)

normal_X = preprocessing.normalize(X)
scale_X = preprocessing.scale(X)

print(normal_X)
print(scale_X)

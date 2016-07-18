from datetime import datetime
import progressbar
from neuronet.network import Network
import postgresql

net = Network()

net.input = 6
net.output = 1
net.hidden = 3, 2, 4

db = postgresql.open('pq://Vitaly:123@localhost:5432/project01')

train_data_set_rows = db.prepare('SELECT * FROM train LIMIT 10')


def prepare_output(data):
    return data


net.prepare_output = prepare_output

print(datetime.now())

# 74180464
pbar = progressbar.ProgressBar(widgets=[progressbar.Percentage(), progressbar.Bar()], maxval=10).start()
row_index = 1
for row in train_data_set_rows:

    p_semana = row[0]
    p_agencia_id = row[1] / 10000
    p_canal_id = row[2] / 100
    p_ruta_sak = row[3]
    p_cliente_id = row[4]
    p_producto_id = row[5]

    data_set = [p_semana, p_agencia_id, p_canal_id, p_ruta_sak, p_cliente_id, p_producto_id]
    print(data_set)
    result = net.train([1, 2, 3, 4, 5, 6])
    # print(result)
    pbar.update(row_index)
    row_index += 1

pbar.finish()
print(datetime.now())

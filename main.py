from neuronet.network import Network
import postgresql

net = Network()

net.input = 6
net.output = 1
net.hidden = 3, 2, 4

db = postgresql.open('pq://Vitaly:123@localhost:5432/project01')

train_data_set_rows = db.prepare('SELECT * FROM train LIMIT 5')


def prepare_output(data):
    return data


net.prepare_output = prepare_output

for row in train_data_set_rows:
    data_set = [
        row[0],
        row[1],
        row[2],
        row[3],
        row[4],
        row[5],
    ]
    result = net.train([1, 2, 3, 4, 5, 6])
    #print(result)

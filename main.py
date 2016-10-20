from datetime import datetime
import progressbar
import postgresql
from neuronet.neuron import Neuron

#db = postgresql.open('pq://postgres:123@localhost:5432/project01')

limit = 3

#train_data_set_rows = db.prepare('SELECT * FROM train LIMIT ' + str(limit))


# Входной слой
l1_n1 = Neuron()
l1_n2 = Neuron()
l1_n3 = Neuron()

# Скрытый слой
l2_n1 = Neuron()
l2_n1.add_relation(l1_n1)
l2_n1.add_relation(l1_n2)
l2_n1.add_relation(l1_n3)

l2_n2 = Neuron()
l2_n2.add_relation(l1_n1)
l2_n2.add_relation(l1_n2)
l2_n2.add_relation(l1_n3)

l2_n3 = Neuron()
l2_n3.add_relation(l1_n1)
l2_n3.add_relation(l1_n2)
l2_n3.add_relation(l1_n3)

# Выходной слой
l3_n1 = Neuron()
l3_n1.add_relation(l2_n1)
l3_n1.add_relation(l2_n2)
l3_n1.add_relation(l2_n3)

l3_n1_val = l3_n1.get_output_value()

print(l3_n1_val)

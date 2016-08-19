from neuronet.network import Network
from neuronet.neuron import Neuron
from neuronet.neuron import Input

data = [
    (1,1,0),
    (2,2,0),
    (3,3,0),
    (1,3,0),
    (4,2,0),
    (6,9,1),
    (7,8,1),
    (7,9,1),
    (8,8,1),
    (9,10,1),
]

net = Network()
net.input = 6
net.hidden = (3,4)
net.output = 1

ls = net.get_layers()
for layer in ls:
    print(ls[layer])

input_1 = Input()
input_2 = Input()

output_1 = Neuron('output_1')
output_1.add_relation(input_1, .335)
output_1.add_relation(input_2, .332)

for row in data:
    input_1.set_output_value(row[0]/10)
    input_2.set_output_value(row[1]/10)
    out_val = output_1.get_output_value()
    #print(out_val)

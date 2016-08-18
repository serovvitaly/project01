from neuronet.neuron import Neuron
from neuronet.neuron import Input


input_1 = Input()
input_2 = Input()

output_1 = Neuron('output_1')
output_1.add_relation(input_1)
output_1.add_relation(input_2)

input_1.set_output_value(2)
input_2.set_output_value(3)

out_val = output_1.get_output_value()

print(out_val)

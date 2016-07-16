from .layer import Layer


class Network:
    input = 1
    output = 1
    hidden = ()
    layers = None

    def __init__(self):
        pass

    def train(self, param):
        layers = self.get_layers()
        print(layers)

    def rebuild_layers(self):
        self.layers = {}
        layer_index = 0
        self.layers[layer_index] = Layer(self.input)
        layer_index += 1
        for h_neurons_number in self.hidden:
            self.layers[layer_index] = Layer(h_neurons_number)
            layer_index += 1
        self.layers[layer_index] = Layer(self.output)

    def get_layers(self):
        if self.layers is None:
            self.rebuild_layers()
        return self.layers

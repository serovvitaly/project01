from .layer import Layer


class Network:
    input = 1
    output = 1
    hidden = ()
    layers = None
    prepare_output = None

    def __init__(self):
        pass

    def prepare_output_result(self, output_result):
        """Функция преобразования выходного сигнала"""
        if self.prepare_output is None:
            return output_result
        return self.prepare_output(output_result)

    def train(self, data_set):
        """Функция тренировки сети"""
        layers = self.get_layers()
        layers_count = len(layers)
        output_result = None
        for layer_index, layer_obj in layers.items():
            if layer_index == 0:
                # Input layer
                data_set = layer_obj.train(data_set)
            elif layer_index == layers_count - 1:
                # Output layer
                output_result = layer_obj.train(data_set)
            else:
                # Hidden layer
                data_set = layer_obj.train(data_set)
        output_result = self.prepare_output_result(output_result)
        return output_result

    def rebuild_layers(self):
        """Первичное построение или перестроение сети"""
        self.layers = {}
        layer_index = 0
        # Создание входного слоя
        self.layers[layer_index] = Layer(self.input)
        prev_layer_neurons_count = self.input
        layer_index += 1
        for h_neurons_count in self.hidden:
            # Создание скрытых слоёв
            self.layers[layer_index] = Layer(h_neurons_count, prev_layer_neurons_count)
            prev_layer_neurons_count = h_neurons_count
            layer_index += 1
        # Создание выходного слоя
        self.layers[layer_index] = Layer(self.output, prev_layer_neurons_count)

    def get_layers(self):
        if self.layers is None:
            self.rebuild_layers()
        return self.layers

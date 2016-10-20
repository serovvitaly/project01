from .neuron import Neuron


class Layer:
    neurons_count = 1
    prev_layer_neurons_count = 0
    weights_matrix = {}
    neurons = {}

    def __init__(self, neurons_count=1, prev_layer_neurons_count=0):
        self.neurons_count = int(neurons_count)
        self.prev_layer_neurons_count = int(prev_layer_neurons_count)
        self.init_weights_matrix()
        self.rebuild_layer()
        pass

    @staticmethod
    def get_init_weight():
        return .1

    def init_weights_matrix(self):
        """Функция инициализации матрицы весов"""
        self_neurons_keys = []
        self_neurons_keys.extend(range(0, self.neurons_count))
        self.weights_matrix = dict((key, [self.get_init_weight()]*self.prev_layer_neurons_count) for key in self_neurons_keys)

    def rebuild_layer(self):
        self_neurons_keys = []
        self_neurons_keys.extend(range(0, self.neurons_count))
        neuron_obj = Neuron()
        self.neurons = dict((key, neuron_obj) for key in self_neurons_keys)

    def train(self, data_set):
        """Функция тренировки слоя"""
        if len(self.weights_matrix) < 1:
            return data_set
        results = []
        for neuron_index, neuron_obj in self.neurons.items():
            weight_set = self.weights_matrix[neuron_index]
            result = self.train_neuron(neuron_obj, data_set, weight_set)
            results.append(result)
        return results

    @staticmethod
    def train_neuron(neuron, data_set, weight_set):
        """Функция тренировки нейрона"""
        return neuron.train(data_set, weight_set)

    def __str__(self):
        return 'Neurons number = ' + str(self.neurons_count)

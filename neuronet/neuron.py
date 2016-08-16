class Neuron:
    output_value = None

    relations = []

    class relation:
        """Связь между нейронами"""
        neuron = None
        weight = None

        def __init__(self, neuron, weight):
            self.neuron = neuron
            self.weight = weight

        def get_calculated_value(self):
            return self.neuron.get_output_value() * self.weight

    def __init__(self):
        pass

    def set_output_value(self, val):
        """
        Устанавливает выходное значение
        """
        self.output_value = val

    def get_output_value(self, recalculate=True):
        """
        Возвращает выходное значение, если установлен recalculate,
        то предварительно пересчитывает выходное значение
        """
        if self.output_value is None | recalculate is True:
            self.calculate_output_value()
        return self.output_value

    def calculate_output_value(self):
        """Расчитывает выходное значение"""
        output_value = 3
        self.set_output_value(output_value)

    def add_relation(self, neuron, weight):
        self.relations.append(self.relation(neuron, weight))

    def train(self, data_set, weight_set):
        """Функция тренировки нейрона"""
        # print(data_set)
        # print(weight_set)
        return 2

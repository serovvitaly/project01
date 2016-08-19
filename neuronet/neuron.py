class Relation:
    """Связь между нейронами"""

    def __init__(self, neuron, weight):
        self.neuron = neuron
        self.weight = weight

    def get_calculated_value(self):
        return self.neuron.get_output_value() * self.weight


class Input:
    """Заглушка для входного слоя"""
    def __init__(self):
        self.output_value = 0

    def set_output_value(self, output_value):
        self.output_value = output_value

    def get_output_value(self):
        return self.output_value


class Neuron:

    def __init__(self, name=None):
        self.name = name
        self.output_value = None
        self.relations = []
        pass

    def set_output_value(self, val):
        """Устанавливает выходное значение"""
        self.output_value = val

    def get_output_value(self, recalculate=True):
        """
        Возвращает выходное значение, если установлен recalculate,
        то предварительно пересчитывает выходное значение
        """
        if self.output_value is None or recalculate is True:
            self.calculate_output_value()
        return self.output_value

    def calculate_output_value(self):
        """Расчитывает выходное значение"""
        output_value = 0
        for relation in self.relations:
            output_value += relation.get_calculated_value()
        output_value = self.calculate_transfer_function(output_value)
        self.set_output_value(output_value)

    def add_relation(self, neuron, weight=0.5):
        """Добавление связи с нейроном"""
        self.relations.append(Relation(neuron, weight))

    def calculate_transfer_function(self, value):
        """Вычисление передаточной функции"""
        return value / 2

    def train(self, data_set, weight_set):
        """Функция тренировки нейрона"""
        # print(data_set)
        # print(weight_set)
        return 2

from layer import Layer

class Network:
    def __init__(self):
        self.layers = [
            Layer(16, 784),
            Layer(16, 16),
            Layer(16, 16),
            Layer(10, 16, use_softmax=True)
        ]

    def predict(self, input):
        for layer in self.layers:
            input = layer.forward(input)
        return input

    def train(self, input, target, lr):
        output = self.predict(input)
        error = output - target
        for layer in reversed(self.layers):
            error = layer.backward(error, lr)

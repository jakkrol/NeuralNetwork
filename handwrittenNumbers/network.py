from layer import Layer

class Network:
    def __init__(self):
        self.layers = [
            Layer(16, 784),
            Layer(16, 16),
            Layer(16, 16),
            Layer(10, 16)
        ]
    
    def predict(self, input):
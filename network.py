from layer import Layer

class Network:
    def __init__(self):
        self.layers = []
        self.layers.append(Layer(3))  
        self.layers.append(Layer(3))
        self.layers.append(Layer(1))
    
    def predict(self, input):
        for layer in self.layers:
            input = layer.predict(input)
        
        return input[0] > 0;
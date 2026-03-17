from layer import Layer

class Network:
    def __init__(self):
        self.layers = []
        self.layers.append(Layer(8))  
        self.layers.append(Layer(8))
        self.layers.append(Layer(4))
    
    def predict(self, input):
        for layer in self.layers:
            input = layer.predict(input)
        
        return input
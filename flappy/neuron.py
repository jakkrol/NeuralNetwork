import random

class Neuron: 
    def __init__(self):
        self.weights = []

    def predict(self, inputs):
        while len(self.weights) < len(inputs) + 1:
            self.weights.append(random.uniform(-1, 1))
        
        total = 0
        for i in range(len(inputs)):
            total += inputs[i] * self.weights[i]

        total += self.weights[-1]

        return total
            
        
    


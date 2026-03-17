from neuron import Neuron

class Layer:
    def __init__(self, numNeurons):
        self.neurons = []

        for i in range(numNeurons):
            self.neurons.append(Neuron())

    def predict(self, input):
        output = []
        
        for neuron in self.neurons:
            output.append(neuron.predict(input))

        return output
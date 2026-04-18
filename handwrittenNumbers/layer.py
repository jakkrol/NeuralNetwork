import numpy as np

class Layer:
    def __init__ (self, numNeurons, numInputs):
        self.weights = np.random.rand(numInputs, numNeurons) * 0.1
        self.biases = np.zeros((1, numNeurons))

    def forward(self, input):
        #self.input = input
        np.array(input).reshape(1, -1) # reshape to 2D array
        z = np.dot(input, self.weights) + self.biases
        z = np.maximum(0, z) # ReLU 
        self.input = input
        self.output = z
        return self.output
    
    def backward(self, output_error, learning_rate):
        p = np.where(self.output > 0, 1, 0)
        gradient = output_error * p
        input_error = np.dot(gradient, self.weights.T)
        weights_error = np.dot(self.input.T, gradient)
        self.weights -= learning_rate * weights_error
        self.biases -= learning_rate * gradient
        return input_error

import numpy as np

class Layer:
    def __init__ (self, numNeurons, numInputs, use_softmax=False):
        self.weights = np.random.rand(numInputs, numNeurons) * 0.1
        self.biases = np.zeros((1, numNeurons))
        self.use_softmax = use_softmax

    def forward(self, input):
        #self.input = input
        input = np.array(input).reshape(1, -1) # reshape to 2D array
        z = np.dot(input, self.weights) + self.biases
        if self.use_softmax:
            z = self.softmax(z)
        else:
            z = np.maximum(0, z) # ReLU 
        self.input = input
        self.output = z
        return self.output
    
    def backward(self, output_error, learning_rate):
        p = np.where(self.output > 0, 1, 0)
        if self.use_softmax:
            gradient = output_error
        else:
            gradient = output_error * p
        input_error = np.dot(gradient, self.weights.T)
        weights_error = np.dot(self.input.T, gradient)
        self.weights -= learning_rate * weights_error
        self.biases -= learning_rate * gradient
        return input_error

    def softmax(self, z):
        exp_z = np.exp(z - np.max(z))
        return exp_z / np.sum(exp_z, axis=1, keepdims=True)
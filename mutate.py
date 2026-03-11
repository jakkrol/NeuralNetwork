# from random import random
# from network import Network

# class Mutate:
#     def __init__(self, parentNetwork):
#         self.mutation = Network

#         for i in range(len(self.parentNetwork.layers)):
#             for j in range(len(self.parentNetwork.layers[i].neurons)):
#                 for k in range(len(self.parentNetwork.layers[i].neurons[j].weights)):
#                     mutation_rate = 0.05
#                     if random.random() <= mutation_rate:
#                         self.mutation.layers[i].neurons[j].weights[k] = random.uniform(-1, 1)
#                     else:
#                         self.mutation.layers[i].neurons[j].weights[k] = self.parentNetwork.layers[i].neurons[j].weights[k]
#     return self.mutation
import random
from network import Network

def mutate_network(parentNetwork):
    new_net = Network()
    
    for i in range(len(parentNetwork.layers)):
        for j in range(len(parentNetwork.layers[i].neurons)):
            
            parent_neuron = parentNetwork.layers[i].neurons[j]
            child_neuron = new_net.layers[i].neurons[j]

            child_neuron.weights = list(parent_neuron.weights)
            
            mutation_rate = 0.05
            for k in range(len(child_neuron.weights)):
                if random.random() <= mutation_rate:
                    child_neuron.weights[k] += random.uniform(-1, 1)
                
    return new_net
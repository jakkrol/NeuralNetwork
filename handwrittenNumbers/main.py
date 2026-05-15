import kagglehub
import numpy as np
import os
from network import Network

def load_data_img(file_path):
    with open(file_path, 'rb') as f:
        data = np.frombuffer(f.read(), dtype=np.uint8, offset=16)
    return data.reshape(-1, 784) / 255.0

def load_data_labels(file_path):
    with open(file_path, 'rb') as f:
        data = np.frombuffer(f.read(), dtype=np.uint8, offset=8)
    return data


train_img = load_data_img('mnist-dataset/versions/1/train-images.idx3-ubyte')
train_labels = load_data_labels('mnist-dataset/versions/1/train-labels.idx1-ubyte')

test_img = load_data_img('mnist-dataset/versions/1/t10k-images.idx3-ubyte')
test_labels = load_data_labels('mnist-dataset/versions/1/t10k-labels.idx1-ubyte')


net = Network()
epochs = 8
for epoch in range(epochs):
    for i in range(len(train_img)):
        img = train_img[i]
        label = train_labels[i]
        target = np.zeros(10)
        target[label] = 1
        net.train(img, target, lr=0.01)
    print(f'Epoch {epoch + 1}/{epochs} completed.')
    


print("\n--- Rozpoczynam testowanie ---")
correct = 0

for i in range(len(test_img)):
    # 1. Pobierz obrazek testowy
    img = test_img[i]
    true_label = test_labels[i]
    
    # 2. Przepuść przez sieć (tylko predict!)
    output = net.predict(img)
    
    # 3. Wybierz cyfrę z najwyższym prawdopodobieństwem
    # np.argmax([0.1, 0.0, 0.8, 0.1]) zwróci indeks 2
    predicted_label = np.argmax(output)
    
    # 4. Sprawdź czy sieć trafiła
    if predicted_label == true_label:
        correct += 1

accuracy = (correct / len(test_img)) * 100
print(f"Wynik na zbiorze testowym: {correct}/{len(test_img)}")
print(f"Skuteczność: {accuracy:.2f}%")
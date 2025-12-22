import tensorflow as tf
from tensorflow.keras.datasets import mnist #type: ignore
from tensorflow.keras.utils import to_categorical #type: ignore

(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train, x_test = x_train[...,None] / 255.0, x_test[...,None] / 255.0
y_train, y_test = to_categorical(y_train), to_categorical(y_test)

model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(10, activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(x_train, y_train, epochs=5, batch_size=64, validation_split=0.1)
print("Test accuracy:", model.evaluate(x_test, y_test)[1])
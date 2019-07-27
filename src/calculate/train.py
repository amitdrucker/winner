from numpy.random import seed

from prepareDF import prepareDf

seed(1)
from tensorflow import set_random_seed

set_random_seed(2)
import tensorflow as tf


def train(test_year):
    x_train, x_test, y_train, y_test, x_test_rounds = prepareDf(test_year)
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Flatten())
    model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu))
    model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu))
    model.add(tf.keras.layers.Dense(10, activation=tf.nn.softmax))
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    model.fit(x_train, y_train, epochs=160)
    val_loss, val_acc = model.evaluate(x_test, y_test)
    print(val_acc)
    print(val_loss)

    model.save('epic_num_reader.model')

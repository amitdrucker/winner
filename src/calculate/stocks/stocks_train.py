from numpy.random import seed
from tensorflow.python.keras.optimizers import SGD

from stocks.stocks_prepareDF import prepareDf

seed(1)
from tensorflow import set_random_seed

set_random_seed(2)
import tensorflow as tf


def train(test_year):
    x_train, x_test, y_train, y_test = prepareDf(test_year)
    model = tf.keras.models.Sequential()
    # model.add(tf.keras.layers.Flatten())
    model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu))
    model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu))
    model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu))
    model.add(tf.keras.layers.Dense(10, activation=tf.nn.softmax))
    sgd = SGD(lr=0.01, decay=1e-6, momentum=0.019)
    model.compile(optimizer=sgd,
                  loss='binary_crossentropy',
                  metrics=['accuracy'])
    model.fit(x_train, y_train, epochs=10)
    val_loss, val_acc = model.evaluate(x_test, y_test)
    print(val_acc)
    print(val_loss)

    model.save('epic_num_reader.model')

import tensorflow as tf
import keras
import numpy as np
from keras.models import Sequential, load_model
from keras.layers import Dense
from global_config import KERAS_MODEL_PATH
from global_config import file_access


def create_uniform_model(input_shape, hidden_layers=(50, 50, 10, 10, 1), activation='elu'):
    model = Sequential()

    layer1 = Dense(units=hidden_layers[0],
                   input_shape=(input_shape,),
                   use_bias=True,
                   kernel_initializer='random_uniform',
                   bias_initializer='random_uniform',
                   activation=activation)
    model.add(layer1)

    for i in range(1, len(hidden_layers)):
        layer = Dense(units=hidden_layers[i],
                      use_bias=True,
                      kernel_initializer='random_uniform',
                      bias_initializer='random_uniform',
                      activation=activation)
        model.add(layer)
    opt = keras.optimizers.Adam(lr=0.001, beta_1=0.9, beta_2=0.999,
                                epsilon=None, decay=0.0, amsgrad=False)
    model.compile(optimizer=opt, loss='mse')
    return model


def train_net(inputs, outputs, test_inputs, test_outputs, load=False):
    inputs = np.asarray(inputs)
    outputs = np.asarray(outputs)
    test_inputs = np.asarray(test_inputs)

    if load and file_access(KERAS_MODEL_PATH):
        print("Loading model from", KERAS_MODEL_PATH)
        model = load_model(KERAS_MODEL_PATH)
    else:
        model = create_uniform_model(inputs.shape[1])
        # early_stopping = keras.callbacks.EarlyStopping(monitor='val_loss',
        #                                                min_delta=5 * 10 ** -6, patience=20,
        #                                                verbose=0, mode='auto',
        #                                                baseline=None,
        #                                                restore_best_weights=True)

        # model.fit(x=inputs, y=outputs,
        #           validation_data=(val_in, val_out),
        #           epochs=1000, callbacks=[early_stopping], verbose=1)
        print(model.summary())
        model.fit(x=inputs, y=outputs, epochs=1000, verbose=1)
    return model, model.predict(x=test_inputs)


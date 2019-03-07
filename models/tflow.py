import tensorflow as tf
import keras
from keras.models import Sequential
from keras.layers import Dense


def create_uniform_model(input_shape, hidden_layers=(50, 50, 10, 10), activation='elu'):
    model = Sequential()
    for i in range(len(hidden_layers)):
        layer = Dense(units=hidden_layers[i],
                      use_bias=True,
                      kernel_initializer='random_uniform',
                      bias_initializer='random_uniform,',
                      input_shape=(input_shape,),
                      activation=activation)
        input_shape=hidden_layers[i]
        model.add(layer)
    opt = keras.optimizers.Adam(lr=0.001, beta_1=0.9, beta_2=0.999,
                                epsilon=None, decay=0.0, amsgrad=False)
    model.compile(optimizer=opt, loss='mse')
    return model


def train_net(inputs, outputs, test_inputs, test_outputs):
    sess = tf.Session(config=tf.ConfigProto(log_device_placement=True))
    model = create_uniform_model(len(inputs))
    # early_stopping = keras.callbacks.EarlyStopping(monitor='val_loss',
    #                                                min_delta=5 * 10 ** -6, patience=20,
    #                                                verbose=0, mode='auto',
    #                                                baseline=None,
    #                                                restore_best_weights=True)

    # model.fit(x=inputs, y=outputs,
    #           validation_data=(val_in, val_out),
    #           epochs=1000, callbacks=[early_stopping], verbose=1)
    model.fit(x=inputs, y=outputs, epochs=1000, verbose=1)
    return model.predict(x=test_inputs)


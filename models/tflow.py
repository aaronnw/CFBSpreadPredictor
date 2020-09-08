import keras
import numpy as np
from keras.models import Sequential, load_model
from keras.layers import Dense
from global_config import KERAS_MODEL_PATH
from utils import file_access


def eval_net(net, inputs, outputs):
    inputs = np.asarray(inputs)
    outputs = np.asarray(outputs)
    correct = 0
    incorrect = 0
    spread_covered = 0
    spread_not_covered = 0
    prediction = net.predict(inputs)
    off_amounts = []
    for prediction, output in zip(prediction, outputs):
        diff = abs(prediction - output)
        off_amounts.append(diff)
        if output > prediction:
            spread_covered += 1
        else:
            spread_not_covered += 1
        if output * prediction > 0:
            correct += 1
        else:
            incorrect += 1

    avg_off = float(np.mean(off_amounts))
    std_off = float(np.std(off_amounts))
    accuracy = float(correct / (correct + incorrect))
    coverage = float(spread_covered / (spread_covered + spread_not_covered))
    print("\n")
    print("On test data:")
    print("Average points off: " + str(avg_off))
    print("Std of points off: " + str(std_off))
    print("Accuracy: " + str(accuracy))
    print("Spread coverage percentage: " + str(coverage))
    return [avg_off, std_off, accuracy, coverage]

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


from sklearn.neural_network import MLPRegressor
import numpy as np
from collections import defaultdict

results = defaultdict(list)


def eval_net(net, inputs, outputs, name, type):
    print("Evaluating " + type + " data " + name)
    correct = 0
    incorrect = 0
    spread_covered = 0
    spread_not_covered = 0
    prediction = net.predict(inputs)
    off_amounts = []
    for prediction, output in zip(prediction, outputs):
        # print(name + " | Prediction: " + str(prediction) + "| Actual: " + str(output))
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
    # print("\n")
    # print("Data: " + type)
    # print(name + " | Average points off: " + str(avg_off))
    # print(name + " | Std of points off: " + str(std_off))
    # print(name + " | Accuracy: " + str(accuracy))
    # print(name + " | Spread coverage percentage: " + str(coverage))
    return [avg_off, std_off, accuracy, coverage]


def train_net(net, name, inputs, outputs, test_inputs, test_outputs):
    global results
    net.fit(inputs, outputs)
    training_result = eval_net(net, inputs, outputs, name, "Training")
    test_result = eval_net(net, test_inputs, test_outputs, name, "Test")
    results[name+"-training"].append(training_result)
    results[name+"-test"].append(test_result)


def train_conventional(inputs, outputs, test_inputs, test_outputs):
    global results
    # Config for 2 hidden layers of size of inputs
    layer1_size = int(len(inputs))
    layer2_size = int(len(inputs))
    net_even = MLPRegressor(hidden_layer_sizes = (layer1_size,layer2_size), max_iter=1000, early_stopping=True)
    train_net(net_even, "Even Net", inputs, outputs, test_inputs, test_outputs)

    # Config for 2 hidden layers of size both half of inputs
    layer1_size = int(0.5*len(inputs))
    layer2_size = int(0.5*len(inputs))
    net_half = MLPRegressor(hidden_layer_sizes = (layer1_size,layer2_size), max_iter=1000, early_stopping=True)
    train_net(net_half, "Half size Net", inputs, outputs, test_inputs, test_outputs)

    # Config for 2 hidden layers of size both double inputs
    layer1_size = int(2 * len(inputs))
    layer2_size = int(2 * len(inputs))
    net_double = MLPRegressor(hidden_layer_sizes=(layer1_size, layer2_size), max_iter=1000, early_stopping=True)
    train_net(net_double, "Double size Net", inputs, outputs, test_inputs, test_outputs)

    # Config for 2 hidden layers, 1st size of inputs, 2nd half of inputs
    layer1_size = int(len(inputs))
    layer2_size = int(0.5*len(inputs))
    net_funnel = MLPRegressor(hidden_layer_sizes = (layer1_size,layer2_size), max_iter=1000, early_stopping=True)
    train_net(net_funnel, "Funnel Net", inputs, outputs, test_inputs, test_outputs)

    # Config for 2 hidden layers, 1st double size of inputs, 2nd half of inputs
    layer1_size = int(2*len(inputs))
    layer2_size = int(0.5*len(inputs))
    net_large_funnel = MLPRegressor(hidden_layer_sizes = (layer1_size,layer2_size), max_iter=1000, early_stopping=True)
    train_net(net_large_funnel, "Large funnel Net", inputs, outputs, test_inputs, test_outputs)

    return results



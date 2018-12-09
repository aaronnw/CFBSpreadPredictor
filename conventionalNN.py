from sklearn.neural_network import MLPRegressor

def train_net(net, name, inputs, outputs):
    net.fit(inputs, outputs)
    correct = 0
    incorrect = 0
    sum_dist = 0
    spread_covered = 0
    spread_not_covered = 0
    prediction = net.predict(inputs)
    for prediction, output in zip(prediction, outputs):
        #print(name + " | Prediction: " + str(prediction) + "| Actual: " + str(output))
        sum_dist += abs(prediction - output)
        if output > prediction:
            spread_covered += 1
        else:
            spread_not_covered += 1
        if output * prediction > 0:
            correct += 1
        else:
            incorrect += 1
    print(name + " | Average points off: " + str(sum_dist / len(inputs)))
    print(name + " | Accuracy: " + str(correct / (correct + incorrect)))
    print(name + " | Spread coverage percentage: " + str(spread_covered / (spread_covered + spread_not_covered)))


def train_conventional(inputs, outputs):
    #Config for 2 hidden layers of size of inputs
    layer1_size = int(len(inputs))
    layer2_size = int(len(inputs))
    net_even = MLPRegressor(hidden_layer_sizes = (layer1_size,layer2_size), max_iter=1000)
    train_net(net_even, "Even Net", inputs, outputs)

    #Config for 2 hidden layers of size both half of inputs
    layer1_size = int(0.5*len(inputs))
    layer2_size = int(0.5*len(inputs))
    net_half = MLPRegressor(hidden_layer_sizes = (layer1_size,layer2_size), max_iter=1000)
    train_net(net_half, "Half size Net", inputs, outputs)

    # Config for 2 hidden layers of size both double inputs
    layer1_size = int(2 * len(inputs))
    layer2_size = int(2 * len(inputs))
    net_double = MLPRegressor(hidden_layer_sizes=(layer1_size, layer2_size), max_iter=1000)
    train_net(net_double, "Double size Net", inputs, outputs)

    #Config for 2 hidden layers, 1st size of inputs, 2nd half of inputs
    layer1_size = int(len(inputs))
    layer2_size = int(0.5*len(inputs))
    net_funnel = MLPRegressor(hidden_layer_sizes = (layer1_size,layer2_size), max_iter=1000)
    train_net(net_funnel, "Funnel Net", inputs, outputs)

    #Config for 2 hidden layers, 1st double size of inputs, 2nd half of inputs
    layer1_size = int(2*len(inputs))
    layer2_size = int(0.5*len(inputs))
    net_large_funnel = MLPRegressor(hidden_layer_sizes = (layer1_size,layer2_size), max_iter=1000)
    train_net(net_large_funnel, "Large funnel Net", inputs, outputs)



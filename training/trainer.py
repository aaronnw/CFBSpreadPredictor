from collections import defaultdict
import numpy as np

from models import tflow
from models.conventionalNN import train_conventional
from models.tflow import train_net
from global_config import KERAS_MODEL_PATH


def train_scikit(inputs, outputs, test_inputs, test_outputs):
    results = defaultdict(list)
    for test in range(10):
        results = train_conventional(inputs, outputs, test_inputs, test_outputs)
    for net_name, net_results in results.items():
        print(net_name)
        for i in range(len(net_results[0])):
            avg_val = np.mean([entry[i] for entry in net_results])
            print(avg_val)
        print("\n")


def train_tf(inputs, outputs, test_inputs, test_outputs):
    model, results = train_net(inputs, outputs, test_inputs, test_outputs, load=True)
    avg_val = np.mean(results)
    tflow.eval_net(model, test_inputs, test_outputs)
    print("Saving model to", KERAS_MODEL_PATH)
    model.save(KERAS_MODEL_PATH)
    print("Average off by", avg_val)


class Trainer:
    def __init__(self, backend):
        self.backend = backend

    def train_model(self, train_data, validation_data, test_data):
        print("Using backend:", self.backend)
        if self.backend == "scikit":
            # scikit_net(all_inputs, all_outputs, test_inputs, test_outputs)
            print(self.backend)
        elif self.backend == "neat":
            # train_neat(all_inputs, all_outputs)
            print(self.backend)
        elif self.backend == "tf":
            # tf_net(all_inputs, all_outputs, test_inputs, test_outputs)
            print(self.backend)


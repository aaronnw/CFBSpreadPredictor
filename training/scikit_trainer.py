from collections import defaultdict

import numpy as np

from models.conventionalNN import train_conventional
from training.trainer import Trainer


class SciKitTrainer(Trainer):
    def train_model(self, train_data, validation_data, test_data):
        print("Using scikit backend for training")
        training_inputs, training_outputs = [x for x in zip(*train_data)]
        val_inputs, val_outputs = [x for x in zip(*validation_data)]

        results = defaultdict(list)
        for test in range(10):
            results = train_conventional(training_inputs, training_outputs, val_inputs, val_outputs)
        for net_name, net_results in results.items():
            print(net_name)
            for i in range(len(net_results[0])):
                avg_val = np.mean([entry[i] for entry in net_results])
                print(avg_val)
            print("\n")

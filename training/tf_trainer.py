import numpy as np

from models import tflow
from models.tflow import train_net
from global_config import KERAS_MODEL_PATH
from training.trainer import Trainer


class TFTrainer(Trainer):
    def train_model(self, train_data, validation_data, test_data):
        print("Using tensorflow backend for training")
        training_inputs, training_outputs = [x for x in zip(*train_data)]
        val_inputs, val_outputs = [x for x in zip(*validation_data)]

        model, results = train_net(training_inputs, training_outputs, val_inputs, val_outputs, load=True)
        avg_val = np.mean(results)
        tflow.eval_net(model, val_inputs, val_outputs)
        print("Saving model to", KERAS_MODEL_PATH)
        model.save(KERAS_MODEL_PATH)
        print("Average off by", avg_val)

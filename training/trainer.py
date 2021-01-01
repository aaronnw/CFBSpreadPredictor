from abc import ABC, abstractmethod


class Trainer(ABC):
    @abstractmethod
    def train_model(self, train_data, validation_data, test_data):
        pass

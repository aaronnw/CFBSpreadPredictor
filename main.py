import argparse

from training.preprocessor import prepare_data
from training.scikit_trainer import SciKitTrainer
from training.tf_trainer import TFTrainer
from training.trainer import Trainer


def start_api():
    print("api mode")


def start_training(trainer_type):
    scikit_trainer = SciKitTrainer()
    tf_trainer = TFTrainer()

    # X and Y values for each set
    print("Preparing training data")
    training_data, validation_data, test_data = prepare_data()
    print("Running training")
    if trainer_type == "tf":
        tf_trainer.train_model(training_data, validation_data, test_data)
    elif trainer_type == "pytorch":
        print("todo: add pytorch trainer")
    else:
        scikit_trainer.train_model(training_data, validation_data, test_data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Start the flask server api or start training a new model')
    parser.add_argument('-mode')
    parser.add_argument('-trainer')
    args = parser.parse_args()
    if args.mode == "training":
        start_training(args.trainer)
    else:
        start_api()

import argparse

from training.preprocessor import prepare_data
from training.trainer import Trainer


def start_api():
    print("api mode")


def start_training():
    scikit_trainer = Trainer("scikit")
    # X and Y values for each set
    print("Preparing training data")
    training_data, validation_data, test_data = prepare_data()
    print("Running training")
    scikit_trainer.train_model(training_data, validation_data, test_data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Start the flask server api or start training a new model')
    parser.add_argument('-mode')
    args = parser.parse_args()
    if args.mode == "training":
        start_training()
    else:
        start_api()

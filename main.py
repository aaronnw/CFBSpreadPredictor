import argparse

from training.preprocessor import prepare_data


def start_api():
    print("api mode")


def start_training():
    prepare_data()
    print("training mode")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Start the flask server api or start training a new model')
    parser.add_argument('-mode')
    args = parser.parse_args()
    if args.mode == "training":
        start_training()
    else:
        start_api()

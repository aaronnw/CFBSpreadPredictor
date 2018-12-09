import neat
import pickle
import os

config_file = "neat.ini"
all_inputs = []
all_outputs = []

def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        for input, output in zip(all_inputs, all_outputs):
            net_output = float(net.activate(input)[0]*200 - 100)
            genome.fitness -= (output - net_output)**2

def train_neat(inputs, outputs):
    global all_inputs
    global all_outputs
    all_inputs = inputs
    all_outputs = outputs
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)
    out = "winner.pkl"

    if os.path.isfile(out) and os.access(out, os.R_OK):
        with open(out, 'rb') as file:
            winner = pickle.load(file)
    else:
        print("Training NEAT network")
        p = neat.Population(config)
        p.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        p.add_reporter(stats)
        p.add_reporter(neat.Checkpointer(20))

        winner = p.run(eval_genomes, 1000)

        with open(out, 'wb') as f:
            pickle.dump(winner, f)

    print('\nBest genome:\n{!s}'.format(winner))

    # Show output of the most fit genome against training data.
    print('\nOutput:')
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
    correct = 0
    incorrect = 0
    for input, output in zip(all_inputs, all_outputs):
        net_output = winner_net.activate(input)[0]*200 - 100
        print("Actual: {!r} | Predicted: {!r}".format(output, net_output))
        if output * net_output > 0:
            correct += 1
        else:
            incorrect += 1
    print("Accuracy: " + str(correct/(correct+incorrect)))
    return True

#
# Informed Search Methods
#
# Packing items into boxes.
# Run with '-h' command-line argument to see usage.
# You do not want to change anything in here!
#
import argparse
import statistics
import simulation
import assign
import estimate

def read_weights(name):
    """
    Read the item weights from a file.
    :param name: Name of file to read
    :return: A list of item weights (in grams).
    """
    weights = []
    puzzle = []
    with open(name) as f:
        for line in f:
            if line:
                weights.append(int(line.strip()))
    return weights


# The main program.
# Set up and parse command-line arguments.
ap = argparse.ArgumentParser()
ap.add_argument("-g", "--gates", default=2, help="Number of gates.",type=int)
ap.add_argument("-c", "--cars",  default=6, help="Number of cars.", type=int)
ap.add_argument("-b", "--boxcap", default=1000, help="Box capacity.",type=int)
ap.add_argument("-t", "--time", default=0, help="Max allocation time.",type=float)
ap.add_argument("-f", "--file", default='weights.txt', help="Weight file.")
ap.add_argument("-i", "--improved", help="Use improved heuristic", action="store_true")
ap.add_argument("-d", "--debug", help="Increase output verbosity", action="store_true")
args = vars(ap.parse_args())
print(args)

# Read in the weights and compute somee statistics.
weights = read_weights(args['file'])
avg = statistics.mean(weights)
std = statistics.stdev(weights)
print( "Read in weight of", len(weights), "items (", avg, round(std,2), ")")

# Run the simulation.
if args['improved']:
    giveaway_estimator = estimate.InformedEstimator(args['gates'], args['boxcap'], avg, std)
else:
    giveaway_estimator = estimate.Estimator(args['gates'], args['boxcap'], avg, std)
assigner = assign.Assign(args['debug'], giveaway_estimator)
sim = simulation.Simulation(args['gates'],args['cars'],args['boxcap'])
sim.reset(assigner.assign, args['time'])
for w in weights:
    sim.step(w)
    if (args['debug']):
        print(sim)
for i in range(len(sim.cars)):
    sim.step(0)
    if (args['debug']):
        print(sim)

# Output number of boxes and some statistics.
n = len(sim.get_boxes())
print( 'Number of filled boxes:', n )
print( 'Box capacity:', sim.get_capacity() )
if n > 0:
    print('Avg: ', sum(sim.get_boxes())/n)
    print('Sum: ', sum(sim.get_boxes()))
    print('Min: ', min(sim.get_boxes()))
    print('Max: ', max(sim.get_boxes()))
    print('Time:', sim.get_total_time())
    print(sim.get_boxes())
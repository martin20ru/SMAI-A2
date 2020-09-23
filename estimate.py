class Estimator:

    def __init__(self, num_gates, capacity, avg, std ):
        assert (num_gates > 0)
        self.num_gates = num_gates
        self.capacity = capacity
        self.avg = avg
        self.std = std

    def get_giveaway(self, gates):
        # Estimate the future giveaway for the partially filled boxes at the gates.
        return 0

class InformedEstimator(Estimator):

    # IMPLEMENT THIS CLASS.

    def get_giveaway(self, gates):
        ...
        return 0

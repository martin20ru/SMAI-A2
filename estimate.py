# import math


class Estimator:

    def __init__(self, num_gates, capacity, avg, std ):
        assert (num_gates > 0)
        self.num_gates = num_gates
        self.capacity = capacity
        self.avg = avg
        self.std = std

    def get_giveaway(self, gates):
        # Estimate the future giveaway for the partially filled boxes at the gates.
        return [0 for _ in gates]


class InformedEstimator(Estimator):

    def __init__(self, num_gates, capacity, avg, std):
        Estimator.__init__(self, num_gates, capacity, avg, std)
        self.compute()
        return

    def compute(self):
        # You implement this (optional) in case you want to do some onetime pre-computations.
        return

    def get_giveaway(self, gates):
        # You implement this.
        # Estimate the future giveaway for the partially filled boxes at the gates.

        return [max(0, weight - (self.capacity - self.avg)) for weight in gates]

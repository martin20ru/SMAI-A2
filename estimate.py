from math import floor, exp
# if not using the anaconda distribution, you can install this package with 'pip install -U scipy'
from scipy.stats import norm


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
        self.comp = self.compute()
        return

    def compute(self):
        """Estimator's onetime pre-computation to create the lookup table of a heuristic to estimate the giveaway"""
        # You implement this (optional) in case you want to do some onetime pre-computations.

        # abbreviations for better readability
        cap = self.capacity
        avg = self.avg
        std = self.std

        times = int(cap // avg)  # number of fillets that fit in a box without giveaway (on average)
        heuristics = ("exp_gauss", "poly_gauss", "gauss_bells", "leaky_ReLU", "ReLU")
        heuristic = heuristics[0]  # choose heuristic

        # exponentially increasing gauss bells with spikes up and down
        if heuristic == "exp_gauss":
            # TODO try different values for k
            k_exp = times
            base_estimator = sum([(norm.pdf(range(cap), cap - avg * (2 * t), std))
                                  - (norm.pdf(range(cap), cap - avg * (2 * t - 1), std))
                                  for t in range(times)])
            estimator = [floor(exp(k_exp * w / cap) * base_estimator[w] * (avg / base_estimator[-1])) for w in range(cap)]
            return estimator

        ################################################################################################################

        # polynomially increasing gauss bells with spikes up and down
        if heuristic == "poly_gauss":
            k_ploy = 4
            base_estimator = sum([(norm.pdf(range(cap), cap - avg * (2 * t), std))
                                  - (norm.pdf(range(cap), cap - avg * (2 * t - 1), std))
                                  for t in range(times)]) ** k_ploy
            estimator = [floor((w / cap) * base_estimator[w] * (avg / base_estimator[-1])) for w in range(cap)]
            return estimator

        ################################################################################################################

        # gauss bells with increasing height * x
        if heuristic == "gauss_bells":
            base_estimator = sum([(norm.pdf(range(cap), cap - avg * t, std)) *
                                  (times - t) for t in range(times)])
            return [floor(base_estimator[w] * (avg / base_estimator[-1])) for w in range(cap)]

        ################################################################################################################


        # leaky ReLU
        if heuristic == "leaky_ReLU":
            k = 64  # 0todo find the best k
            return [w//k + max(0, (-w//k) + w - (cap - avg)) for w in range(cap)]

        ################################################################################################################

        # ReLU
        if heuristic == "ReLU":
            return [max(0, w - (cap - avg)) for w in range(cap)]

    def get_giveaway(self, gates):
        # You implement this.
        # Estimate the future giveaway for the partially filled boxes at the gates.

        return [self.comp[weight] for weight in gates]

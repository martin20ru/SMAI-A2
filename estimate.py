from math import exp
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

        times = int(cap / avg)  # number of fillets that fit in a box without giveaway (on average)
        heuristics = ("new_gauss", "exp_gauss", "poly_gauss", "gauss_bells", "leaky_ReLU", "ReLU")
        heuristic = heuristics[0]  # choose heuristic

        if heuristic == "new_gauss":
            k_exp = times
            estimator_base = norm.pdf(range(cap), cap, std)
            estimator_peak = sum([(norm.pdf(range(cap), cap - avg*t, std)) for t in range(times)])
            estimator = estimator_base - estimator_peak
            estimator = [exp(k_exp * w / cap) * estimator[w] for w in range(cap)]
            # align and rescale
            estimator -= min(estimator)
            estimator = [int(estimator[w] * (avg/estimator[-1]) + avg/2/estimator[0]) for w in range(cap)]
            estimator = [estimator[w] * w/cap for w in range(cap)]
            return estimator

        # exponentially increasing gauss bells with spikes up and down
        if heuristic == "exp_gauss":
            # OTODO try different values for k
            k_exp = times
            #estimator2 = sum([(norm.pdf(range(cap), cap - avg*t, std)) for t in range(times)])
            #estimator *= estimator2
            estimator = sum([(norm.pdf(range(cap), cap - avg * (2 * t), std))
                             - (norm.pdf(range(cap), cap - avg * (2 * t - 1), std))
                             for t in range(times)])
            estimator = [exp(k_exp * w / cap) * estimator[w] for w in range(cap)]
            # align and rescale
            estimator -= min(estimator)
            estimator = [int(estimator[w] * (avg/estimator[-1]) + avg/2/estimator[0]) for w in range(cap)]
            return estimator

        # polynomially increasing gauss bells with spikes up and down
        elif heuristic == "poly_gauss":
            k_poly = 4
            estimator = sum([((norm.pdf(range(cap), cap - avg * (2 * t), std))
                             - (norm.pdf(range(cap), cap - avg * (2 * t - 1), std)))
                             for t in range(times)])
            [print(w, estimator[w]) for w in range(len(estimator)) if estimator[w] != estimator[w]]
            # align and rescale
            estimator -= min(estimator)
            estimator = [estimator[w] * w ** k_poly for w in range(cap)]
            estimator = [int(estimator[w] * (avg/estimator[-1])) for w in range(cap)]
            return estimator

        # gauss bells with increasing height * x
        elif heuristic == "gauss_bells":
            estimator = sum([(norm.pdf(range(cap), cap - avg * t, std)) *
                             (times - t) for t in range(times)])
            return [int(avg / 2 + estimator[w] * (avg / estimator[-1])) for w in range(cap)]

        # leaky ReLU
        elif heuristic == "leaky_ReLU":
            k = 64  # OTODO find the best k
            return [w//k + max(0, (-w//k) + w - (cap - avg)) for w in range(cap)]

        # ReLU
        elif heuristic == "ReLU":
            return [max(0, w - (cap - avg)) for w in range(cap)]

        else:
            AssertionError("Please choose one of the above heuristics")

    def get_giveaway(self, gates):
        # You implement this.
        # Estimate the future giveaway for the partially filled boxes at the gates.

        return [self.comp[weight] for weight in gates]

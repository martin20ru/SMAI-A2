from timeit import default_timer as timer


class Assign:
    def __init__(self, debug, estimator):
        self.debug = debug
        self.estimator = estimator
        return

    def get_estimator(self):
        return self.estimator

    def assign(self, cars, gates, capacity, time):
        """
        Determines the gate number to dispatch the item in car[0].

        :param cars: List with weight of items.
        :param gates: List with weight of boxes at gates.
        :param capacity: Box capacity
        :param time: Maximum time (in seconds) allowed for allocation; if 0, then there are no time-limits.
        :return: The gate number to assign item in car[0]
        """

        def time_is_up(start, time):
            if time == 0:
                return False
            return timer() - start >= time

        def do_assign(w, g):
            """Assign a weight to a gate

            :param w: weight to be assigned to a gate
            :param g: gate being assigned the weight
            :return: information whether the gate has been filled up and the resulting giveaway
            """
            filled = False
            giveaway = 0
            gates[g] += w
            if gates[g] >= capacity:
                giveaway = gates[g] - capacity
                gates[g] = 0
                filled = True
            return (filled, giveaway)

        def undo_assign(w, g, info):
            """Undo an assignment of a weight to a box, given the information of the assignment"""
            filled, giveaway = info
            if filled:
                gates[g] = (capacity + giveaway) - w
            else:
                gates[g] -= w
            return

        def clear_assignments(d):
            for _ in range(len(cars)):
                if _ == d:
                    break
                undo_assign(cars[_], assign_table[_], infos[_])
            return

        # IMPLEMENT THIS ROUTINE
        # Suggestion: Use an iterative-deepening version of DFBnB.
        # Call 'self.estimator.get_giveaway(gates)' for the heuristic estimate of future giveaway
        start = timer()
        max_giveaway = capacity * len(gates)
        best_fit = [0 for _ in range(len(cars))]  # index=car, value=gate
        giveaways = [0 for _ in range(len(gates))]  # index=gate, value=giveaway
        infos = [(False, 0) for _ in range(len(cars))]  # index=car, value=(full,giveaway)
        assign_table = [-1 for _ in range(len(cars))]  # index=car, value=gate
        max_giveaway = capacity * len(gates)
        depth = 0
        for depth in range(len(cars)):
            for c in range(depth):
                for g in range(len(gates)):
                    infos[c] = do_assign(cars[c], g)
                    giveaway = sum(self.estimator.get_giveaway(gates))
                    # giveaway = sum(giveaways)
                    if max_giveaway > giveaway:
                        max_giveaway = giveaway
                        if c == 0:
                            best_fit[c] = g
                    undo_assign(cars[c], g, infos[c])
                infos[c] = do_assign(cars[c], best_fit[c])
                assign_table[c] = best_fit[c]
            if time_is_up(start, time): break
        # print("depth:", depth)

        # undo all assignments after search or timeout to restore entry state
        clear_assignments(depth)
        return best_fit[0]

from timeit import default_timer as timer


class Assign:
    def __init__(self, debug, estimator):
        self.debug = debug
        self.estimator = estimator
        return

    def get_estimator(self):
        return self.estimator

    def assign(self, cars, gates, capacity, time_limit):
        """
        Determines the gate number to dispatch the item in car[0].

        :param cars: List with weight of items.
        :param gates: List with weight of boxes at gates.
        :param capacity: Box capacity
        :param time_limit: Maximum time (in seconds) allowed for allocation; if 0, then there are no time-limits.
        :return: The gate number to assign item in car[0]
        """

        def time_is_up(start, time=time_limit):
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
            return filled, giveaway

        def undo_assign(w, g, info):
            """Undo an assignment of a weight to a box, given the information of the assignment"""
            filled, giveaway = info
            if filled:
                gates[g] = (capacity + giveaway) - w
            else:
                gates[g] -= w
            return

        def rec_dfbnb(current_depth, last_giveaway_depth, best_fit):
            """Recursive Depth-First Branch-and-Bound search (second try)

            :param current_depth: current search depth = number of cars
            :param last_giveaway_depth:
            :param best_fit: best solution for current iteration
            :return:
            """
            for current_gate in range(len(gates)):
                infos[current_depth] = do_assign(cars[current_depth], current_gate)
                giveaway_certain = sum([infos[_][1] for _ in range(current_depth+1)])
                current_fit[current_depth] = current_gate

                # if the first box fills the gate, immediately do it
                if current_depth == 0:
                    if infos[0] == (True, 0):
                        best_fit[0] = current_gate
                        best_giveaway[0] = current_gate
                        # unneeded
                        # last_giveaway_depth = 0
                        # undo_assign(cars[0], current_gate, (True, 0))
                        return True

                # prune too costly branches early
                if giveaway_certain > best_giveaway[current_depth]:
                    undo_assign(cars[current_depth], current_gate, infos[current_depth])
                    continue  # to next gate

                # go deeper
                if current_depth < depth:
                    rec_dfbnb(current_depth + 1, last_giveaway_depth, best_fit)

                # reached the iteration's depth to be explored
                else:
                    giveaway_estimate = sum(self.estimator.get_giveaway(gates))
                    # found a better solution
                    if giveaway_certain + giveaway_estimate < best_giveaway[current_depth]:
                        best_giveaway[current_depth] = giveaway_certain + giveaway_estimate
                        last_giveaway_depth = current_depth
                        best_fit[:] = current_fit[:]

                # don't forget to undo the weight assignment to gate !!!
                undo_assign(cars[current_depth], current_gate, infos[current_depth])
                if time_is_up(begin):
                    return False

        # IMPLEMENT THIS ROUTINE
        # Suggestion: Use an iterative-deepening version of DFBnB.
        # Call 'self.estimator.get_giveaway(gates)' for the heuristic estimate of future giveaway
        begin = timer()
        max_depth = len(cars)
        worst_giveaway = capacity * max_depth

        current_fit = [-1 for _ in range(max_depth)]
        best_fit_list = [-1 for _ in range(max_depth)]  # index=car, value=gate
        infos = [(False, 0) for _ in range(max_depth)]  # index=car, value=(full,giveaway)
        best_giveaway = [worst_giveaway for _ in range(max_depth)]

        depth = 0

        while depth < max_depth:
            # OTODO remove recursion -> BestFit
            # OTODO value ordering
            stop_search = rec_dfbnb(0, -1, best_fit_list)
            if time_is_up(begin) or stop_search: break
            else:
                depth += 1
        return best_fit_list[0]


class BestFit:
    """Class that stores all assignments and their respective giveaways"""
    def __init__(self, max_depth: int, depth: int, assignments: list, giveaways: list):
        self.max_depth = max_depth
        self.depth = depth
        self.assignments = assignments
        self.giveaways = giveaways

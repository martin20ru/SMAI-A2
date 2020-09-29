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
                if _ != d:
                    undo_assign(cars[_], assign_table[_], infos[_])
                else:
                    break
            # TODO: clear assign_table as well (or update it for next car)
            return

        def recursive_dfbnb1(current_depth, last_giveaway_depth):
            """DFBnB search with recursion (to be called iteratively)

            :param current_depth: depth of the current recursion
            :param last_giveaway_depth: recursion depth at which the last best solution was found
            :return:
            """
            if current_depth < depth:
                for current_gate in range(len(gates)):
                    if time_is_up(start, time): return

                    infos[current_depth] = do_assign(cars[current_depth], current_gate)
                    # DF, BnB later
                    if current_depth < depth - 1:
                        recursive_dfbnb1(current_depth + 1, last_giveaway_depth)
                    elif current_depth == depth - 1:
                        current_giveaway_estimate = sum(self.estimator.get_giveaway(gates))     # h
                        current_giveaway_certain = sum([infos[_][1] for _ in range(depth)])     # g
                        current_giveaway = current_giveaway_estimate + current_giveaway_certain  # f
                        # prune costly solution
                        if current_giveaway_certain > best_giveaway[current_depth]:
                            undo_assign(cars[current_depth], current_gate, infos[current_depth])
                            return
                        # found a better solution
                        elif current_giveaway < best_giveaway[current_depth] or current_depth > last_giveaway_depth:
                            best_giveaway[current_depth] = current_giveaway
                            best_fit[current_depth] = current_gate
                            last_giveaway_depth = current_depth
                            undo_assign(cars[current_depth], current_gate, infos[current_depth])
                            # found optimal solution
                            if current_giveaway == 0:
                                return
                        else:
                            undo_assign(cars[current_depth], current_gate, infos[current_depth])
                    else:
                        undo_assign(cars[current_depth], current_gate, infos[current_depth])

            # reached deepest recursion step to be explored currently (var 'depth')
            else:
                return

        # IMPLEMENT THIS ROUTINE
        # Suggestion: Use an iterative-deepening version of DFBnB.
        # Call 'self.estimator.get_giveaway(gates)' for the heuristic estimate of future giveaway
        start = timer()
        max_depth = len(cars)
        best_fit = [-1 for _ in range(max_depth)]  # index=car, value=gate
        giveaways = [0 for _ in range(len(gates))]  # index=gate, value=giveaway
        infos = [(False, 0) for _ in range(max_depth)]  # index=car, value=(full,giveaway)
        assign_table = [-1 for _ in range(max_depth)]  # index=car, value=gate
        max_giveaway = capacity * max_depth
        best_giveaway = [capacity * max_depth for _ in range(max_depth)]
        depth = 1
        best = 0

        while depth <= max_depth:
            recursive_dfbnb1(current_depth=0, last_giveaway_depth=-1)
            if time_is_up(start, time):
                break
            depth += 1
            best = best_fit[0]

        return best

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
        return max(0, best_fit[0])

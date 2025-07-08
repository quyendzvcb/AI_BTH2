from pyarrow import nulls


class Problem(object):
    def __init__(self, initial=None, goal=None, **kwds):
        self.__dict__.update(initial=initial, goal=goal, **kwds)

    def actions(self, state):
        raise NotImplementedError

    def result(self, state, action):
        raise NotImplementedError

    def is_goal(self, state):
        return state == self.goal

    def action_cost(self, s, action, s1):
        return 1

    def h(self, node):
        return 0


class RouteProblem(Problem):
    def actions(self, state):
        return self.map.neighbors[state]

    def result(self, state, action):
        return action if action in self.map.neighbors[state] else state

    def action_cost(self, s, action, s1):
        return self.map.distances.get((s, s1), self.map.distances.get((s1, s), float('inf')))
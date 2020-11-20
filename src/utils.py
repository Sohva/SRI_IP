from collections import defaultdict


class PreferenceHelper:

    def __init__(self, preferences):
        self.preferences = []
        for i, ls in enumerate(preferences):
            self.preferences.append([j - 1 for j in ls])
        self.n = len(preferences)
        self.ranks = defaultdict(lambda: 0)
        for u, prefs in enumerate(self.preferences):
            for index, v in enumerate(prefs):
                self.ranks[(u, v)] = index + 1

    def get_neighbours(self, i):
        return self.preferences[i]

    def get_neighbour_pairs(self):
        for v in range(self.n):
            for u in self.get_neighbours(v):
                yield (u, v)

    def get_edges(self):
        for v in range(self.n):
            for u in self.get_neighbours(v):
                if u < v:
                    yield (u, v)

    def get_non_edges(self):
        for v in range(self.n):
            for u in range(self.n):
                if u <= v and u not in self.get_neighbours(v):
                    yield u, v

    def get_preferred_neighbours(self, u, v):
        for i in self.get_neighbours(u):
            if i != v:
                yield i
            else:
                break

    def delta(self, i):
        deltas = defaultdict(lambda: 0)
        for u, prefs in enumerate(preferences):
            if i <= len(prefs):
                deltas[u, prefs[i - 1]] = 1
        return deltas

"""
assert ranks[9, 8] == 6
assert ranks[3, 4] == 8
assert delta(1)[3,9] == 1
assert delta(1)[3,7] == 0
assert delta(2)[5,7] == 1"""
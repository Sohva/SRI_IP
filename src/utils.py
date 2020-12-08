from collections import defaultdict

def read_instance(size, density=None, index=None, offset=1):
    if not type(size) == type(""):
        file = "C:\\Users\\Sofia\\Documents\\level5project\\SRI_IP\\data\\instances\\%d\\i-%d-%d-%d.txt" % (size, size, density, index)
    else:
        file = size
    with open(file) as f:
        preferences = []
        n = int(f.readline())
        for _ in range(n):
            line = f.readline()
            preferences.append([int(i) - offset for i in line.split()])
    return preferences

class PreferenceHelper:

    def __init__(self, preferences):
        self.preferences = preferences
        self.n = len(preferences)
        self.ranks = defaultdict(lambda: 0)
        self.max_pref_length = 0
        for u, prefs in enumerate(self.preferences):
            if len(prefs) > self.max_pref_length:
                self.max_pref_length = len(prefs)
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
        for u, prefs in enumerate(self.preferences):
            if i <= len(prefs):
                deltas[u, prefs[i - 1]] = 1
        return deltas

"""
assert ranks[9, 8] == 6
assert ranks[3, 4] == 8
assert delta(1)[3,9] == 1
assert delta(1)[3,7] == 0
assert delta(2)[5,7] == 1"""
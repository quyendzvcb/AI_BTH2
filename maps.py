from collections import defaultdict

def multimap(pairs):
    result = defaultdict(list)
    for key, val in pairs:
        result[key].append(val)
    return result

class Map:
    def __init__(self, links, locations=None, directed=False):
        if not directed:
            for (v1, v2) in list(links):
                links[v2, v1] = links[v1, v2]
        self.distances = links
        self.neighbors = multimap(links)
        self.locations = locations or defaultdict(lambda : (0, 0))
class dijtra:
    def __init__(self, graph, start, end):
        self.graph = graph
        self.start = start
        self.end = end
        self.visited = set()
        self.path = []
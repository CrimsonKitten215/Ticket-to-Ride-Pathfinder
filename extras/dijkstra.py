class Dijkstra:
    def __init__(self, start: str, end: str, places: list, distances: dict):
        self.places = places
        self.distances = distances
        self.start = start
        self.end = end

        self.route = {}
        for p in places:
            self.route[p] = ""

    def __minimum(self):
        """
        Returns the key with the smallest value
        """

        min_key = list(self.unexplored.keys())[0]
        for i in list(self.unexplored.keys())[1:]:
            if self.unexplored[i] < self.unexplored[min_key]:
                min_key = i
        return min_key

    def __add_to_path(self, old_place: str, new_place: str, added_dist: int):
        if new_place in self.unexplored.keys():
            distance = self.unexplored[old_place] + added_dist
            if distance < self.unexplored[new_place]:
                self.unexplored[new_place] = distance
                self.route[new_place] = old_place

    def __get_path(self, route: dict):
        """
        Retraces the path from the route
        :param route: The dictionary
        :return: Final path
        """

        path = {}
        next = self.end
        next2 = route[next]
        while next2 != "-1":
            try:
                path[(next, next2)] = self.distances[(next, next2)]
            except:
                path[(next2, next)] = self.distances[(next2, next)]
            next = next2
            next2 = route[next]
        return path

    def get_shortest_path(self):
        """
        Calculates the shortest path between 2 places
        :return: [path, distance]
        """

        self.unexplored = {p : float("inf") for p in self.places}
        self.unexplored[self.start] = 0
        self.route[self.start] = "-1"
        explore = self.__minimum()

        while self.unexplored and explore != self.end:
            for path in self.distances.items():
                if path[0][0] == explore:
                    self.__add_to_path(path[0][0], path[0][1], path[1])
                elif path[0][1] == explore:
                    self.__add_to_path(path[0][1], path[0][0], path[1])

            del self.unexplored[explore]
            explore = self.__minimum()

        path = self.__get_path(self.route)
        return [path, self.unexplored[explore]]
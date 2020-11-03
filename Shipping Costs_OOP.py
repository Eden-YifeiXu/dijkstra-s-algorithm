# Requirements:
    # use classes
    # Create a class called city(dots in graph)
    # Connect cities(lines in graph)
    # Create a class called path(shortest distance)


def get_key(dictionary, val):
    for key, value in dictionary.items():
        if val == value:
            return key
    return 'key does not exist'


class City:
    def __init__(self, cities, one_way):
        self.cities = cities
        self.one_way = one_way

    def dj(self, nodes, costs, start_node):
        """
        Dijkstra's algorithm for computing the minimum additive cost from a start node to all other nodes.
        :param nodes: all unique nodes
        :param costs: costs from one node to another
        :param start_node: start node
        :return: minimum additive cost from start node to all other nodes
        """
        unvisited_nodes = {node: None for node in nodes}
        visited_nodes = {}
        current_node = start_node
        current_cost = 0
        unvisited_nodes[current_node] = current_cost
        while True:
            for neighbor, cost in costs[current_node].items():
                if neighbor not in unvisited_nodes:
                    continue
                new_cost = current_cost + cost
                if unvisited_nodes[neighbor] is None or new_cost < unvisited_nodes[neighbor]:
                    unvisited_nodes[neighbor] = new_cost
            visited_nodes[current_node] = current_cost
            del unvisited_nodes[current_node]
            if not unvisited_nodes:
                break
            candidates = [node for node in unvisited_nodes.items() if node[1]]

            # we need the maximum, so sort from largest to smallest
            current_node, current_cost = sorted(candidates, key=lambda x: x[1], reverse=False)[0]
        return visited_nodes


    def make_two_way(self):
        network = self.one_way.copy()
        for k_outer, v_outer in self.one_way.items():
            for k_inner, v_inner in v_outer.items():
                if k_inner not in network:
                    network[k_inner] = {}
                if k_inner not in network[k_inner].keys():
                    network[k_inner][k_outer] = v_inner
        return network


    def generate_by_cost(self):
        for k_outer, v_outer in self.one_way.items():
            for k_inner, v_inner in v_outer.items():
                distance = self.one_way[k_outer][k_inner]
                cost = 0
                if distance > 2000:
                    cost += 0.002 * (distance - 2000) + 0.003 * 1000 + 0.004 * 500 + 0.005 * 500
                elif distance > 1000:
                    cost += 0.003 * (distance - 1000) + 0.004 * 500 + 0.005 * 500
                elif distance > 500:
                    cost += 0.004 * (distance - 500) + 0.005 * 500
                else:
                    cost += 0.005 * distance
                self.one_way[k_outer][k_inner] = cost
        return self.one_way


    def get_network(self,by_distance=True):
        if not by_distance:
            self.one_way = self.generate_by_cost()
        two_way = self.make_two_way()
        return cities, two_way


    def driver(self):
        print('\n\n')
        by_distance = input('Computing by (type 0 for distance or 1 for costs)? ')
        city_nodes, costs = self.get_network(by_distance = int(by_distance)==0)
        nodes = city_nodes.keys()
        start_city = input('What is the start city? ')
        start_node = get_key(city_nodes, start_city)
        paths = self.dj(nodes, costs, start_node)
        for k, v in paths.items():
            print(f'{start_city} : {city_nodes[k]} = {round(v, 4)}')




if __name__ == '__main__':
    cities = {1: 'Seattle', 2: 'San Francisco', 3: 'Las Vegas', 4: 'Los Angeles', 5: 'Denver',
              6: 'Minneapolis', 7: 'Dallas', 8: 'Chicago', 9: 'Washington, D.C.', 10: 'Boston',
              11: 'New York', 12: 'Miami'}

    one_way = {1: {2: 1306, 5: 2161, 6: 2661},
               2: {3: 919, 4: 629},
               3: {4: 435, 5: 1225, 7: 1983},
               5: {6: 1483, 7: 1258},
               6: {7: 1532, 8: 661},
               7: {9: 2113, 12: 2161},
               8: {9: 1145, 10: 1613},
               9: {10: 725, 11: 383, 12: 1709},
               10: {11: 338},
               11: {12: 2145}}

    city_obj = City(cities=cities, one_way=one_way)

    city_obj.driver()
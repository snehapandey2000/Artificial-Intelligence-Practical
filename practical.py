from collections import deque


class Graph:
    def __init__(self, adjac_lis):
        self.adjac_lis = adjac_lis

    def get_neighbors(self, v):
        return self.adjac_lis[v]

    # heuristic function
    def h(self, n):
        H = {
            'A': 9,
            'B': 1,
            'C': 3,
            'D': 4,
            'E': 1,
            'F': 5,
            'G1': 0,
            'G2': 0,
            'G3': 0,
            'S': 8,
        }

        return H[n]

    def a_star_algorithm(self, start):
        open_lst = set([start])
        closed_lst = set([])
        # poo has present distances from start to all other nodes
        # the default value is +infinity
        poo = {}
        poo[start] = 0
        # par contains an adjac mapping of all nodes
        par = {}
        par[start] = start
        while len(open_lst) > 0:
            n = None

            # it will find a node with the lowest value of f() -
            for v in open_lst:
                if n == None or poo[v] + self.h(v) < poo[n] + self.h(n):
                    n = v

            if n == None:
                print('Path does not exist!')
                return None

            # if the current node is the stop
            # then we start again from start
            if n == 'G1' or n == 'G2' or n == 'G3':
                reconst_path = []

                while par[n] != n:
                    reconst_path.append(n)
                    n = par[n]

                reconst_path.append(start)

                reconst_path.reverse()

                print('Path found: {}'.format(reconst_path))
                return reconst_path

            # for all the neighbors of the current node do
            for (m, weight) in self.get_neighbors(n):
                if m not in open_lst and m not in closed_lst:
                    open_lst.add(m)
                    par[m] = n
                    poo[m] = poo[n] + weight

                # otherwise, check if it's quicker to first visit n, then m
                # and if it is, update par data and poo data
                # and if the node was in the closed_lst, move it to open_lst
                else:
                    if poo[m] > poo[n] + weight:
                        poo[m] = poo[n] + weight
                        par[m] = n

                        if m in closed_lst:
                            closed_lst.remove(m)
                            open_lst.add(m)

            # remove n from the open_lst, and add it to closed_lst
            # because all of his neighbors were inspected
            open_lst.remove(n)
            closed_lst.add(n)

        print('Path does not exist!')
        return None


adjac_lis = {
    'A': [('G1', 10), ('E', 7)],
    'B': [('C', 2), ('F', 2)],
    'C': [('G3', 11)],
    'D': [('G2', 5), ('S', 6)],
    'E': [('G1', 2)],
    'F': [('D', 1)],
    'S': [('A', 3), ('B', 1), ('C', 5)]
}
graph1 = Graph(adjac_lis)
graph1.a_star_algorithm('S')

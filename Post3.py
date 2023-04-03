from ai_pkg.search import Graph, Problem, Node
from ai_pkg.utils import random, argmax_random_tie

# Node kota-kota tujuan
city_map = Graph(dict(
Sibiu = dict(Sibiu=0, Fagaras=99, Bucharest=232, Pitesti=143, Rimnicu=80, Craiova=175),
Fagaras = dict(Sibiu=99, Fagaras=0, Bucharest=211, Pitesti=82, Rimnicu=81, Craiova=169),
Bucharest = dict(Sibiu=232, Fagaras=211, Bucharest=0, Pitesti=101, Rimnicu=186, Craiova=152),
Pitesti = dict(Sibiu=143, Fagaras=82, Bucharest=101, Pitesti=0, Rimnicu=97, Craiova=138),
Rimnicu = dict(Sibiu=80, Fagaras=81, Bucharest=186, Pitesti=97, Rimnicu=0, Craiova=146),
Craiova = dict(Sibiu=175, Fagaras=169, Bucharest=152, Pitesti=138, Rimnicu=146, Craiova=0)
),directed=False)

# Representasi graf
distances = {}
class TSP_problem(Problem):
	def generate_neighbour(self, state):
		neighbour_state = state[:]
		left = random.randint(0, len(neighbour_state)-1)
		right = random.randint(0, len(neighbour_state)-1)
		if left > right:
			left, right = right, left
		neighbour_state[left: right + 1] = reversed(neighbour_state[left: right + 1])
		return neighbour_state

	def actions(self, state):
		return [self.generate_neighbour]

	def result(self, state, action):
		return action(state)

	def path_cost(self, state):
		cost = 0
		for i in range(len(state)-1):
			current_city = state[i]
			next_city = state[i+1]
			cost += distances[current_city][next_city]
		cost += distances[state[0]][state[-1]]
		return cost

	def value (self, state):
		return -1*self.path_cost(state)

# Hill Climbing
def hill_climbing(problem):
	def find_neighbors(state, number_of_neighbors=100):
		neighbors = []
		for i in range(number_of_neighbors):
			new_state = problem.generate_neighbour(state)
			neighbors.append(Node(new_state))
			state =  new_state
		return neighbors

	current = Node(problem.initial)
	while True:
		neighbors = find_neighbors(current.state)
		if not neighbors:
			break
		neighbor = argmax_random_tie(neighbors, key=lambda node: problem.value(node.state))
		if problem.value(neighbor.state) <= problem.value(current.state):
			break
		current.state = neighbor.state
	return current.state

# Kasus Traveling Salesman Problem
if __name__=='__main__':
	all_cities = []
	cities_graph = city_map.graph_dict

	for city_1 in cities_graph.keys():
		distances[city_1] = {}
		if(city_1 not in all_cities):
			all_cities.append(city_1)
		for city_2 in cities_graph.keys():
			if(cities_graph.get(city_1).get(city_2) is not None):
				distances[city_1] [city_2] = cities_graph.get(city_1).get(city_2)

# Jalankan program
tsp_problem = TSP_problem(all_cities)
result = hill_climbing(tsp_problem)
print(result)

# Total jarak
cost = tsp_problem.path_cost(result)
print('cost: ', cost) 
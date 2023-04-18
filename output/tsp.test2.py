import math
import itertools




def distance(city1, city2):
    x1, y1 = city1
    x2, y2 = city2
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)


count =0
def result(cities):
    shortest_distance = math.inf
    for path in itertools.permutations(cities):
        count +=1
        total_distance = sum(distance(path[i], path[i+1]) for i in range(len(path)-1))
        if total_distance < shortest_distance:
            shortest_distance = total_distance
            shortest_path = path
    return shortest_path, shortest_distance

cities = [(8, 31), (54, 97), (50, 50), (65, 16), (70, 47), (25, 100), (55, 74)]
shortest_path, shortest_distance = result(cities)
print(shortest_distance)
print(shortest_path)

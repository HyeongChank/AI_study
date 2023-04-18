import math
import itertools



f = open('./data/tsp30.txt', 'r')
num_cities = f.readline()

cities = []
for line in f.readlines():
    # 좌표는 튜플로 만들어야 함 자리 안 바뀌도록
    # eval 억지로 정리하는 함수 최대한 안 쓰도록
    cities.append(eval(line))
    
print(cities)
f.close()
#cities = [(0,0), (1,2), (3,1), (5,4), (4,6)]

def tsp(cities):
    shortest_distance = math.inf
    for path in itertools.permutations(cities):
        total_distance = sum(distance(path[i], path[i+1]) for i in range(len(path)-1))
        if total_distance < shortest_distance:
            shortest_distance = total_distance
            shortest_path = path
    print(shortest_distance)
    return shortest_path, shortest_distance

def distance(city1, city2):
    x1, y1 = city1
    x2, y2 = city2
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)




tsp(cities)
#print("Shortest path:", shortest_path)
#print("Shortest distance:", shortest_distance)


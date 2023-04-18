import itertools
import math
import random
# TODO : 인접행렬
def create_problem(filename):
    f = open(filename, 'r')
    num_cities = f.readline()
    num_cities = (int)(num_cities)
    print(num_cities)
    print(type(num_cities))
    locations = []
    for line in f.readlines():
        #print(line)
        # 좌표는 튜플로 만들어야 함 자리 안 바뀌도록
        # eval 억지로 정리하는 함수 최대한 안 쓰도록
        locations.append(eval(line))

    f.close()
    table = create_distance_table(num_cities, locations)
    return num_cities, locations, table

def create_distance_table(num_cities, locations):
    print("create_distance_table 넘어옴")
    table = []
    for i in range(num_cities):
        line=[]
        for k in range(num_cities):
            
            distance = math.sqrt(((locations[i][0] - locations[k][0])**2 + (locations[i][1] - locations[k][1])**2))
            line.append(distance)
        table.append(line)
        #print(line)    
    return table

def describe_problem(p):
    #print()
    n = p[0]
    print(f"num : {n}")
    locations = p[1]
    table = p[2]
    for i in range(n):
        print(f"{locations[i]}")
        print(len(table))

        if i% 5 ==4:
            print()
        pass

def random_init(p):
    # 결과가 shuffle! 해서 나와야 함
    print("random_init pass")
    # n = number_cities(30개)
    n = p[0]
    init = list(range(n))
    random.shuffle(init)
    #print(init)
    return init


def evaluate(current, p):

    #cost 출력
    cost =0
    num_cities, locations, table = p
    for i in range(num_cities):
        cost += table[current[i]][current[i-1]]
        #print(table[current[i]][current[i-1]])
        print(i, "번째 도시 합한 total distance : " , cost)
    return cost




if __name__ == '__main__':
    p = create_problem('./data/tsp30.txt')
    #describe_problem(p)
    init = random_init(p)
    print(init)
    print(evaluate(init,p))
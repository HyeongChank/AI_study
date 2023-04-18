import tsp_test
import random

LIMITS = 100
def first_choice(p):
    current = tsp_test.random_init(p)
    value_distance = tsp_test.evaluate(current, p)
    i=0
    while i< LIMITS:
        successor = random_mutant(current,p)
        _value_distance = tsp_test.evaluate(successor,p)
        if _value_distance < value_distance:
            current = successor
            value_distance = _value_distance
            i =0
        else:
            i+=1
        
    ## 알고리즘 활용해서 최적값을 변경 코드 작성

    return current, value_distance

def random_mutant(current, p):
    while True:
        # [a,b] 만듬
        i, j = sorted([random.randrange(p[0]) for _ in range(2)])
        print("i", i, "j" , j)
        cur_copy = current[:]
        if i < j:
            cur_copy = inversion(current, i, j)
        break
    return cur_copy

def inversion(current, i, j):
    cur_copy = current[:]
    while i< j: 
        cur_copy[i], cur_copy[j] = cur_copy[j], cur_copy[i]
        i += 1
        j -= 1
    return cur_copy


if __name__ == '__main__':
    p = tsp_test.create_problem('./data/tsp30.txt')
    solution, minimum = first_choice(p)
    print(solution)
    print(minimum)
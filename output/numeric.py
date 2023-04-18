# def inc(x):
#     return x+1

# def test_answer():
#     assert inc(3) ==5

##간단한 언덕 등반 알고리즘
##Convex.txt 파일을 사용해서 계산
## 1.

# def convex(x1,x2, x3, x4, x5):
#     return (x1 - 2) ** 2 +5 * (x2 - 5) ** 2 + 8 * (x3 + 8) ** 2 + 3 * (x4 + 1) ** 2 + 6 * (x5 - 7) ** 2

# result = convex(5,5,5,5,5)
# print(result)

import random
def create_problem(filename):
    #1-1.파일을 읽자
    init_file = open(filename, 'r')
    # 개행문자 없애기(strip)
    expression = init_file.readline().strip()
    var_names = []
    low = []
    up = []

    for line in init_file.readlines():
        x,y,z = tuple(line.split(","))
        var_names.append(x)
        low.append(float(y))
        up.append(float(z))
        
    init_file.close()    
    domain = [var_names, low, up]
    print(domain)
        #print(x,y,z)
    #1-2. 수식과 리스트로 분리
    #1-3. 리턴
    return expression, domain

def random_init(p):
    expression, domain = p
    init = []
    for i in range(0, len(domain[0])):
        #최대 최소 사이의 랜덤 선택
        init.append(random.uniform(domain[1][i], domain[2][i]))
        pass
    return init



def evaluate(state, p):
    num_eval = 0
    expression= p[0]
    var_name = p[1][0]

    for i in range(len(var_name)):
        assignment = var_name[i] + '=' + str(state[i])

 
        exec(assignment)

    return eval(expression)

def test():
    #exec, eval 문자열이 실행됨    
    exec("print(random.uniform(-30,30))")
    eval("print(random.uniform(-30,30))")

# if __name__ == "__main__": 지점부터 읽음(엔트리 포인트)
if __name__ == "__main__":
    #식과 인자를 분리
    print(create_problem("./data/Convex.txt"))
    test()
    #식과 인자를 출력
    
    #초기값 결정

    #
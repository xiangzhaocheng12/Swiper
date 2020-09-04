import random
import copy

def sequence_generator():
    N = int(input('N = '))
    M = int(input('M = '))
    N_len = N
    res = []

    for i in range(M):
        N = [j for j in range(N_len)]
        n = copy.deepcopy(N)
        for j in range(len(n)):
            if len(res) == M:
                break
            num = random.choice(n)
            n.remove(num)
            res.append(str(num))
    return res


a = sequence_generator()
print(','.join(a))

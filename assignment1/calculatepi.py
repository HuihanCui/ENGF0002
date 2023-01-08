import random

def estimate_pi(precision):
    hit = 0
    for i in range(precision):
        a = random.random()
        b = random.random()
        if (a - 0.5)** 2 + (b - 0.5)** 2 <= 0.5 ** 2:
            hit += 1
    return 4 * hit / precision

pi = estimate_pi(100000)
print(pi)    
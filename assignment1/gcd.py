def gcd(a,b):
    while not a == b:
        if a > b:
            a = a - b
        else:
            b = b - a
    return a

ax = 42
bx = 30
print("GCD of", ax, "and", bx, "is", gcd(ax,bx))
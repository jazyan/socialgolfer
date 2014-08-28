import itertools
import random
from math import sqrt

def field_prime (order):
    c_scalar = [i for i in range(order)]
    points = [(i, j) for i in range(order) for j in range(order)]
    equ_class = [(1, b) for b in range(order)] + [(0, 1)]
    lines = {(a, b, c):[] for (a, b) in equ_class for c in c_scalar}
    nums = {pt:i for (i, pt) in enumerate(points)}
    for (x, y) in points:
        for (a, b, c) in lines:
            if (a*x + b*y + c)%order == 0:
                lines[(a, b, c)].append(nums[(x, y)])
    for (a, b) in equ_class:
        print "-----"
        for c in c_scalar:
            print lines[(a, b, c)]

def rem_lead_0 (li):
    to_str = ''.join(map(str, li)).rstrip("0")
    return [int(i) for i in to_str]

def polydiv (dividend, divisor, p):
    # poly a0 + a1*x + a2*x^2 + ... + an*x^n is [a0, a1, ..., an]
    divisor = rem_lead_0(divisor)
    dividend = rem_lead_0(dividend)
    deg_ans = len(dividend) - len(divisor)
    ans = [0 for i in range(deg_ans + 1)]
    while len(dividend) >= len(divisor):
        deg_ans = len(dividend) - len(divisor)
        for i in range(p):
            if (divisor[-1]*i)%p == dividend[-1]:
                coeff = i
        ans[deg_ans] = coeff
        carry = [0 for i in range(deg_ans)] + [(coeff * i)%p for i in divisor]
        dividend = [(dividend[i] - carry[i])%p for i in range(len(dividend))]
        dividend = rem_lead_0(dividend)
    if dividend == []:
        return ans

def rand_deg_poly (deg, p):
    poly = [1]
    for i in range(deg):
        z = random.randint(0, p-1)
        poly.insert(0, z)
    return poly

def gen_irreducible (deg, p):
    poly = rand_deg_poly (deg, p)
    div_deg = deg/2
    divisors = []
    for i in range(deg/2):
        poss_ints = [k for k in range(p)]*(i+2)
        div = list(set(itertools.combinations(poss_ints, i+2)))
        divisors += div
    divisors = [d for d in divisors if sum(d) > (p-1)]
    divisors.append((0, 1))
    score = 0
    while score != len(divisors):
        score = 0
        poly = rand_deg_poly (deg, p)
        for d in divisors:
            if polydiv(poly, d, p) != None:
                break;
            else:
                score += 1
    return poly

def fieldelts (p, n):
    acc = [i for i in range(p)]*n
    ans = list(set(itertools.combinations(acc, n)))
    assert len(ans) == pow(p, n)
    return ans

def polymult (p1, p2, p):
    ans = [0]*(len(p1)+len(p2)-1)
    for i1, c1 in enumerate(p1):
        for i2, c2 in enumerate(p2):
            ans[i1 + i2] = (ans[i1+i2] + (c1*c2)%p)%p
    ans = rem_lead_0(ans)
    return ans

# if len(ans) >= len(irr)
def polymod (poly, irr, p):
    deg = len(poly) - len(irr)
    while deg >= 0:
        x_deg = [0 for i in range(deg + 1)]
        for i in range(p):
            if (irr[-1]*i)%p == poly[-1]:
                coeff = i
        x_deg[-1] = coeff
        mod = polymult(x_deg, irr, p)
        poly = [(poly[i] - mod[i])%p for i in range(len(poly))]
        poly = rem_lead_0(poly)
        deg = len(poly) - len(irr)
    return poly

def polymultmod (p1, p2, irr, p):
    poly = polymult(p1, p2, p)
    poly = polymod(poly, irr, p)
    if poly == []:
        poly = [0]
    return poly

def multtable (irr, elts, p):
    L = len(elts)
    table = [[0 for i in range(L)] for j in range(L)]
    for i in range(L):
        for j in range(i, L):
            table[i][j] = polymultmod(elts[i], elts[j], irr, p)
            table[j][i] = table[i][j]
    return table

def field_prime_power (p, n):
    irred_poly = gen_irreducible (n, p)
    elts = fieldelts(p, n)
    mapped = {i:elts[i] for i in range(len(elts))}
    table = multtable(irred_poly, mapped, p)
    nums = {v:k for k, v in mapped.items()}
    iden_0 = tuple([0 for i in range(n)])
    iden_1 = tuple([1] + [0 for i in range(n-1)])

    points = [(i, j) for i in elts for j in elts]
    enum = {pt:i for (i, pt) in enumerate(points)}
    equ_class = [(iden_1, e) for e in elts] + [(iden_0, iden_1)]
    lines = {(a, b, c):[] for (a, b) in equ_class for c in elts}
    for (x, y) in points:
        for (a, b, c) in lines:
            L = len(c)
            ax = polymultmod(a, x, irred_poly, p)
            ax += [0 for i in range(L-len(ax))]
            by = polymultmod(b, y, irred_poly, p)
            by += [0 for i in range(L-len(by))]
            ans = [(ax[i] + by[i] + c[i])%p for i in range(L)]
            if tuple(ans) == iden_0:
                lines[(a, b, c)].append(enum[(x, y)])
    for (a, b) in equ_class:
        print "-----"
        for c in elts:
            print lines[(a, b, c)]

num_points = int(raw_input("How many points? "))

def prime_factor(n):
    ans = []
    i = 2
    while i*i < n:
        while n%i == 0:
            n /= i
            ans.append(i)
        i += 1
    return ans

small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
prime_fac = prime_factor(num_points)

if len(prime_fac)%2 == 0 and all(x == prime_fac[0] for x in prime_fac) and prime_fac[0] in small_primes:
    p = prime_fac[0]
    if len(prime_fac) == 2:
        field_prime(p)
    else:
        field_prime_power(p, len(prime_fac)/2)
else:
    print "Try another number next time! A square of a prime power."

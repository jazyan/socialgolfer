# Implementation of block design (n^2, n, 1) represented as an affine plane.
# For info on block designs: http://mathworld.wolfram.com/BlockDesign.html
# For info on affine planes: http://mathworld.wolfram.com/AffinePlane.html

import itertools
import random
from math import sqrt

# Finite affine planes have order q, q = p^n, p is prime and n >= 1
# They consist of ordered pairs of the finite field Fq

# If the order = p, then Fp has elt 0, 1, ..., p-1, with normal mod + and *
# Below creates the block design (q^2, q, 1), with prime q
def field_prime (order):
    c_scalar = [i for i in range(order)]
    points = [(i, j) for i in range(order) for j in range(order)]
    # equ_class contains slopes of the line. there are q+1 distinct slopes
    equ_class = [(1, b) for b in range(order)] + [(0, 1)]
    # lines are represented as ax + by + c = 0
    lines = {(a, b, c):[] for (a, b) in equ_class for c in c_scalar}
    # maps each point to a number
    nums = {pt:i for (i, pt) in enumerate(points)}

    # checks which points (x, y) are in line ax + by + c = 0
    for (x, y) in points:
        for (a, b, c) in lines:
            if (a*x + b*y + c)%order == 0:
                lines[(a, b, c)].append(nums[(x, y)])

    # pretty printing of groups
    for (a, b) in equ_class:
        print "-----"
        for c in c_scalar:
            print lines[(a, b, c)]


# Below are defs that create Fq, where q = p^n, n >= 2
# If q = p^n where n >= 2, problem of 0-divisors
# For example: F4 != Z/4Z, because 2*2 = 0

# F4 thus is represented as F2[x]/f, where f is an irreducible poly with deg 2
# In general, Fq = Fp[x]/f, f deg = n
# We represent all the elements as vectors (a_0, a_1, a_2, ..., a_n-1)
# (a_0, a_1, a_2, ..., a_n-1) = a_0 + a_1*x + a_2*x^2 + ... + a_n-1*x^(n-1)

# remove leading zeros
# ex: (0, 1, 0) can be reduced to (0, 1) (where both vectors represent x)
def rem_lead_0 (li):
    to_str = ''.join(map(str, li)).rstrip("0")
    return [int(i) for i in to_str]


# polynomial long division
def polydiv (dividend, divisor, p):
    # avoids divide-by-zero errors
    divisor = rem_lead_0(divisor)
    dividend = rem_lead_0(dividend)
    deg_ans = len(dividend) - len(divisor)
    ans = [0] * (deg_ans + 1)

    # recursion to find coeffs of ans
    while len(dividend) >= len(divisor):
        deg_ans = len(dividend) - len(divisor)
        # mod division
        for i in range(p):
            if (divisor[-1]*i)%p == dividend[-1]:
                coeff = i
        ans[deg_ans] = coeff
        carry = [0] * deg_ans + [(coeff * i) % p for i in divisor]
        # update dividend
        dividend = [(dividend[i] - carry[i]) % p for i in range(len(dividend))]
        dividend = rem_lead_0(dividend)

    # return ans if no remainder
    if dividend == []:
        return ans


# find a random polynomial with deg n
def rand_deg_poly (n, p):
    poly = [1]
    for i in range(n):
        z = random.randint(0, p-1)
        poly.insert(0, z)
    return poly


# Generate poly with deg n randomly, and check if it is irreducible
def gen_irreducible (n, p):
    poly = rand_deg_poly (n, p)
    divisors = []

    # if irreducible, it has no factors with lower deg
    # sufficient to check factors with deg <= n/2
    for i in range(n/2):
        poss_ints = [k for k in range(p)]*(i+2)
        div = list(set(itertools.combinations(poss_ints, i+2)))
        divisors += div

    # careful! (1, 0) will divide everything
    divisors = [d for d in divisors if sum(d) > (p-1)]
    # add back the factor x
    divisors.append((0, 1))

    # check all the factors
    score = 0
    while score != len(divisors):
        score = 0
        poly = rand_deg_poly (n, p)
        for d in divisors:
            if polydiv(poly, d, p) != None:
                break;
            else:
                score += 1

    # around 1/n of polys with deg n are irreducible -> expected n trials
    return poly


# Generate elements of Fq
def fieldelts (p, n):
    acc = [i for i in range(p)]*n
    ans = list(set(itertools.combinations(acc, n)))
    return ans


# Polynomial multiplication using convolution
def polymult (p1, p2, p):
    ans = [0] * (len(p1) + len(p2) - 1)
    for i1, c1 in enumerate(p1):
        for i2, c2 in enumerate(p2):
            ans[i1 + i2] = (ans[i1 + i2] + (c1 * c2) % p) % p
    ans = rem_lead_0(ans)
    return ans


# Fq/f means that we mod by f. Defined below is modding a poly by f
def polymod (poly, f, p):
    deg = len(poly) - len(f)
    while deg >= 0:
        x_deg = [0] * (deg + 1)

        # mod p division
        for i in range(p):
            if (f[-1] * i) % p == poly[-1]:
                coeff = i
        x_deg[-1] = coeff
        mod = polymult(x_deg, f, p)

        # update f
        poly = [(poly[i] - mod[i]) % p for i in range(len(poly))]
        poly = rem_lead_0(poly)
        deg = len(poly) - len(f)
    return poly


# Poly multiplication mod by the irreducible poly f
def polymultmod (p1, p2, f, p):
    poly = polymult(p1, p2, p)
    poly = polymod(poly, f, p)
    if poly == []:
        poly = [0]
    return poly


# Do not need to create addition table for Fq, add vector components mod p
# Creates the multiplication table for Fq
def multtable (irr, elts, p):
    L = len(elts)
    table = [[0 for i in range(L)] for j in range(L)]
    for i in range(L):
        for j in range(i, L):
            table[i][j] = polymultmod(elts[i], elts[j], irr, p)
            table[j][i] = table[i][j]
    return table


# We can now create our finite affine plane of order q = p^n
def field_prime_power (p, n):
    # find an irreducible poly f to mod by
    f = gen_irreducible (n, p)
    # generate the field elements
    elts = fieldelts(p, n)

    # map the elements to a number (makes generating the table easier)
    mapped = {i : elts[i] for i in range(len(elts))}
    # generate the multiplcation table
    table = multtable(f, mapped, p)

    # the two field identities
    # need to convert to tuples. The dict cannot hash lists
    iden_0 = tuple([0] * n)
    iden_1 = tuple([1] + [0] * (n-1))

    # the points in the affine plane
    points = [(i, j) for i in elts for j in elts]

    # mapping the points to numbers (for display purposes)
    enum = {pt : i for (i, pt) in enumerate(points)}

    # equ_class has all (q + 1) unique slopes of the lines
    equ_class = [(iden_1, e) for e in elts] + [(iden_0, iden_1)]
    lines = {(a, b, c):[] for (a, b) in equ_class for c in elts}

    # checking which points are in which lines
    for (x, y) in points:
        for (a, b, c) in lines:
            L = len(c)
            ax = polymultmod(a, x, f, p)
            by = polymultmod(b, y, f, p)
            # pad ax and by by 0s to have same length as c
            ax += [0] * (L-len(ax))
            by += [0] * (L-len(by))
            ans = [(ax[i] + by[i] + c[i])%p for i in range(L)]
            # if ax + by + c = 0
            if tuple(ans) == iden_0:
                lines[(a, b, c)].append(enum[(x, y)])

    # pretty printing
    for (a, b) in equ_class:
        print "-----"
        for c in elts:
            print lines[(a, b, c)]

def prime_factor(n):
    ans = []
    i = 2
    while i*i <= n:
        while n%i == 0:
            n /= i
            ans.append(i)
        i += 1
    return ans

num_points = int(raw_input("How many points? "))
small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
prime_fac = prime_factor(num_points)

print prime_fac

if len(prime_fac)%2 == 0 and all(x == prime_fac[0] for x in prime_fac) and prime_fac[0] in small_primes:
    p = prime_fac[0]
    if len(prime_fac) == 2:
        field_prime(p)
    else:
        field_prime_power(p, len(prime_fac)/2)
else:
    print "Try another number next time! A square of a prime power."

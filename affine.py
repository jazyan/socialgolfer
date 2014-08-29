##########################################################################
# Implementation of block design (n^2, n, 1) using finite affine planes.
# For info on block designs: http://mathworld.wolfram.com/BlockDesign.html
# For info on affine planes: http://mathworld.wolfram.com/AffinePlane.html
##########################################################################

import itertools
import random
from math import sqrt

##########################################################################
# Finite affine planes have order q, q = p^n, p is prime and n >= 1
# They consist of ordered pairs of the finite field Fq
# If the q = p, then Fp has elts 0, 1, ..., p-1, with + and * mod p
# Below creates the block design (q^2, q, 1), with prime q
##########################################################################

def field_prime (q):
    c_scalar = [i for i in range(q)]
    points = [(i, j) for i in range(q) for j in range(q)]
    # equ_class contains the (q+1) distinct line slopes
    equ_class = [(1, b) for b in range(q)] + [(0, 1)]
    # lines are represented as ax + by + c = 0
    lines = {(a, b, c):[] for (a, b) in equ_class for c in c_scalar}
    # maps each point to a number
    nums = {pt:i for (i, pt) in enumerate(points)}

    # checks which points (x, y) are in line ax + by + c = 0
    for (x, y) in points:
        for (a, b, c) in lines:
            if (a*x + b*y + c) % q == 0:
                lines[(a, b, c)].append(nums[(x, y)])

    # pretty printing of groups
    for (a, b) in equ_class:
        print "-----"
        for c in c_scalar:
            print lines[(a, b, c)]

#########################################################################
# Below are defs that create Fq, where q = p^n, n >= 2
# If q = p^n where n >= 2, problem of 0-divisors
# For example: F4 != Z/4Z, because 2*2 = 0
# F4 thus is represented as F2[x]/f, where f is an irreducible poly with deg 2
# In general, Fq = Fp[x]/f, f deg = n
# We represent all the elements as vectors (a_0, a_1, a_2, ..., a_n-1)
# (a_0, a_1, a_2, ..., a_n-1) = a_0 + a_1*x + a_2*x^2 + ... + a_n-1*x^(n-1)
#########################################################################

# removes leading zeros
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


# Return an irreducible poly with deg n.
# Poly with deg n generated randomly, then checked if they are irreducible
def gen_irreducible (n, p):
    poly = [random.randint(0, p-1) for i in range(n)] + [1]

    # sufficient to check factors with deg <= n/2
    while 1:
        for i in range(n/2):
            poss_ints = [k for k in range(p)]*(i+2)
            div = list(set(itertools.combinations(poss_ints, i+2)))
            for d in div:
                if sum(d) > (p-1) or d == (0, 1):
                    if polydiv(poly, d, p) != None:
                        br = 1
                        break;
            if br == 1:
                break;
        if i == (n/2 - 1):
            return poly
        else:
            poly = [random.randint(0, p-1) for i in range(n)] + [1]


# Generate elements of Fq, where q = p^n
def fieldelts (p, n):
    acc = [i for i in range(p)]*n
    ans = list(set(itertools.combinations(acc, n)))
    return ans


# Calculates p1 * p2 mod p, where p is a prime
def polymult (p1, p2, p):
    ans = [0] * (len(p1) + len(p2) - 1)
    for i1, c1 in enumerate(p1):
        for i2, c2 in enumerate(p2):
            ans[i1 + i2] = (ans[i1 + i2] + (c1 * c2) % p) % p
    ans = rem_lead_0(ans)
    return ans


# Calculates poly mod f mod p where f is an irreducible poly and p is a prime
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

# Calculates p1 * p2 mod f mod p
def polymultmod (p1, p2, f, p):
    poly = polymult(p1, p2, p)
    poly = polymod(poly, f, p)
    if poly == []:
        poly = [0]
    return poly


# Creates the multiplication table for Fq
# NOTE: addition in Fq is merely adding vector components mod p
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


def run ():
    num_points = int(raw_input("How many points? "))
    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
    prime_fac = prime_factor(num_points)

    # if it can be factored into an even number of a prime, it passes
    if len(prime_fac) % 2 == 0 and all(x == prime_fac[0] for x in prime_fac) and prime_fac[0] in small_primes:
        q = prime_fac[0]
        # if num = q^2, create Fq using field_prime
        if len(prime_fac) == 2:
            field_prime(q)
        # otherwise, need to use field_prime_power to create Fq
        else:
            field_prime_power(q, len(prime_fac)/2)
    else:
        print "I demand a square of a prime power!"

if __name__ == "__main__":
    run()

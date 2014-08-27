import itertools
import random

order = 5

scalar = [i for i in range(order) if i != 0]
c_scalar = [i for i in range(order)]

points = [(i, j) for i in range(order) for j in range(order)]
equ_class = [(1, b) for b in range(order)] + [(0, 1)]

print equ_class

lines = {(a, b, c):[] for (a, b) in equ_class for c in c_scalar}

nums = {(a, b):i for (i, (a, b)) in enumerate(points)}
print nums

for (x, y) in points:
    for (a, b, c) in lines:
        if (a*x + b*y + c)%order == 0:
            lines[(a, b, c)].append(nums[(x, y)])

print len(lines)
for (a, b) in equ_class:
    print "-----"
    for c in c_scalar:
        print (a, b, c), lines[(a, b, c)]

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
        #print "ans", ans, "divisor", divisor, "dividend", dividend
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
'''
print polydiv ([-1, 0, 1], [1, 1], 10)
test_divd = [0 for i in range(17)]
test_divd[1] = -1
test_divd[16] = 1
test_div = [1, 1, 0, 0, 1]
print polydiv (test_divd, test_div, 2)
'''
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
    print "DIVISORS", divisors
    score = 0
    while score != len(divisors):
        score = 0
        poly = rand_deg_poly (deg, p)
        print "POLY", poly
        for d in divisors:
            print d
            if polydiv(poly, d, p) != None:
                print "FAILED", d, polydiv(poly, d, p)
                break;
            else:
                score += 1
    print "POLY", poly
    return poly

print gen_irreducible (4, 2)



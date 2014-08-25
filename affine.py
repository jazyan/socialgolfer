order = 7

scalar = [i for i in range(order) if i != 0]
c_scalar = [i for i in range(order)]

points = [(i, j) for i in range(order) for j in range(order) if (i, j) != (0, 0)]

equ_class = []
for (a1, b1) in points:
    tally = 0
    test = []
    for s in scalar:
        if ((a1*s)%order, (b1*s)%order) not in equ_class:
            tally += 1
        else:
            test.append([s, (a1, b1), ((a1*s)%order,(b1*s)%order)])
            break;
    if tally == len(scalar):
        equ_class.append((a1, b1))

points.append((0,0))
print points
print len(points)
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

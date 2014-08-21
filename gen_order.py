import sys

order = 4
points = pow(order, 2) + order + 1

fout = open(sys.argv[1], 'w')
initial = [1, 3, 8, 9, 12]
tofile = ""

for i in range(points):
    shift = [(x + i)%points for x in initial]
    tofile = ' '.join(map(str, shift)) + "\n"
    fout.write(tofile)

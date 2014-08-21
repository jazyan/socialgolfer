import sys

fin = open(sys.argv[1], 'r')
T = []
while True:
    line = fin.readline()
    if not line: break
    line = line.replace(',', '')
    T.append(map(int, line.split()))
print T

lineinf = T.pop()
length = len(T[0]) - 1
print "LINE of INF", lineinf

new = []
for row in T:
    newrow = []
    for i in row:
        if i not in lineinf:
            newrow.append(i)
    new.append(newrow)

#toobig = [16, 17, 18, 19, 20]
easier = []
for row in new:
    print row
'''
    replace = []
    for elt in row:
        if elt in toobig:
            ind = toobig.index(elt)
            replace.append(lineinf[ind])
        else:
            replace.append(elt)
    easier.append(sorted(replace))

easier = sorted(easier, key = lambda k: k[0])
groups = [[] for i in range(5)]
for i in range(5):
    groups[i].append(easier[i][:])
    for j in range(i, len(easier)):
        if len(set(easier[j] + easier[i])) == 8:
            groups[i].append(easier[j])

print groups
inc = 0
for row in groups:
    print inc, row
    inc += 1
'''

import itertools

# G = num of groups, P = num of people/group, W = num of weeks
G, P, W = map(int, raw_input().split())

people = [i for i in range(G*P)]

# adjacency list
adj = {i:[] for i in range(G*P)}

# week0 is automatically the people in order
state0 = [people[i:i+P] for i in range(0, len(people), P)]

def updateadj (state):
# add elements to adjacency list
    for group in state:
        for elt in group:
            holder = group[:]
            holder.remove(elt)
            adj[elt] += holder

updateadj (state0)

# union of i and j's neighbors
def updatepairs (n):
    # create all possible pairs
    pairs = {(i, j):[] for i in range(G*P) for j in range(i+1, G*P)}
    for i in range(len(adj)):
        for j in range(i+1, len(adj)):
            pairs[(i, j)] = list(set(adj[i] + adj[j]))
    # all pairs that were used, and their reverse
    taken = [key for key, value in pairs.items() if len(value) <= n*P]
    rev = [(j, i) for (i, j), value in pairs.items() if len(value) <= n*P]
    taken += rev
    # remaining available pairs
    pairs = {key:value for key, value in pairs.items() if len(value) > n*P}
    # sort by least FREEDOM
    order = sorted(pairs, key=lambda k: len(pairs[k]), reverse = True)
    return taken, pairs, order

taken, pairs, order = updatepairs (1)

(i, j) = order[0]
state1 = [i, j]
copy = order[1:]
start = 0

while len(state1) != G*P:
    # if there is no more, we were too greedy. Need to backtrack
    if copy == []:
        (i, j) = state1[-2:]
        state1 = state1[:-2]
        # find where we were, and choose next one
        start = order.index((i, j))
        copy = order[start + 1:]
    (a, b) = copy.pop(0)
    # first check that (a, b) has not been used already
    if not(a in state1) and not(b in state1):
        # if we start a new group, we can add it
        if len(state1)%P == 0:
            start = order.index((a, b))
            state1.append(a)
            state1.append(b)
        # otherwise, we need to check within the group that it is valid
        else:
            currgroup = state1[-(P-2):] + [a, b]
            allpairs = list(itertools.combinations(currgroup, 2))
            tally = 0
            for (i, j) in allpairs:
                if not((i,j) in taken):
                    tally += 1
                else:
                    #print "DIDN'T WORK", (i, j)
                    break;
            if tally == len(allpairs):
                # all pairs are valid, so we can add (a, b)
                state1.append(a)
                state1.append(b)
                # start of new group: we can reconsider ones passed over
                if len(state1)%P == 0:
                    copy = order[start + 1:]
                # NOTE: later can delete already seen pairs to speed up

state1 = [state1[i:i+P] for i in range(0, len(people), P)]

print "STATE0", state0
print "STATE1", state1

print order[0], pairs[order[0]]
print order[-1], pairs[order[-1]]

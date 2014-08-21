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

def used (state):
    allpairs = []
    for group in state:
        allpairs += itertools.combinations(group, 2)
    rev = [(j, i) for (i, j) in allpairs]
    allpairs += rev
    return allpairs

# union of i and j's neighbors
def updatepairs (state):
    # create all possible pairs
    pairs = {(i, j):[] for i in range(G*P) for j in range(i+1, G*P)}
    for i in range(len(adj)):
        for j in range(i+1, len(adj)):
            pairs[(i, j)] = list(set(adj[i] + adj[j]))
    taken = used (state)
    # remaining available pairs
    pairs = {key:value for key, value in pairs.items() if key not in taken}
    # sort by least FREEDOM
    order = sorted(pairs, key=lambda k: len(pairs[k]), reverse = True)
    return taken, pairs, order

def createstate (order, pairs, taken):
    (i, j) = order[0]
    state = [i, j]
    copy = order[1:]
    start = 0

    while len(state) != G*P:
        # if there is no more, we were too greedy. Need to backtrack
        if copy == []:
            (i, j) = state[-2:]
            state = state[:-2]
            # find where we were, and choose next one
            start = order.index((i, j))
            copy = order[start + 1:]
        (a, b) = copy.pop(0)
        # first check that (a, b) has not been used already
        if not(a in state) and not(b in state):
            # if we start a new group, we can add it
            if len(state)%P == 0:
                start = order.index((a, b))
                state.append(a)
                state.append(b)
            # otherwise, we need to check within the group that it is valid
            else:
                currgroup = state[-(P-2):] + [a, b]
                allpairs = list(itertools.combinations(currgroup, 2))
                tally = 0
                for (i, j) in allpairs:
                    if (i,j) not in taken:
                        tally += 1
                    else:
                        break;
                if tally == len(allpairs):
                    # all pairs are valid, so we can add (a, b)
                    state.append(a)
                    state.append(b)
                    # start of new group: we can reconsider ones passed over
                    if len(state)%P == 0:
                        copy = order[start + 1:]
                    # NOTE: later can delete already seen pairs to speed up
    return state

def run(state, prevstates):
    updateadj (state)
    taken, pairs, order = updatepairs(prevstates + state)
    print "LARGEST", len(pairs[order[0]])
    print "SMALLEST", len(pairs[order[-1]])
    state = createstate(order, pairs, taken)
    return [state[i:i+P] for i in range(0, len(people), P)]

curr_state = state0
states = state0
print "state 0", state0
for i in range(W-1):
    next_state = run(curr_state, states)
    print "state", i+1, next_state
    states = states + next_state
    curr_state = next_state


#state1 = [[0, 4, 8, 12], [1, 5, 9, 13], [2, 6, 10, 14], [3, 7, 11, 15]]
#state2 = [[3, 6, 9, 12], [0, 7, 10, 13], [2, 5, 8, 15], [1, 4, 11, 14]]

#state3 = run(state2, state0 + state1 + state2)
#print state3

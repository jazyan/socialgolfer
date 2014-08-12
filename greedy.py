import itertools

G, P, W = map(int, raw_input().split())
people = [i for i in range(G*P)]

adj = {i:[] for i in range(G*P)}

state0 = [people[i:i+P] for i in range(0, len(people), P)]

for group in state0:
    for elt in group:
        holder = group[:]
        holder.remove(elt)
        adj[elt] += holder

pairs = {(i, j):[] for i in range(G*P) for j in range(i+1, G*P)}

for i in range(len(adj)):
    for j in range(i+1, len(adj)):
        pairs[(i, j)] = list(set(adj[i] + adj[j]))

order = sorted(pairs, key=lambda (i, j): len(pairs[(i,j)]), reverse = True)

print pairs[order[0]], pairs[order[len(order)-1]]

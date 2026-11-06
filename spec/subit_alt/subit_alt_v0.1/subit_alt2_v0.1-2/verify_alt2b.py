import itertools
from collections import Counter

S = list(itertools.product(range(4), repeat=3))
IDX = {x: i for i, x in enumerate(S)}
AX = [0, 1, 2]
NAMES = {0: 'w', 1: 'e', 2: 'n'}
G = {0: (1, 0), 1: (1, 1), 2: (0, 1), 3: (0, 0)}
Ginv = {v: k for k, v in G.items()}

def to_bits(x):
    b = []
    for c in x:
        b += list(G[c])
    return tuple(b)

def from_bits(b):
    return tuple(Ginv[(b[2*i], b[2*i+1])] for i in range(3))

def Nmap(x):
    b = to_bits(x)
    return from_bits((b[1], b[2], b[3], b[2], b[3], b[4]))

NN = [IDX[Nmap(x)] for x in S]

def power(f, k):
    g = list(range(64))
    for _ in range(k):
        g = [f[v] for v in g]
    return g

print("== 9.1 Powers of the nuclear map N on the 64 contexts ==")
for k in range(1, 6):
    print("  |image of N^%d| = %d" % (k, len(set(power(NN, k)))))
print("N^4 == N^2:", power(NN, 4) == power(NN, 2))
print("N^3 == N^2:", power(NN, 3) == power(NN, 2), " N^3 == N:", power(NN, 3) == NN)
per = sorted(set(power(NN, 2)))
print("periodic points (image of N^2):", [S[i] for i in per])
print("N^3 swaps the 2-cycle and fixes 111111/000000 (N^3 == N on periodic points):",
      all(power(NN, 3)[i] == NN[i] for i in per))

print("\n== 9.2 N versus the axis relations R_i ==")
def R(i, x, y):
    return all(x[k] == y[k] for k in AX if k != i)
for i in AX:
    pats = Counter()
    for x in S:
        for y in S:
            if x != y and R(i, x, y):
                nx, ny = Nmap(x), Nmap(y)
                pats[tuple(NAMES[k] for k in AX if nx[k] != ny[k])] += 1
    print("  pairs x R_%s y (x != y): patterns of axes where N x, N y differ:" % NAMES[i], dict(pats))

print("\n== 9.3 Basins and depth levels as propositions (invariance under box_i) ==")
cyc = set(per)
def attractor_id(i):
    while i not in cyc:
        i = NN[i]
    orb = [i]; j = NN[i]
    while j != i:
        orb.append(j); j = NN[j]
    return min(orb)
basin = {}
for i in range(64):
    basin.setdefault(attractor_id(i), set()).add(i)
depth = {}
for i in range(64):
    d = 0; j = i
    while j not in cyc:
        j = NN[j]; d += 1
    depth[i] = d
levels = {d: {i for i in range(64) if depth[i] == d} for d in (0, 1, 2)}
def invariant(Bset, ax):
    return all((IDX[y] in Bset) for x in Bset for y in S if R(ax, S[x], y))
for name, grp in [("basin of " + format(code, '06b'), B) for code, B in
                  [(sum(b << (5 - k) for k, b in enumerate(to_bits(S[a]))), B) for a, B in basin.items()]] + \
                 [("depth %d" % d, L) for d, L in levels.items()]:
    print("  %-22s size %2d; union of R_w/R_e/R_n classes:" % (name, len(grp)),
          [invariant(grp, ax) for ax in AX])

print("\n== 10. Definability: bisimulation classes (finite frame => definable sets = unions of classes) ==")
def succ_R(i): return [[IDX[y] for y in S if R(i, x, y)] for x in S]
def succ_X(i, s=1):
    out = []
    for x in S:
        y = list(x); y[i] = (y[i] + s) % 4
        out.append([IDX[tuple(y)]])
    return out
REL = {
    'R_w': succ_R(0), 'R_e': succ_R(1), 'R_n': succ_R(2),
    'X_w': succ_X(0), 'X_e': succ_X(1), 'X_n': succ_X(2),
    'Xi_w': succ_X(0, -1), 'Xi_e': succ_X(1, -1), 'Xi_n': succ_X(2, -1),
    'N': [[v] for v in NN],
}
SIG = {
    'S5 only (R_w,R_e,R_n)': ['R_w', 'R_e', 'R_n'],
    'S5 + X_w': ['R_w', 'R_e', 'R_n', 'X_w'],
    'S5 + X_w,X_e,X_n': ['R_w', 'R_e', 'R_n', 'X_w', 'X_e', 'X_n'],
    'S5 + X and inverses': ['R_w', 'R_e', 'R_n', 'X_w', 'X_e', 'X_n', 'Xi_w', 'Xi_e', 'Xi_n'],
    'N only': ['N'],
    'S5 + N': ['R_w', 'R_e', 'R_n', 'N'],
}
def vals(f):
    return [f(x) for x in S]
ATOMS = {
    'none': lambda x: (),
    '{w=0}': lambda x: (x[0] == 0,),
    '{w in {0,1}}': lambda x: (x[0] in (0, 1),),
    '{w in {0,2}}': lambda x: (x[0] in (0, 2),),
    '{w=0, e=0, n=0}': lambda x: (x[0] == 0, x[1] == 0, x[2] == 0),
    'family W (w=a, all a)': lambda x: (x[0],),
    'families W,E': lambda x: (x[0], x[1]),
    'all coordinate atoms': lambda x: x,
}
def classes(sig, atom):
    v = vals(ATOMS[atom])
    ids = {}
    cls = [ids.setdefault(t, len(ids)) for t in v]
    while True:
        sigs = []
        for x in range(64):
            s = [cls[x]]
            for r in sig:
                s.append(tuple(sorted({cls[y] for y in REL[r][x]})))
            sigs.append(tuple(s))
        ids2 = {}
        new = [ids2.setdefault(t, len(ids2)) for t in sigs]
        if len(ids2) == len(set(cls)):
            return len(ids2)
        cls = new
hdr = "%-26s" % "signature \\ atoms" + "".join("%-10s" % k[:9] for k in ATOMS)
print(hdr)
for sname, sig in SIG.items():
    print("%-26s" % sname + "".join("%-10d" % classes(sig, a) for a in ATOMS))
print("(number of bisimulation classes; maximum 64 = every context distinguishable)")

import itertools, math
from collections import Counter
import numpy as np

G = {0: (1, 0), 1: (1, 1), 2: (0, 1), 3: (0, 0)}   # Z4 -> bit pair (10,11,01,00)
Ginv = {v: k for k, v in G.items()}

def to_bits(x):
    b = []
    for c in x:
        b += list(G[c])
    return tuple(b)

def from_bits(b):
    return tuple(Ginv[(b[2*i], b[2*i+1])] for i in range(3))

def code6(b):
    return sum(bit << (5-i) for i, bit in enumerate(b))

def bits_of(i):
    return tuple((i >> (5-k)) & 1 for k in range(6))

S = list(itertools.product(range(4), repeat=3))

def lee(x, y):
    return sum(min((a-b) % 4, (b-a) % 4) for a, b in zip(x, y))

def ham(a, b):
    return sum(u != v for u, v in zip(a, b))

def analyze(f):
    n = len(f); st = [0]*n; cycnodes = set(); cyc = []
    for s in range(n):
        if st[s]:
            continue
        path = []; x = s
        while st[x] == 0:
            st[x] = 1; path.append(x); x = f[x]
        if st[x] == 1:
            i = path.index(x); cyc.append(len(path)-i); cycnodes.update(path[i:])
        for y in path:
            st[y] = 2
    depth = {c: 0 for c in cycnodes}
    for s in range(n):
        if s in depth:
            continue
        stack = []; x = s
        while x not in depth:
            stack.append(x); x = f[x]
        base = depth[x]
        for y in reversed(stack):
            base += 1; depth[y] = base
    return tuple(sorted(cyc)), max(depth.values()), len(set(f)), cycnodes, depth

def lcm_list(l):
    r = 1
    for v in l:
        r = r*v//math.gcd(r, v)
    return r

print("== 1. Gray / Lee ==")
print("gray cyclic adjacent:", all(ham(G[k], G[(k+1) % 4]) == 1 for k in range(4)))
print("code6 bijection:", sorted(code6(to_bits(x)) for x in S) == list(range(64)))
print("Lee == Hamming under Gray:", all(lee(x, y) == ham(to_bits(x), to_bits(y)) for x in S for y in S))

def flip(b, i):
    b = list(b); b[2*i] ^= 1; b[2*i+1] ^= 1; return tuple(b)

print("+2 on coord i == XOR 11 on block i:",
      all(to_bits(tuple((c+2) % 4 if j == i else c for j, c in enumerate(x))) == flip(to_bits(x), i)
          for x in S for i in range(3)))
# +1 on a coordinate: is it XOR with a constant?
diffs = set()
for x in S:
    y = (x[0], x[1], (x[2]+1) % 4)
    diffs.add(tuple(a ^ b for a, b in zip(to_bits(x), to_bits(y))))
print("+1 on coord 3 as XOR pattern: distinct patterns =", len(diffs), "(1 would mean XOR-translation)")

print("\n== 2. Translations ==")
ords = Counter()
for t in S:
    o = 1
    while tuple((o*c) % 4 for c in t) != (0, 0, 0):
        o += 1
    ords[o] += 1
print("order of translation vectors:", dict(ords))

print("\n== 3. Hexagram maps ==")
def N(b): return (b[1], b[2], b[3], b[2], b[3], b[4])
def comp(b): return tuple(1-x for x in b)
def rev(b): return b[::-1]
fN = [code6(N(bits_of(i))) for i in range(64)]
cyc, mp, im, cn, depth = analyze(fN)
print("nuclear: cycle lengths", cyc, "max preperiod", mp, "image size", im)
print("depth distribution:", dict(sorted(Counter(depth.values()).items())))
print("attractor nodes in coords (w,e,n):", sorted(from_bits(bits_of(i)) for i in cn))
print("attractor nodes as 6-bit codes:", sorted(format(i, '06b') for i in cn))
# basins
def cyc_id(x):
    while x not in cn:
        x = fN[x]
    orb = [x]; y = fN[x]
    while y != x:
        orb.append(y); y = fN[y]
    return min(orb)
basin = Counter(cyc_id(i) for i in range(64))
print("basin sizes by attractor (min node code):", {format(k, '06b'): v for k, v in sorted(basin.items())})
print("N commutes with complement:", all(code6(N(comp(bits_of(i)))) == code6(comp(N(bits_of(i)))) for i in range(64)))
print("N commutes with reverse:", all(code6(N(rev(bits_of(i)))) == code6(rev(N(bits_of(i)))) for i in range(64)))
print("complement == +(2,2,2):", all(to_bits(tuple((c+2) % 4 for c in from_bits(bits_of(i)))) == comp(bits_of(i)) for i in range(64)))
print("reverse == (w,e,n)->(2-n,2-e,2-w):",
      all(to_bits(tuple(((2-c) % 4) for c in reversed(from_bits(bits_of(i))))) == rev(bits_of(i)) for i in range(64)))
orbs = set()
for i in range(64):
    b = bits_of(i)
    orbs.add(frozenset([b, comp(b), rev(b), comp(rev(b))]))
print("orbits of <complement, reverse>:", len(orbs), Counter(len(o) for o in orbs))
print("reverse-fixed:", sum(1 for i in range(64) if rev(bits_of(i)) == bits_of(i)),
      " complement-reverse-fixed:", sum(1 for i in range(64) if comp(rev(bits_of(i))) == bits_of(i)))
ratio = max(ham(N(bits_of(a)), N(bits_of(b)))/ham(bits_of(a), bits_of(b)) for a in range(64) for b in range(64) if a != b)
print("max Hamming expansion ratio of N:", ratio)
def Nc(x):
    return from_bits(N(to_bits(x)))
hom = sum(1 for x in S for y in S if Nc(tuple((a+b) % 4 for a, b in zip(x, y))) == tuple((a+b) % 4 for a, b in zip(Nc(x), Nc(y))))
print("N additive on Z4^3 for", hom, "of 4096 pairs")

print("\n== 4. Isometries ==")
Lm = np.array([[lee(x, y) for y in S] for x in S])
sidx = {x: i for i, x in enumerate(S)}
mono = set()
for perm in itertools.permutations(range(3)):
    for eps in itertools.product([1, 3], repeat=3):
        for c in S:
            f = tuple(sidx[tuple((eps[i]*x[perm[i]]+c[i]) % 4 for i in range(3))] for x in S)
            mono.add(f)
print("monomial maps x_i -> e_i x_perm(i) + c_i: distinct =", len(mono))
ok = all((Lm[np.ix_(f, f)] == Lm).all() for f in mono)
print("all Lee isometries:", ok)
# block-preserving bit isometries
pairs = {frozenset([0, 1]), frozenset([2, 3]), frozenset([4, 5])}
blk = set()
for perm in itertools.permutations(range(6)):
    if {frozenset(perm[j] for j in p) for p in pairs} != pairs:
        continue
    for t in range(64):
        tb = bits_of(t)
        f = []
        for x in S:
            b = to_bits(x)
            nb = tuple(b[perm[j]] ^ tb[j] for j in range(6))
            f.append(sidx[from_bits(nb)])
        blk.add(tuple(f))
print("block-preserving Q6 isometries:", len(blk), "; equal to monomial set:", blk == mono)
print("pairings of 6 coordinates (index of subgroup in B6 = 46080/3072):", 46080 // 3072)
types = Counter()
maxord = 1
for f in mono:
    c, _, _, _, _ = analyze(list(f))
    types[c] += 1
    maxord = max(maxord, lcm_list(c))
print("monomial maps: distinct cycle types =", len(types), ", max order =", maxord)

print("\n== 5. Matrices over Z4 (3x3) ==")
pts = np.array(S, dtype=np.int16)
mats = np.array(list(itertools.product(range(4), repeat=9)), dtype=np.int16).reshape(-1, 3, 3)
bij_types = Counter(); pre = Counter(); nil = 0; bij = 0; maxperiodic = 1
ex_pre = None; ex_nil_pre = None
for s in range(0, len(mats), 8192):
    ch = mats[s:s+8192]
    img = np.einsum('nij,pj->nip', ch, pts) % 4
    f = (16*img[:, 0, :] + 4*img[:, 1, :] + img[:, 2, :]).astype(np.int64)
    for k in range(len(ch)):
        c, mpre, im, _, _ = analyze(f[k].tolist())
        pre[mpre] += 1
        if im == 64:
            bij += 1; bij_types[c] += 1
        if c == (1,):
            nil += 1
        maxperiodic = max(maxperiodic, lcm_list(c))
        if mpre == max(pre) and ex_pre is None or (ex_pre is not None and mpre > ex_pre[0]):
            ex_pre = (mpre, ch[k].tolist())
print("total matrices:", len(mats), " invertible (bijective):", bij, "(expected |GL3(Z4)| = 86016)")
print("distinct cycle types among invertible:", len(bij_types))
print("max order of invertible matrix (lcm of cycles):", max(lcm_list(c) for c in bij_types))
print("nilpotent (all points -> 0):", nil)
print("max preperiod over all matrices:", max(pre), "example:", ex_pre)
print("preperiod distribution:", dict(sorted(pre.items())))
print("max lcm of periodic cycle lengths over all matrices:", maxperiodic)
print("top cycle types among invertible:")
for c, v in bij_types.most_common(8):
    print("  ", Counter(c), v)

print("\n== 6. The 2x2 example M=[[1,1],[1,2]] mod 4 ==")
def mm(A, B):
    return [[sum(A[i][k]*B[k][j] for k in range(2)) % 4 for j in range(2)] for i in range(2)]
M = [[1, 1], [1, 2]]
M2 = mm(M, M); M3 = mm(M2, M)
print("det M mod 4 =", (1*2-1*1) % 4, " M^2 =", M2, " M^3 =", M3)
S2 = list(itertools.product(range(4), repeat=2))
f2 = [4*((M[0][0]*a+M[0][1]*b) % 4)+((M[1][0]*a+M[1][1]*b) % 4) for a, b in S2]
print("cycle type of M on Z4^2:", Counter(analyze(f2)[0]))

#!/usr/bin/env python3
# =====================================================================
#  SUBIT-ALT v0.3  --  verification of theorems ALT-8 and ALT-9
#  (release SUBIT-infinity v6.14.2)
#
#  ASCII-only output (safe under Windows cp1252).
#
#  ALT-8: structure of GL_3(Z4): order, kernel K, splitting, group H,
#         cycle types (17), conjugacy classes (60).
#  ALT-9: bisimulation partition of (S; R_w,R_e,R_n; N; atoms) is the
#         product partition P (36 classes); nu-orbits (also 36) are a
#         DIFFERENT partition; Aut(structure) is trivial.
#
#  Run:  python3 verify_alt8_alt9.py
# =====================================================================
import numpy as np, itertools, collections, random
from collections import Counter

checks = []
def check(name, cond, extra=""):
    checks.append(bool(cond))
    print(("[PASS] " if cond else "[FAIL] ") + name + (("   " + extra) if extra else ""))

def hr(t):
    print("\n" + "=" * 72)
    print(t)
    print("=" * 72)

# ---------------------------------------------------------------------
#  Z4 matrix machinery (exact integer determinant!)
# ---------------------------------------------------------------------
def decode(c):
    d = []
    for _ in range(9):
        d.append(c % 4); c //= 4
    return np.array(d[::-1], dtype=np.int64).reshape(3, 3)

def encode(M):
    c = 0
    for i in range(3):
        for j in range(3):
            c = c * 4 + int(M[i, j])
    return c

def det(M):
    return (M[0,0]*(M[1,1]*M[2,2]-M[1,2]*M[2,1])
            - M[0,1]*(M[1,0]*M[2,2]-M[1,2]*M[2,0])
            + M[0,2]*(M[1,0]*M[2,1]-M[1,1]*M[2,0]))

_DEC = {}
def D(c):
    if c not in _DEC:
        _DEC[c] = decode(c)
    return _DEC[c]

def mul(a, b):
    return encode((D(a) @ D(b)) % 4)

I = np.eye(3, dtype=np.int64)
ID = encode(I)

def mat_from_rows(rows):
    return encode(np.array(rows, dtype=np.int64))

# =====================================================================
#  ALT-8
# =====================================================================
hr("ALT-8 : structure of GL_3(Z4)")

# --- generators of GL_3(Z4) ---
gens = []
for i in range(3):
    for j in range(3):
        if i == j:
            continue
        E = I.copy(); E[i, j] = 1; gens.append(encode(E))
for i in range(3):
    Dg = I.copy(); Dg[i, i] = 3; gens.append(encode(Dg))
for p in itertools.permutations(range(3)):
    P = np.zeros((3, 3), dtype=np.int64)
    for r, cc in enumerate(p):
        P[r, cc] = 1
    gens.append(encode(P))
gens = sorted(set(gens))

# --- generate the group ---
Gset = {ID}; frontier = [ID]
while frontier:
    nf = []
    for x in frontier:
        for g in gens:
            y = mul(x, g)
            if y not in Gset:
                Gset.add(y); nf.append(y)
    frontier = nf
Gl = sorted(Gset)
nG = len(Gl)
print("generators          :", len(gens))
print("|GL_3(Z4)|          :", nG)
check("|GL_3(Z4)| = 86016 = 2^12*3*7", nG == 86016 and 2**12 * 3 * 7 == 86016)

# --- determinant of every element is odd ---
all_odd = all(det(D(c)) % 2 == 1 for c in Gl)
check("every element has odd determinant", all_odd)

# --- kernel K = {M == I mod 2} ---
K = [c for c in Gl if np.array_equal(D(c) % 2, np.eye(3, dtype=np.int64) % 2)]
Kset = set(K)
print("|K|                 :", len(K))
check("|K| = 512 = 2^9", len(K) == 512)
# K is elementary abelian (Z/2)^9
k_ab = all(mul(a, b) == mul(b, a) for a in K for b in K)
k_exp2 = all(mul(a, a) == ID for a in K)
check("K abelian", k_ab)
check("K exponent 2  => K = (Z/2)^9", k_exp2 and len(K) == 512)
# K normal (check g K g^-1 = K for generators)
def inv_code(c):
    M = D(c)
    adj = np.zeros((3, 3), dtype=np.int64)
    for i in range(3):
        for j in range(3):
            minor = np.delete(np.delete(M, j, 0), i, 1)
            adj[i, j] = ((-1) ** (i + j)) * (minor[0,0]*minor[1,1] - minor[0,1]*minor[1,0]) % 4
    d = det(M) % 4
    return encode((adj * {1: 1, 3: 3}[d]) % 4)
norm = True
for g in gens:
    gi = inv_code(g)
    for k in K:
        if mul(mul(g, k), gi) not in Kset:
            norm = False; break
    if not norm:
        break
check("K normal in GL_3(Z4)", norm)

# --- quotient GL_3(Z4)/K  has order 168 = |GL_3(F2)| ---
check("|G/K| = 168 = |GL_3(F2)|", nG // len(K) == 168 and 168 == 7 * 6 * 4)

# --- splitting: explicit complement C = <s,t> ---
s = mat_from_rows([[2, 0, 1], [2, 3, 2], [1, 0, 2]])
t = mat_from_rows([[2, 1, 3], [3, 3, 0], [2, 2, 3]])

def elt_order(c):
    x = c; o = 1
    while x != ID:
        x = mul(x, c); o += 1
        if o > 500:
            return -1
    return o

def subgroup_order(gs, cap=500000):
    Sset = {ID}; fr = [ID]
    while fr:
        nf = []
        for x in fr:
            for g in gs:
                y = mul(x, g)
                if y not in Sset:
                    Sset.add(y); nf.append(y)
                    if len(Sset) > cap:
                        return len(Sset)
        fr = nf
    return len(Sset)

st = mul(s, t)
p7 = ID
for _ in range(7):
    p7 = mul(p7, st)
print("order(s)            :", elt_order(s))
print("order(t)            :", elt_order(t))
print("(st)^7              :", "I" if p7 == ID else "not I")
check("s^2 = 1, t^3 = 1, (st)^7 = 1  (presentation of GL_3(F2)=PSL(2,7))",
      elt_order(s) == 2 and elt_order(t) == 3 and p7 == ID)
oC = subgroup_order([s, t])
print("|<s,t>|             :", oC)
check("|<s,t>| = 168", oC == 168)
# reduction mod 2 of <s,t> generates GL_3(F2) of order 168
sm2 = encode(D(s) % 2); tm2 = encode(D(t) % 2)
# C intersects K trivially
Sset = {ID}; fr = [ID]
while fr:
    nf = []
    for x in fr:
        for g in (s, t):
            y = mul(x, g)
            if y not in Sset:
                Sset.add(y); nf.append(y)
    fr = nf
check("complement C meets K trivially (C cap K = {I})", len(Sset & Kset) == 1)
# reduction of C to GL_3(F2): distinct mod-2 images of the 168 elements
img2 = {encode(D(c) % 2) for c in Sset}
check("reduction of complement is all of GL_3(F2)  =>  1 -> K -> G -> GL_3(F2) -> 1 SPLITS",
      len(img2) == 168)

# --- group H = preimage of S_3 (permutation matrices mod 2) ---
def is_perm_mod2(M):
    B = M % 2
    if B.sum() != 3:
        return False
    return all(B[i].sum() == 1 for i in range(3)) and all(B[:, j].sum() == 1 for j in range(3))

H = [c for c in Gl if is_perm_mod2(D(c))]
print("|H|                 :", len(H), "  index:", nG // len(H))
check("|H| = 3072 = 2^9*6, index 28", len(H) == 3072 and nG // len(H) == 28)
# H = monomial matrices: each row and column exactly one odd entry
mono = [c for c in Gl if all(sum(int(D(c)[i, j]) % 2 for j in range(3)) == 1 for i in range(3))
                       and all(sum(int(D(c)[i, j]) % 2 for i in range(3)) == 1 for j in range(3))]
check("H = {M : M mod 2 is a permutation matrix} = Z4-monomial matrices", set(H) == set(mono))
# complement of K in H given by the 0/1 permutation matrices
def is_perm01(M):
    B = M
    if B.sum() != 3 or any(int(B[i, j]) not in (0, 1) for i in range(3) for j in range(3)):
        return False
    return all(B[i].sum() == 1 for i in range(3)) and all(B[:, j].sum() == 1 for j in range(3))

perms01 = [c for c in Gl if is_perm01(D(c))]
check("permutation matrices (order 6) form a complement: H = K : S_3",
      len(perms01) == 6 and len({mul(k, p) for k in K for p in perms01}) == 3072)

# --- cycle types ---
def cycle_type(M):
    f = np.empty(64, dtype=np.int64)
    for w in range(4):
        for e in range(4):
            for n in range(4):
                v = M @ np.array([w, e, n]) % 4
                f[w*16 + e*4 + n] = int(v[0]*16 + v[1]*4 + v[2])
    seen = np.zeros(64, dtype=bool); ct = []
    for s0 in range(64):
        if seen[s0]:
            continue
        L = 0; x = s0
        while not seen[x]:
            seen[x] = True; x = int(f[x]); L += 1
        ct.append(L)
    return tuple(sorted(ct))

def mod2_order(M):
    B = M % 2; x = np.eye(3, dtype=np.int64); o = 1
    while True:
        x = (x @ B) % 2
        if np.array_equal(x, np.eye(3, dtype=np.int64)):
            return o
        o += 1

ctypes = Counter()
for c in Gl:
    ctypes[cycle_type(D(c))] += 1
print("distinct cycle types:", len(ctypes))
check("exactly 17 cycle types among the 86016 invertible matrices", len(ctypes) == 17)
print("   order | order mod 2 | cycle type (len^mult)         | count")
grouped = {}
for c in Gl:
    M = D(c)
    grouped.setdefault((elt_order(c), mod2_order(M)), Counter())[cycle_type(M)] += 1
for key in sorted(grouped):
    for ct, cnt in sorted(grouped[key].items(), key=lambda kv: -len(kv[0])):
        comp = Counter(ct)
        desc = ",".join("%d^%d" % (L, comp[L]) for L in sorted(comp))
        print("   %5d | %10d | %-28s | %d" % (key[0], key[1], desc, cnt))

# order counts
ord_counts = Counter(elt_order(c) for c in Gl)
print("element-order counts:", dict(sorted(ord_counts.items())))
check("|{order 7}| = 3072", ord_counts.get(7, 0) == 3072)
check("|{order 3}| = 3584", ord_counts.get(3, 0) == 3584)

# --- conjugacy classes ---
inv_gens = []
for g in gens:
    ig = inv_code(g)
    assert mul(g, ig) == ID
    inv_gens.append(ig)

gidx = {c: i for i, c in enumerate(Gl)}
parent = list(range(nG))
def find(a):
    while parent[a] != a:
        parent[a] = parent[parent[a]]; a = parent[a]
    return a
for c in Gl:
    ci = gidx[c]; Mc = D(c)
    for g, gi in zip(gens, inv_gens):
        y = encode((D(g) @ Mc @ D(gi)) % 4)
        ra, rb = find(ci), find(gidx[y])
        if ra != rb:
            parent[ra] = rb
classes = Counter(find(i) for i in range(nG))
hist = dict(sorted(Counter(classes.values()).items()))
print("conjugacy classes   :", len(classes))
print("class-size histogram:", hist)
check("exactly 60 conjugacy classes", len(classes) == 60)
check("class-size histogram = {1:2,21:2,24:2,28:2,42:2,56:2,84:2,336:4,672:6,1344:4,1536:16,2688:8,3584:8}",
      hist == {1: 2, 21: 2, 24: 2, 28: 2, 42: 2, 56: 2, 84: 2, 336: 4, 672: 6,
               1344: 4, 1536: 16, 2688: 8, 3584: 8})

# =====================================================================
#  ALT-9
# =====================================================================
hr("ALT-9 : bisimulation of S5 + N (nuclear hexagram)")

Gc = {0: (1, 0), 1: (1, 1), 2: (0, 1), 3: (0, 0)}
Gci = {v: k for k, v in Gc.items()}
S = [(w, e, n) for w in range(4) for e in range(4) for n in range(4)]
IDX = {x: i for i, x in enumerate(S)}

def to_bits(x):
    b = []
    for c in x:
        b += list(Gc[c])
    return tuple(b)

def from_bits(b):
    return tuple(Gci[(b[2*i], b[2*i+1])] for i in range(3))

def Nbits(b):
    return (b[1], b[2], b[3], b[2], b[3], b[4])

NN = np.array([IDX[from_bits(Nbits(to_bits(x)))] for x in S])

def refine_exact(f, use_axes=True):
    cls = [(x[0] == 0) * 1 + (x[1] == 0) * 2 + (x[2] == 0) * 4 for x in S]
    n_old = len(set(cls))
    depth = 0
    while True:
        sigs = []
        for x in range(64):
            w, e, n = S[x]
            s = [cls[x]]
            if use_axes:
                for (a, b, cc) in [(1, 0, 0), (0, 1, 0), (0, 0, 1)]:
                    neigh = sorted({cls[IDX[((w + a*k) % 4, (e + b*k) % 4, (n + cc*k) % 4)]] for k in range(4)})
                    s.append(tuple(neigh))
            s.append(cls[int(f[x])])
            sigs.append(tuple(s))
        ids = {}
        new = [ids.setdefault(t, len(ids)) for t in sigs]
        depth += 1
        if len(ids) == n_old:
            return new, len(ids), depth
        cls, n_old = new, len(ids)

cls_ax, n_ax, depth_ax = refine_exact(NN, True)
cls_no, n_no, _ = refine_exact(NN, False)
print("classes (S5 + N + atoms) :", n_ax, " (stabilized at depth %d)" % depth_ax)
print("classes (N + atoms)      :", n_no)
check("S5 + N + atoms has exactly 36 bisimulation classes", n_ax == 36)
check("N + atoms has 21 classes (spec §10 table)", n_no == 21)

# S5 + atoms only (no N): use identity map
cls_id, n_id, _ = refine_exact(np.arange(64), True)
print("classes (S5 + atoms only):", n_id)
check("S5 + atoms only has 8 classes (spec §10 table)", n_id == 8)

# --- product partition P ---
def bwu(w):
    return {0: 0, 1: 1, 2: 1, 3: 2}[w]

def bnn(n):
    return {0: 0, 1: 1, 2: 2, 3: 2}[n]

P = [(bwu(w), e, bnn(n)) for (w, e, n) in S]

def canon(a):
    m = {}
    return tuple(m.setdefault(v, len(m)) for v in a)

check("bisimulation partition == product partition P", canon(cls_ax) == canon(P))
check("#P = 3 (w-blocks) * 4 (e) * 3 (n-blocks) = 36", len(set(P)) == 36)
histP = Counter(Counter(P).values())
print("P class-size histogram   :", dict(sorted(histP.items())))
check("P size histogram = {1:16, 2:16, 4:4}", dict(histP) == {1: 16, 2: 16, 4: 4})

# --- P is stable (a bisimulation) ---
def ms(x, i):
    out = []
    for k in range(4):
        y = list(S[x]); y[i] = (y[i] + k) % 4
        out.append(P[IDX[tuple(y)]])
    return tuple(sorted(out))

stable = True
for i in range(3):
    groups = collections.defaultdict(set)
    for x in range(64):
        groups[P[x]].add(ms(x, i))
    if any(len(v) > 1 for v in groups.values()):
        stable = False
gN = collections.defaultdict(set)
for x in range(64):
    gN[P[x]].add(P[int(NN[x])])
if any(len(v) > 1 for v in gN.values()):
    stable = False
check("P is stable under R_w, R_e, R_n and N  (=> a bisimulation)", stable)

# --- nu-orbits ---
nu = np.array([IDX[tuple((-v) % 4 for v in x)] for x in S])
nucls = [0] * 64
seen = [False] * 64; cc = 0
for i in range(64):
    if not seen[i]:
        j = i
        while not seen[j]:
            seen[j] = True; nucls[j] = cc; j = int(nu[j])
        cc += 1
print("nu-orbits                :", cc)
check("nu-orbits = 36 (the upper bound of ALT 16.1)", cc == 36)
check("nu-orbit partition != bisimulation partition (36 = 36 is a coincidence)",
      canon(nucls) != canon(cls_ax))
viol = sum(1 for x in range(64) if nucls[int(NN[x])] != nucls[int(NN[int(nu[x])])])
print("nu-partition violations for N:", viol, "of 64")
check("nu is NOT an automorphism of N (violations > 0)", viol > 0)

# --- automorphism group of the full structure ---
perms = [p for p in itertools.permutations(range(4)) if p[0] == 0]
autos = []
for tw in perms:
    for te in perms:
        for tn in perms:
            g = np.empty(64, dtype=np.int64)
            for x in range(64):
                w, e, n = S[x]
                g[x] = IDX[(tw[w], te[e], tn[n])]
            if all(int(g[int(NN[x])]) == int(NN[int(g[x])]) for x in range(64)):
                autos.append(g)
print("|Aut(S; R_w,R_e,R_n; N; atoms)| :", len(autos))
check("Aut(structure) is trivial  => no automorphism-orbit explanation of 36", len(autos) == 1)

# =====================================================================
hr("SUMMARY")
ok = all(checks)
print("checks passed: %d / %d" % (sum(checks), len(checks)))
print("RESULT:", "ALL CHECKS PASSED" if ok else "SOME CHECKS FAILED")

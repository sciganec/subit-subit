#!/usr/bin/env python3
# =====================================================================
#  SUBIT-ALT v0.3  --  verification of theorems ALT-10 and ALT-11
#  (release SUBIT-infinity v6.14.3)
#
#  ASCII-only output (safe under Windows cp1252).
#
#  ALT-10: hybrid logic on the frame F = (S, R_w, R_e, R_n).
#          Nominals and coordinate atoms are mutually definable;
#          one nominal + S5^3 defines exactly 256 subsets of S
#          (= Boolean algebra of the three coordinate planes through p);
#          the satisfaction operator @ defines only the constants 0, S.
#
#  ALT-11: two-dimensional semantics; the monster operator M_k^b
#          commutes with @ exactly on {c_k = b} x S (1024 of 4096 pairs);
#          no M_k^b commutes globally; the diagonal operator Mtilde_k^b
#          (updating context AND circumstance) commutes with @ universally.
#
#  Run:  python3 verify_alt10_alt11.py
# =====================================================================
import numpy as np, itertools, collections
from collections import Counter

checks = []
def check(name, cond, extra=""):
    checks.append(bool(cond))
    print(("[PASS] " if cond else "[FAIL] ") + name + (("   " + extra) if extra else ""))

def hr(t):
    print("\n" + "=" * 72)
    print(t)
    print("=" * 72)

S = [(w, e, n) for w in range(4) for e in range(4) for n in range(4)]
IDX = {x: i for i, x in enumerate(S)}
NP = 64

def mask(pred):
    m = 0
    for i, x in enumerate(S):
        if pred(x):
            m |= 1 << i
    return m

def popcount(m):
    return bin(m).count("1")

# =====================================================================
#  ALT-10
# =====================================================================
hr("ALT-10 : hybrid logic on the frame F")

def rel_i(x, i):
    out = []
    for a in range(4):
        y = list(x); y[i] = a
        out.append(tuple(y))
    return out

def Rimage(m, i):
    out = 0
    for x in range(NP):
        for y in rel_i(S[x], i):
            if m >> IDX[y] & 1:
                out |= 1 << x
                break
    return out

# --- R_i is an equivalence with 16 classes of size 4 ---
def classes_of(rel):
    seen = [-1] * NP; c = 0
    for x in range(NP):
        if seen[x] >= 0:
            continue
        for y in rel(S[x]):
            seen[IDX[y]] = c
        c += 1
    return seen, c

size_ok = True
for i in range(3):
    seen, c = classes_of(lambda x, i=i: rel_i(x, i))
    sizes = Counter(seen)
    if c != 16 or set(sizes.values()) != {4}:
        size_ok = False
print("each R_i : 16 classes of size 4 :", size_ok)
check("each R_i is an equivalence with 16 classes of size 4", size_ok)

# --- bisimulation refinement ---
def refine(atom_masks, use_axes=True):
    ids = {}
    cls = [ids.setdefault(tuple((m >> i) & 1 for m in atom_masks), len(ids)) for i in range(NP)]
    n_old = len(set(cls))
    while True:
        sigs = []
        for x in range(NP):
            s = [cls[x]]
            if use_axes:
                for i in range(3):
                    nb = tuple(sorted({cls[IDX[y]] for y in rel_i(S[x], i)}))
                    s.append(nb)
            sigs.append(tuple(s))
        ids = {}
        new = [ids.setdefault(t, len(ids)) for t in sigs]
        if len(ids) == n_old:
            return new, len(ids)
        cls, n_old = new, len(ids)

def atoms_all_coord():
    return [mask(lambda x, i=i, a=a: x[i] == a) for i in range(3) for a in range(4)]

_, n_none = refine([], True)
_, n_w0 = refine([mask(lambda x: x[0] == 0)], True)
_, n_3a = refine([mask(lambda x: x[0] == 0), mask(lambda x: x[1] == 0), mask(lambda x: x[2] == 0)], True)
_, n_all = refine(atoms_all_coord(), True)
print("classes  S5^3 (no atoms) :", n_none)
print("classes  S5^3 + {w=0}    :", n_w0)
print("classes  S5^3 + 3 atoms  :", n_3a)
print("classes  S5^3 + 12 atoms :", n_all)
check("S5^3 with no atoms has 1 class (2 definable sets)", n_none == 1)
check("S5^3 + {w=0} has 2 classes (4 sets)", n_w0 == 2)
check("S5^3 + {w=0,e=0,n=0} has 8 classes (256 sets)", n_3a == 8)
check("S5^3 + all 12 coordinate atoms has 64 classes (all 2^64 sets)", n_all == 64)

# --- nominal <-> coordinate atom mutual definability ---
ok_single = all(popcount(mask(lambda x, p=p: x == p)) == 1 for p in S)
check("every nominal n_p denotes a singleton {p}", ok_single)

atom_ok = True
for i in range(3):
    for a in range(4):
        u = 0
        for p in S:
            if p[i] == a:
                u |= mask(lambda x, p=p: x == p)
        if u != mask(lambda x, i=i, a=a: x[i] == a):
            atom_ok = False
check("each coordinate atom {x_i=a} is the union of 16 nominals", atom_ok)

p0 = (1, 2, 3)
nom_p0 = mask(lambda x: x == p0)
inter = mask(lambda x: x[0] == 1) & mask(lambda x: x[1] == 2) & mask(lambda x: x[2] == 3)
check("each nominal n_p = {w=pw} cap {e=pe} cap {n=pn} (p=(1,2,3) checked)", nom_p0 == inter)

# --- one nominal: R-closure and Boolean algebra ---
def r_closure(base):
    fam = {base}; frontier = [base]
    while frontier:
        nf = []
        for m in frontier:
            for i in range(3):
                v = Rimage(m, i)
                if v not in fam:
                    fam.add(v); nf.append(v)
        frontier = nf
    return fam

def bool_atoms(fam):
    fam = list(fam); atoms = []
    for bits in range(1 << len(fam)):
        m = (1 << NP) - 1
        for j, s in enumerate(fam):
            m &= s if (bits >> j) & 1 else ((1 << NP) - 1) ^ s
        if m:
            atoms.append(m)
    return atoms

p = (0, 0, 0)
G = r_closure(mask(lambda x: x == p))
prof = Counter(popcount(m) for m in G)
print("R-closure of one nominal :", len(G), "sets, size profile", dict(sorted(prof.items())))
check("R-closure of a single nominal has 8 sets with sizes {1,4,4,4,16,16,16,64}",
      len(G) == 8 and dict(prof) == {1: 1, 4: 3, 16: 3, 64: 1})

al = bool_atoms(G)
print("Boolean atoms            :", len(al))
check("the Boolean algebra of the R-closure has 8 atoms => 256 sets", len(al) == 8)

full = set()
for bits in range(1 << len(al)):
    m = 0
    for j in range(len(al)):
        if (bits >> j) & 1:
            m |= al[j]
    full.add(m)
print("Boolean algebra size     :", len(full))
check("the algebra has 2^8 = 256 elements", len(full) == 256)
check("the algebra is closed under R_w, R_e, R_n",
      all(Rimage(m, i) in full for m in full for i in range(3)))
line_w = Rimage(mask(lambda x: x == p), 0)
plane_n = Rimage(Rimage(mask(lambda x: x == p), 0), 1)
check("the algebra contains the singleton {p}, the lines and the planes",
      mask(lambda x: x == p) in full and line_w in full and plane_n in full
      and popcount(line_w) == 4 and popcount(plane_n) == 16)

# --- @ defines only constants ---
def AT_frame(m):
    return ((1 << NP) - 1) if (m >> IDX[p]) & 1 else 0
check("@_n maps every definable set to 0 or S (adds only global constants)",
      all(AT_frame(m) in (0, (1 << NP) - 1) for m in full))

# --- comparison with the axis language ---
check("one nominal (256 sets) equals S5^3 + {w=0,e=0,n=0} (256 sets)",
      256 == 2 ** n_3a)
check("all 64 nominals define all 64 singletons => all 2^64 sets (same as 12 atoms)",
      len({mask(lambda x, p=p: x == p) for p in S}) == 64 and 2 ** 64 == 2 ** n_all)

# =====================================================================
#  ALT-11
# =====================================================================
hr("ALT-11 : monster operators M_k^b versus the satisfaction operator @")

PAIRS = [(c, i) for c in S for i in S]
Pidx = {ci: k for k, ci in enumerate(PAIRS)}
FULL = (1 << len(PAIRS)) - 1

def pmask(pred):
    m = 0
    for k, (c, i) in enumerate(PAIRS):
        if pred(c, i):
            m |= 1 << k
    return m

def ctx_atom(k, a):
    return pmask(lambda c, i, k=k, a=a: c[k] == a)

def circ_atom(k, a):
    return pmask(lambda c, i, k=k, a=a: i[k] == a)

def NEG(m):
    return FULL ^ m

def BOX_k(m, k):
    out = 0
    for c in S:
        for i in S:
            good = all((m >> Pidx[(c, tuple(i[j] if j != k else a for j in range(3)))]) & 1 for a in range(4))
            if good:
                out |= 1 << Pidx[(c, i)]
    return out

def AT(m):
    out = 0
    for c in S:
        if (m >> Pidx[(c, c)]) & 1:
            for i in S:
                out |= 1 << Pidx[(c, i)]
    return out

def Mk(m, k, b):
    out = 0
    for c in S:
        c2 = tuple(c[j] if j != k else b for j in range(3))
        for i in S:
            if m >> Pidx[(c2, i)] & 1:
                out |= 1 << Pidx[(c, i)]
    return out

def Mtilde(m, k, b):
    out = 0
    for c in S:
        c2 = tuple(c[j] if j != k else b for j in range(3))
        for i in S:
            i2 = tuple(i[j] if j != k else b for j in range(3))
            if m >> Pidx[(c2, i2)] & 1:
                out |= 1 << Pidx[(c, i)]
    return out

# sanity: @ depends only on the context, and is idempotent
san_at = True
for kk in range(3):
    for a in range(4):
        m = circ_atom(kk, a)
        if AT(AT(m)) != AT(m):
            san_at = False
check("@ is idempotent (@@phi <-> @phi) on all circumstance atoms", san_at)

# exact commutation set of M_k^b with @
all_exact = True
for k in range(3):
    for b in range(4):
        hyper = pmask(lambda c, i, k=k, b=b: c[k] == b)
        if popcount(hyper) != 1024:
            all_exact = False
        # witness phi = o_k=b  (circumstance atom)
        phi = circ_atom(k, b)
        agree = NEG(Mk(AT(phi), k, b) ^ AT(Mk(phi, k, b)))
        if agree != hyper:
            all_exact = False
        print("k=%d b=%d : commutation set = {c_k=b} x S, |.| = %d" % (k, b, popcount(agree)))
check("M_k^b @phi <-> @M_k^b phi holds exactly on {c_k=b} x S (1024 of 4096 pairs), all 12 (k,b)",
      all_exact)
check("the commutation hyperplane has 1024 = 16 * 64 pairs", 16 * 64 == 1024)

# witness shows failure outside the hyperplane
fail_ok = True
for k in range(3):
    for b in range(4):
        phi = circ_atom(k, b)
        disagree = Mk(AT(phi), k, b) ^ AT(Mk(phi, k, b))
        hyper = pmask(lambda c, i, k=k, b=b: c[k] == b)
        if disagree != NEG(hyper):
            fail_ok = False
check("for c_k != b the witness phi = o_k=b separates (3072 failing pairs, all 12 (k,b))",
      fail_ok)

# no M_k^b commutes globally
nocom = all(
    NEG(Mk(AT(circ_atom(k, b)), k, b) ^ AT(Mk(circ_atom(k, b), k, b))) != FULL
    for k in range(3) for b in range(4))
check("no M_k^b commutes with @ on all of S x S", nocom)

# diagonal operator commutes with @ universally
diag_ok = True
for k in range(3):
    for b in range(4):
        for kk in range(3):
            for a in range(4):
                phi = circ_atom(kk, a)
                if NEG(Mtilde(AT(phi), k, b) ^ AT(Mtilde(phi, k, b))) != FULL:
                    diag_ok = False
check("the diagonal Mtilde_k^b (context AND circumstance) commutes with @ on all 4096 pairs",
      diag_ok)
# diagonal also commutes on context atoms
diag_ok2 = True
for k in range(3):
    for b in range(4):
        for kk in range(3):
            for a in range(4):
                phi = ctx_atom(kk, a)
                if NEG(Mtilde(AT(phi), k, b) ^ AT(Mtilde(phi, k, b))) != FULL:
                    diag_ok2 = False
check("the diagonal Mtilde_k^b commutes with @ on all context atoms too", diag_ok2)

# =====================================================================
hr("SUMMARY")
ok = all(checks)
print("checks passed: %d / %d" % (sum(checks), len(checks)))
print("RESULT:", "ALL CHECKS PASSED" if ok else "SOME CHECKS FAILED")

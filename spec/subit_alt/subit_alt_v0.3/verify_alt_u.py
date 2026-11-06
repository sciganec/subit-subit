#!/usr/bin/env python3
"""verify_alt_u.py -- new results of the unified SUBIT-ALT specification.

Usage:  python3 verify_alt_u.py [U1 U2 U3 U4 U5 U6]     (no argument = all sections)
Needs numpy. Sections U2, U3, U6 sweep all 4**9 = 262144 matrices over Z4.
"""
import itertools
import math
import random
import sys
from collections import Counter

import numpy as np

SECTIONS = set(sys.argv[1:]) or {"U1", "U2", "U3", "U4", "U5", "U6"}

# ---------------------------------------------------------------- basics
S = list(itertools.product(range(4), repeat=3))        # state = (w, e, n), index 16w+4e+n
IDX = {x: i for i, x in enumerate(S)}
CO = np.array(S, dtype=np.int64)                        # (64, 3)
G = {0: (1, 0), 1: (1, 1), 2: (0, 1), 3: (0, 0)}        # Gray code of v0.1
Ginv = {v: k for k, v in G.items()}


def to_bits(x):
    b = []
    for c in x:
        b += list(G[c])
    return tuple(b)


def from_bits(b):
    return tuple(Ginv[(b[2 * i], b[2 * i + 1])] for i in range(3))


def code6(b):
    return sum(bit << (5 - i) for i, bit in enumerate(b))


def bits_of(c):
    return tuple((c >> (5 - k)) & 1 for k in range(6))


CODEOF = np.array([code6(to_bits(x)) for x in S])       # state index -> 6-bit code
STATEOF = np.zeros(64, dtype=np.int64)
STATEOF[CODEOF] = np.arange(64)


def Nbits(b):
    return (b[1], b[2], b[3], b[2], b[3], b[4])


NN = [IDX[from_bits(Nbits(to_bits(x)))] for x in S]     # nuclear map on state indices
NN_arr = np.array(NN)
NCODE = np.array([code6(Nbits(bits_of(c))) for c in range(64)])   # nuclear map on codes

SH = np.zeros((3, 4, 64), dtype=np.int64)               # SH[i][a][x] = index of x + a*e_i
for i in range(3):
    for a in range(4):
        for x in S:
            y = list(x)
            y[i] = (y[i] + a) % 4
            SH[i][a][IDX[x]] = IDX[tuple(y)]


def hr(title):
    print("\n== %s ==" % title, flush=True)


def lcm_list(l):
    r = 1
    for v in l:
        r = r * v // math.gcd(r, v)
    return r


def analyze(f):
    """cycle lengths (sorted), max preperiod of a function given as a list."""
    n = len(f)
    per = set()
    for x in range(n):
        y = x
        for _ in range(n):
            y = f[y]
        per.add(y)
    seen = set()
    cyc = []
    for x in sorted(per):
        if x in seen:
            continue
        L = 0
        y = x
        while True:
            seen.add(y)
            y = f[y]
            L += 1
            if y == x:
                break
        cyc.append(L)
    depth = {p: 0 for p in per}
    for x in range(n):
        path = []
        y = x
        while y not in depth:
            path.append(y)
            y = f[y]
        d = depth[y]
        for z in reversed(path):
            d += 1
            depth[z] = d
    return tuple(sorted(cyc)), max(depth.values())


def all_matrices():
    return np.array(list(itertools.product(range(4), repeat=9)), dtype=np.int64).reshape(-1, 3, 3)


def matrix_maps(mats):
    img = np.einsum('nij,pj->npi', mats, CO) % 4         # (B, 64, 3)
    return 16 * img[:, :, 0] + 4 * img[:, :, 1] + img[:, :, 2]


def batches(bs=4096):
    mats = all_matrices()
    for s in range(0, len(mats), bs):
        m = mats[s:s + bs]
        yield m, matrix_maps(m)


def bijective(F):
    return (np.sort(F, axis=1) == np.arange(64)[None, :]).all(1)


# ---------------------------------------------------------------- graphs and groups
def hamming_adj():
    return [[IDX[y] for y in S if sum(a != b for a, b in zip(x, y)) == 1] for x in S]


def lee_adj():
    adj = [[] for _ in S]
    for x in S:
        for i in range(3):
            for s in (1, 3):
                y = list(x)
                y[i] = (y[i] + s) % 4
                adj[IDX[x]].append(IDX[tuple(y)])
    return adj


def count_stab0(adj, color=None):
    """number of automorphisms of the graph fixing vertex 0 (optionally preserving edge colours)."""
    n = len(adj)
    adjm = [sum(1 << v for v in a) for a in adj]
    order = [0]
    seen = {0}
    for u in order:
        for v in adj[u]:
            if v not in seen:
                seen.add(v)
                order.append(v)
    assert len(order) == n
    pos = {v: i for i, v in enumerate(order)}
    parent = {v: min((u for u in adj[v] if pos[u] < pos[v]), key=lambda u: pos[u]) for v in order[1:]}
    img = [-1] * n
    img[0] = 0
    st = {'count': 0, 'amask': 1, 'imask': 1}

    def rec(k):
        if k == n:
            st['count'] += 1
            return
        v = order[k]
        nv = adjm[v] & st['amask']
        for c in adj[img[parent[v]]]:
            if (st['imask'] >> c) & 1:
                continue
            m = 0
            t = nv
            good = True
            while t:
                b = t & -t
                u = b.bit_length() - 1
                t ^= b
                m |= 1 << img[u]
                if color is not None and color[(u, v)] != color.get((img[u], c), -1):
                    good = False
                    break
            if not good or (adjm[c] & st['imask']) != m:
                continue
            img[v] = c
            st['amask'] |= 1 << v
            st['imask'] |= 1 << c
            rec(k + 1)
            st['amask'] ^= 1 << v
            st['imask'] ^= 1 << c
            img[v] = -1

    rec(1)
    return st['count']


_WREATH = None


def wreath_maps():
    """all 24^3 * 6 = 82944 maps x_i -> tau_i(x_i) placed at axis sigma(i); rows = images of the 64 states."""
    global _WREATH
    if _WREATH is None:
        P4 = np.array(list(itertools.permutations(range(4))))
        grid = np.array(list(itertools.product(range(24), repeat=3)))
        out = []
        for sig in itertools.permutations(range(3)):
            Y = np.zeros((len(grid), 64, 3), dtype=np.int64)
            for i in range(3):
                Y[:, :, sig[i]] = P4[grid[:, i]][:, CO[:, i]]
            out.append(16 * Y[:, :, 0] + 4 * Y[:, :, 1] + Y[:, :, 2])
        _WREATH = np.concatenate(out)
    return _WREATH


def hamming_edges():
    return [(IDX[x], IDX[y]) for x in S for y in S
            if IDX[x] < IDX[y] and sum(a != b for a, b in zip(x, y)) == 1]


def lee_edges():
    return [(IDX[x], IDX[y]) for x in S for y in S
            if IDX[x] < IDX[y] and sorted([((a - b) % 4) for a, b in zip(x, y)]) in ([0, 0, 1], [0, 0, 3])]


def wreath_flags(F):
    """booleans per row: automorphism of H(3,4), Lee isometry, Z4-affine."""
    he = np.array(hamming_edges())
    le = np.array(lee_edges())
    auto = np.zeros(len(F), bool)
    iso = np.zeros(len(F), bool)
    aff = np.zeros(len(F), bool)
    e = [IDX[(1, 0, 0)], IDX[(0, 1, 0)], IDX[(0, 0, 1)]]
    for s in range(0, len(F), 4096):
        f = F[s:s + 4096]
        Cx = CO[f[:, he[:, 0]]]
        Cy = CO[f[:, he[:, 1]]]
        auto[s:s + 4096] = ((Cx != Cy).sum(-1) == 1).all(1)
        Dx = (CO[f[:, le[:, 1]]] - CO[f[:, le[:, 0]]]) % 4
        nz = (Dx != 0).sum(-1)
        odd = ((Dx % 2 == 1).sum(-1) == 1)
        iso[s:s + 4096] = ((nz == 1) & odd).all(1)
        C0 = CO[f[:, 0]]
        V = (CO[f[:, e]] - C0[:, None, :]) % 4              # (b, 3, 3)
        pred = (C0[:, None, :] + np.einsum('xi,bik->bxk', CO, V)) % 4
        aff[s:s + 4096] = (pred == CO[f]).all((1, 2))
    return auto, iso, aff


# ================================================================ U1
if "U1" in SECTIONS:
    hr("U1. Groups: frame automorphisms, Lee isometries, Z4-affine maps")
    sh = count_stab0(hamming_adj())
    col = {}
    for x in S:
        for y in S:
            d = [i for i in range(3) if x[i] != y[i]]
            if len(d) == 1:
                col[(IDX[x], IDX[y])] = d[0]
    shc = count_stab0(hamming_adj(), col)
    sl = count_stab0(lee_adj())
    print("Hamming graph H(3,4): |Stab(0)| = %d  -> |Aut| = 64*%d = %d" % (sh, sh, 64 * sh))
    print("  edge-colour preserving (axes fixed): |Stab(0)| = %d -> %d" % (shc, 64 * shc))
    print("Lee graph (Cayley graph of Z4^3, +-e_i): |Stab(0)| = %d -> |Isom(S,d_L)| = %d" % (sl, 64 * sl))
    print("  (vertex-transitive via translations, so |Aut| = 64*|Stab(0)|)")
    W = wreath_maps()
    distinct = len(np.unique(W.astype(np.uint8), axis=0))
    auto, iso, aff = wreath_flags(W)
    print("explicit wreath maps S4 wr S3: %d rows, %d distinct" % (len(W), distinct))
    print("  all are automorphisms of H(3,4):", bool(auto.all()))
    print("  Lee isometries among them:", int(iso.sum()))
    print("  Z4-affine among them:", int(aff.sum()))
    print("  both:", int((iso & aff).sum()), "; sets equal:", bool((iso == aff).all()))
    ident = int((W == np.arange(64)[None, :]).all(1).sum())
    print("  identity occurs %d time(s)" % ident)

# ================================================================ U2
def morph_flags(F):
    """frame morphisms: every R_i-class is mapped inside one R_j-class (j may depend on class).
    p-morphism: ... onto an entire R_j-class."""
    B = F.shape[0]
    C0 = CO[F]
    is_m = np.ones(B, bool)
    is_p = np.ones(B, bool)
    for i in range(3):
        diff = np.zeros((B, 64, 3), bool)
        vals = []
        for a in range(4):
            Ca = CO[F[:, SH[i][a]]]
            diff |= (Ca != C0)
            vals.append(Ca)
        nd = diff.sum(-1)
        is_m &= (nd <= 1).all(1)
        one = (nd == 1).all(1)
        j = diff.argmax(-1)
        st = np.stack([np.take_along_axis(v, j[..., None], axis=2)[..., 0] for v in vals], axis=-1)
        s = np.sort(st, axis=-1)
        distinct = (s[..., 1:] != s[..., :-1]).all(-1).all(1)
        is_p &= one & distinct
    return is_m, is_p


if "U2" in SECTIONS:
    hr("U2. Linear maps that are frame morphisms")
    tot = nm = npm = nb_m = nb_p = 0
    profiles = Counter()
    morph_mats = []
    for mats, F in batches():
        im, ip = morph_flags(F)
        bj = bijective(F)
        tot += len(F)
        nm += int(im.sum())
        npm += int(ip.sum())
        nb_m += int((im & bj).sum())
        nb_p += int((ip & bj).sum())
        for k in np.nonzero(im)[0]:
            morph_mats.append(mats[k])
            c, pre = analyze(F[k].tolist())
            profiles[(c, pre)] += 1
    print("matrices:", tot)
    print("frame morphisms (each class into one line):", nm)
    print("  bijective among them:", nb_m)
    print("p-morphisms (each class onto a whole line):", npm, "; bijective among them:", nb_p)
    print("distinct orbit profiles (cycle type, max preperiod) among the %d morphisms: %d" % (nm, len(profiles)))
    print("max preperiod among morphisms:", max(p for (_, p) in profiles))
    cols = Counter()
    for m in morph_mats:
        cols[tuple(sorted(int((m[:, i] != 0).sum()) for i in range(3)))] += 1
    print("columns have <=1 nonzero entry in every morphism:", all(
        all(int((m[:, i] != 0).sum()) <= 1 for i in range(3)) for m in morph_mats))
    mons = []
    for k in range(3):
        d = np.eye(3, dtype=np.int64)
        d[k, k] = 0
        mons.append(d)
    keyset = {m.tobytes() for m in morph_mats}
    print("monster projections M_k^0 = diag with 0 at k belong to the morphism set:",
          all(m.tobytes() in keyset for m in mons))


# ================================================================ U3
def reach_flags(Fm, K):
    B = Fm.shape[0]
    rows = np.arange(B)[:, None]
    cols = np.arange(64)[None, :]
    dia = np.zeros((B, 64, 64), bool)
    diap = np.zeros_like(dia)
    rec = np.zeros_like(dia)
    P = np.tile(np.arange(64), (B, 1))
    for k in range(K + 1):
        oh = np.zeros((B, 64, 64), bool)
        oh[rows, cols, P] = True
        dia |= oh
        if k >= 1:
            diap |= oh
        if k >= 2:
            rec |= oh
        P = np.take_along_axis(Fm, P, axis=1)
    return (dia == diap).all((1, 2)), (diap == rec).all((1, 2)), (dia == rec).all((1, 2))


def predicted_flags(Fm):
    """bijective ; image inside the periodic set."""
    B = Fm.shape[0]
    P = np.tile(np.arange(64), (B, 1))
    for _ in range(64):
        P = np.take_along_axis(Fm, P, axis=1)
    per = np.zeros((B, 64), bool)
    per[np.arange(B)[:, None], P] = True
    img_in_per = np.take_along_axis(per, Fm, axis=1).all(1)
    return bijective(Fm), img_in_per


if "U3" in SECTIONS:
    hr("U3. Collapse of temporal modalities  (diamond, diamond+, rec)  vs  bijectivity")
    c1 = c2 = c3 = pb = pi1 = mis = tot = 0
    for mats, F in batches(4096):
        e1, e2, e3 = reach_flags(F, 40)
        bj, i1 = predicted_flags(F)
        tot += len(F)
        c1 += int(e1.sum()); c2 += int(e2.sum()); c3 += int(e3.sum())
        pb += int(bj.sum()); pi1 += int(i1.sum())
        mis += int((e1 != bj).sum() + (e3 != bj).sum() + (e2 != i1).sum())
    print("all %d matrices over Z4:" % tot)
    print("  diamond == diamond+  : %d   (bijective: %d)" % (c1, pb))
    print("  diamond+ == rec      : %d   (image inside periodic set: %d)" % (c2, pi1))
    print("  diamond == rec       : %d" % c3)
    print("  mismatches with the predicted conditions:", mis)
    # nuclear map and cyclic shift
    Fn = NN_arr[None, :]
    e1, e2, e3 = reach_flags(Fn, 40)
    bj, i1 = predicted_flags(Fn)
    print("N: (d==d+, d+==rec, d==rec) =", bool(e1[0]), bool(e2[0]), bool(e3[0]),
          "; bijective:", bool(bj[0]), "; image in periodic set:", bool(i1[0]))
    Xn = SH[2][1][None, :]
    e1, e2, e3 = reach_flags(Xn, 40)
    print("X_WHEN: (d==d+, d+==rec, d==rec) =", bool(e1[0]), bool(e2[0]), bool(e3[0]))
    # random functions of three kinds
    rnd = random.Random(7)
    rows = []
    kinds = []
    for _ in range(600):
        rows.append([rnd.randrange(64) for _ in range(64)]); kinds.append('uniform')
    for _ in range(300):
        p = list(range(64)); rnd.shuffle(p); rows.append(p); kinds.append('permutation')
    for _ in range(600):
        m = rnd.randrange(1, 64)
        pts = rnd.sample(range(64), m)
        sh = pts[:]
        rnd.shuffle(sh)
        f = [0] * 64
        for a, b in zip(pts, sh):
            f[a] = b
        for x in range(64):
            if x not in pts:
                f[x] = rnd.choice(pts)
        rows.append(f); kinds.append('depth<=1')
    R = np.array(rows)
    e1, e2, e3 = reach_flags(R, 140)
    bj, i1 = predicted_flags(R)
    print("random functions (%d): mismatches d==d+ vs bijective: %d ; d+==rec vs image-in-periodic: %d ; d==rec vs bijective: %d"
          % (len(R), int((e1 != bj).sum()), int((e2 != i1).sum()), int((e3 != bj).sum())))
    print("  kinds:", dict(Counter(kinds)), "; bijective:", int(bj.sum()), "; image-in-periodic:", int(i1.sum()))

# ================================================================ U4
if "U4" in SECTIONS:
    hr("U4. Gray map: Z4-affine versus F2-affine")
    # N in codes: F2-linear?
    def f2_affine_codes(g):
        """g: (B,64) maps on 6-bit codes -> boolean F2-affine."""
        base = g[:, 0]
        basis = [g[:, 1 << k] ^ base for k in range(6)]
        pred = np.tile(base[:, None], (1, 64))
        c = np.arange(64)
        for k in range(6):
            pred ^= ((c >> k) & 1)[None, :] * basis[k][:, None]
        return (pred == g).all(1)

    def state_map_to_code_map(F):
        return CODEOF[F[:, STATEOF]]

    gN = NCODE[None, :]
    print("N is F2-linear on 6-bit codes:", bool(f2_affine_codes(gN)[0]), "; N(000000) =", format(int(NCODE[0]), '06b'))
    L = (CO[NN_arr] - CO[NN_arr[0]]) % 4
    sumidx = np.zeros((64, 64), dtype=np.int64)
    for x in S:
        for y in S:
            sumidx[IDX[x], IDX[y]] = IDX[tuple((a + b) % 4 for a, b in zip(x, y))]
    ok = 0
    first = None
    for a in range(64):
        for b in range(64):
            if ((L[sumidx[a, b]] - L[a] - L[b]) % 4 == 0).all():
                ok += 1
            elif first is None:
                first = (a, b)
    print("N - N(0) additive on Z4^3 for %d of 4096 pairs -> N is Z4-affine: %s" % (ok, ok == 4096))
    if first:
        a, b = first
        print("  first violating pair: x=%s, y=%s ; N(x+y)-N(0)=%s vs (N(x)-N(0))+(N(y)-N(0))=%s ; N(0)=%s" % (
            S[a], S[b], tuple(int(v) for v in L[sumidx[a, b]]),
            tuple(int(v) for v in (L[a] + L[b]) % 4), S[NN[0]]))
    # identities behind the hand proof of the row criterion (standard Gray map phi_s: 0,1,2,3 -> 00,01,11,10)
    phi_s = {0: (0, 0), 1: (0, 1), 2: (1, 1), 3: (1, 0)}
    carry = all(tuple((phi_s[a][k] + phi_s[b][k] + (a * b) % 2) % 2 for k in range(2)) == phi_s[(a + b) % 4]
                for a in range(4) for b in range(4))
    parity_affine = all((phi_s[a][0] ^ phi_s[a][1]) == a % 2 for a in range(4))
    gamma_shift = all(tuple(phi_s[a][k] ^ (1 if k == 0 else 0) for k in range(2)) == G[a] for a in range(4))
    print("phi_s(a+b) = phi_s(a)+phi_s(b)+(ab mod 2)(1,1) for all 16 pairs:", carry,
          "; a mod 2 = h xor l:", parity_affine, "; gamma = phi_s xor (1,0):", gamma_shift)
    # translations
    Tr = np.array([[IDX[tuple((a + b) % 4 for a, b in zip(x, t))] for x in S] for t in S])
    print("all 64 translations are F2-affine under the Gray map:", bool(f2_affine_codes(state_map_to_code_map(Tr)).all()))
    # census over linear maps
    tot = aff = affb = 0
    ctypes_aff = Counter()
    row_mis = col_mis = row_cnt = col_cnt = 0
    for mats, F in batches():
        a = f2_affine_codes(state_map_to_code_map(F))
        bj = bijective(F)
        tot += len(F)
        aff += int(a.sum())
        affb += int((a & bj).sum())
        par = mats % 2
        row_ok = (par.sum(axis=2) <= 1).all(axis=1)      # every row has at most one odd entry
        col_ok = (par.sum(axis=1) <= 1).all(axis=1)      # every column has at most one odd entry
        row_mis += int((row_ok != a).sum())
        col_mis += int((col_ok != a).sum())
        row_cnt += int(row_ok.sum())
        col_cnt += int(col_ok.sum())
        for k in np.nonzero(a & bj)[0]:
            ctypes_aff[analyze(F[k].tolist())[0]] += 1
    print("criterion 'every ROW of M mod 2 has weight <= 1': satisfied by %d matrices, mismatches with F2-affine: %d" % (row_cnt, row_mis))
    print("criterion 'every COLUMN of M mod 2 has weight <= 1': satisfied by %d matrices, mismatches with F2-affine: %d" % (col_cnt, col_mis))
    print("Z4-linear maps x -> Mx: %d total; F2-affine under Gray: %d ; bijective and F2-affine: %d" % (tot, aff, affb))
    print("  => among all 16777216 Z4-affine maps, F2-affine ones: 64 * %d = %d" % (aff, 64 * aff))
    print("  distinct cycle types among bijective F2-affine linear maps:", len(ctypes_aff))

# ================================================================ U5
_Q6 = None


def q6_maps():
    global _Q6
    if _Q6 is None:
        codes = np.arange(64)
        bits = (codes[:, None] >> (5 - np.arange(6))[None, :]) & 1
        wts = 1 << (5 - np.arange(6))
        tb = (np.arange(64)[:, None] >> (5 - np.arange(6))[None, :]) & 1
        out = []
        for pi in itertools.permutations(range(6)):
            permuted = bits[:, list(pi)]
            nb = permuted[None, :, :] ^ tb[:, None, :]
            out.append((nb * wts).sum(-1))
        _Q6 = np.concatenate(out)
    return _Q6


def perm_order(g):
    cur = g.copy()
    idn = np.arange(len(g))
    k = 1
    while not (cur == idn).all():
        cur = g[cur]
        k += 1
    return k


def aut_count_functional_graph(f):
    n = len(f)
    per = set()
    for x in range(n):
        y = x
        for _ in range(n):
            y = f[y]
        per.add(y)
    children = {x: [] for x in range(n)}
    for x in range(n):
        if x not in per:
            children[f[x]].append(x)
    canon_memo, aut_memo = {}, {}

    def canon(v):
        if v not in canon_memo:
            canon_memo[v] = tuple(sorted(canon(c) for c in children[v]))
        return canon_memo[v]

    def aut(v):
        if v not in aut_memo:
            r = 1
            for c in children[v]:
                r *= aut(c)
            for _, m in Counter(canon(c) for c in children[v]).items():
                r *= math.factorial(m)
            aut_memo[v] = r
        return aut_memo[v]

    seen = set()
    comps = Counter()
    comp_aut = {}
    for x in sorted(per):
        if x in seen:
            continue
        cyc = [x]
        seen.add(x)
        y = f[x]
        while y != x:
            cyc.append(y)
            seen.add(y)
            y = f[y]
        types = [canon(v) for v in cyc]
        p = len(cyc)
        rots = sum(1 for r in range(p) if all(types[i] == types[(i + r) % p] for i in range(p)))
        a = rots
        for v in cyc:
            a *= aut(v)
        key = min(tuple(types[(i + r) % p] for i in range(p)) for r in range(p))
        comps[key] += 1
        comp_aut[key] = a
    total = 1
    for key, m in comps.items():
        total *= comp_aut[key] ** m * math.factorial(m)
    return total


if "U5" in SECTIONS:
    hr("U5. Symmetries commuting with the nuclear map N")
    # self-test of the functional-graph automorphism counter
    rnd = random.Random(3)
    okt = True
    for _ in range(60):
        n = rnd.randrange(1, 8)
        f = [rnd.randrange(n) for _ in range(n)]
        brute = sum(1 for s in itertools.permutations(range(n)) if all(s[f[x]] == f[s[x]] for x in range(n)))
        if brute != aut_count_functional_graph(f):
            okt = False
    for _ in range(25):
        n = 8
        f = [rnd.randrange(n) for _ in range(n)]
        brute = sum(1 for s in itertools.permutations(range(n)) if all(s[f[x]] == f[s[x]] for x in range(n)))
        if brute != aut_count_functional_graph(f):
            okt = False
    structured = [
        [0] * 8,                                   # star over a fixed point
        [1, 0, 0, 0, 1, 1, 1, 1],                  # 2-cycle with 3 and 4 leaves
        [1, 0, 1, 0, 0, 1, 0, 1],                  # 2-cycle, symmetric leaves
        [1, 2, 0, 0, 1, 2, 0, 1],                  # 3-cycle with unequal trees
        [0, 0, 1, 1, 2, 2, 3, 3],                  # binary tree on a fixed point
        [1, 0, 3, 2, 0, 1, 2, 3],                  # two 2-cycles, isomorphic components
    ]
    for f in structured:
        n = len(f)
        brute = sum(1 for s in itertools.permutations(range(n)) if all(s[f[x]] == f[s[x]] for x in range(n)))
        if brute != aut_count_functional_graph(f):
            okt = False
    print("self-test of Aut counter vs brute force (60 random n<=7, 25 random n=8, 6 structured n=8):", okt)
    Q = q6_maps()
    print("Aut(Q6) enumerated as bit-permutation + XOR: %d maps, %d distinct" % (len(Q), len(np.unique(Q.astype(np.uint8), axis=0))))
    comm = (Q[:, NCODE] == NCODE[Q]).all(1)
    idxs = np.nonzero(comm)[0]
    print("centralizer of N in Aut(Q6): order", len(idxs))
    pis = list(itertools.permutations(range(6)))
    orders = Counter(perm_order(Q[k]) for k in idxs)
    print("  element orders:", dict(sorted(orders.items())))
    for k in idxs[:64]:
        pi, t = pis[k // 64], k % 64
        print("   bit-permutation (new bit i = old bit pi[i], bits 1..6 = 0..5) pi=%s, xor t=%s" % (
            pi, format(t, '06b')))
    W = wreath_maps()
    auto, iso, aff = wreath_flags(W)
    cw = (W[:, NN_arr] == NN_arr[W]).all(1)
    print("centralizer of N in S4 wr S3 (frame automorphisms, 82944):", int(cw.sum()))
    mu = iso & aff
    print("centralizer of N in the monomial group (3072):", int((cw & mu).sum()))
    wr_orders = Counter(perm_order(W[k]) for k in np.nonzero(cw)[0])
    print("  element orders in the S4 wr S3 centralizer:", dict(sorted(wr_orders.items())))
    ANTI = SH[0][2][SH[1][2][SH[2][2][np.arange(64)]]]
    REV = np.array([IDX[((2 - x[2]) % 4, (2 - x[1]) % 4, (2 - x[0]) % 4)] for x in S])
    print("complement (+(2,2,2)) commutes with N:", bool((ANTI[NN_arr] == NN_arr[ANTI]).all()),
          "; reverse (w,e,n)->(2-n,2-e,2-w) commutes with N:", bool((REV[NN_arr] == NN_arr[REV]).all()))
    print("the 4 centralizer elements in Z4-coordinates are {id, anti, rev, anti o rev}:",
          sorted(map(tuple, W[cw][:, :].tolist())) == sorted(map(tuple, [list(range(64)), ANTI.tolist(), REV.tolist(), ANTI[REV].tolist()])))
    a = aut_count_functional_graph(NN)
    print("|Aut_Dyn(S, N)| = |{sigma in Sym(64): sigma N = N sigma}| =", a)
    print("   = %.4e ; log2 = %.2f" % (a, math.log2(a)))
    print("   (the geometric centralizers above are subgroups of this group)")

# ================================================================ U6
U64 = np.uint64


def mix(k):
    k = k ^ (k >> U64(33))
    k = k * U64(0xFF51AFD7ED558CCD)
    k = k ^ (k >> U64(33))
    return k


def refine(F, use_axes=True):
    """number of bisimulation classes for the signature (R_w,R_e,R_n if use_axes, M) with atoms {w=0},{e=0},{n=0}."""
    B = F.shape[0]
    L = np.tile((CO[:, 0] == 0) * 1 + (CO[:, 1] == 0) * 2 + (CO[:, 2] == 0) * 4, (B, 1)).astype(np.int64)
    prev = len(np.unique(L[0]))
    ncls = np.array([len(np.unique(r)) for r in L])
    NB = [SH[i].T for i in range(3)]
    with np.errstate(over='ignore'):
        for _ in range(70):
            lm = np.take_along_axis(L, F, axis=1)
            k = L.astype(U64)
            if use_axes:
                for i in range(3):
                    msk = np.bitwise_or.reduce(np.left_shift(U64(1), L[:, NB[i]].astype(U64)), axis=2)
                    k = mix(k * U64(0x9E3779B97F4A7C15) + msk)
            k = mix(k * U64(0xC2B2AE3D27D4EB4F) + lm.astype(U64))
            order = np.argsort(k, axis=1)
            sk = np.take_along_axis(k, order, axis=1)
            rk = np.concatenate([np.zeros((B, 1), dtype=np.int64), np.cumsum(sk[:, 1:] != sk[:, :-1], axis=1)], axis=1)
            Ln = np.empty_like(L)
            np.put_along_axis(Ln, order, rk, axis=1)
            new_n = rk[:, -1] + 1
            if (new_n == ncls).all():
                return new_n
            L, ncls = Ln, new_n
    raise RuntimeError("no fixpoint")


def refine_exact(f, use_axes=True):
    """pure-python partition refinement (cross-check)."""
    cls = [(x[0] == 0) * 1 + (x[1] == 0) * 2 + (x[2] == 0) * 4 for x in S]
    n_old = len(set(cls))
    while True:
        sigs = []
        for x in range(64):
            s = [cls[x]]
            if use_axes:
                for i in range(3):
                    s.append(tuple(sorted({cls[SH[i][a][x]] for a in range(4)})))
            s.append(cls[f[x]])
            sigs.append(tuple(s))
        ids = {}
        new = [ids.setdefault(t, len(ids)) for t in sigs]
        if len(ids) == n_old:
            return len(ids)
        cls, n_old = new, len(ids)


if "U6" in SECTIONS:
    hr("U6. Expressiveness census: bisimulation classes of (S, M) over all matrices, atoms {w=0},{e=0},{n=0}")
    hist_ax, hist_m = Counter(), Counter()
    hist_ax_b, hist_ax_nb = Counter(), Counter()
    hist_ax_morph = Counter()
    sample = []
    rnd = random.Random(5)
    for mats, F in batches(4096):
        c_ax = refine(F, True)
        c_m = refine(F, False)
        bj = bijective(F)
        im, _ = morph_flags(F)
        hist_ax.update(c_ax.tolist())
        hist_m.update(c_m.tolist())
        hist_ax_b.update(c_ax[bj].tolist())
        hist_ax_nb.update(c_ax[~bj].tolist())
        hist_ax_morph.update(c_ax[im].tolist())
        for k in rnd.sample(range(len(F)), 3):
            sample.append((F[k].tolist(), int(c_ax[k]), int(c_m[k])))
    ok = all(refine_exact(f, True) == a and refine_exact(f, False) == m for f, a, m in sample)
    print("cross-check of the vectorised refinement on %d sampled matrices against exact python:" % len(sample), ok)
    print("S5 axes + M: histogram {classes: matrices}:", dict(sorted(hist_ax.items())))
    print("  full (64 classes):", hist_ax.get(64, 0), "of", sum(hist_ax.values()))
    print("  bijective maps:", dict(sorted(hist_ax_b.items())))
    print("  non-bijective maps:", dict(sorted(hist_ax_nb.items())))
    print("  frame-morphism maps (U2):", dict(sorted(hist_ax_morph.items())))
    print("M alone (no axes): histogram {classes: matrices}:", dict(sorted(hist_m.items())))
    print("  full (64 classes):", hist_m.get(64, 0))
    print("S5 axes alone (no M) with the same atoms: 8 classes (v0.2, section 10)")
    neg = [IDX[tuple((-v) % 4 for v in x)] for x in S]
    orbits = len({min(i, neg[i]) for i in range(64)})
    fixed = sum(1 for i in range(64) if neg[i] == i)
    print("negation x -> -x: %d fixed points (the points with 2x = 0), %d orbits = (64 + %d)/2" % (fixed, orbits, fixed))
    print("maximum number of classes over all matrices:", max(hist_ax), "(S5+M);", max(hist_m), "(M alone); bound from negation orbits:", orbits)
    print("negation preserves every R_i, the three atoms, and commutes with every x -> Mx:",
          all(neg[SH[i][a][x]] == SH[i][(-a) % 4][neg[x]] for i in range(3) for a in range(4) for x in range(64))
          and all(CO[neg[x]][k] == 0 if CO[x][k] == 0 else CO[neg[x]][k] != 0 for x in range(64) for k in range(3)))

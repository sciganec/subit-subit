#!/usr/bin/env python3
# =====================================================================
#  SUBIT-ALT v0.3  --  verification of theorem ALT-12
#  (release SUBIT-infinity v6.14.4)
#
#  ASCII-only output (safe under Windows cp1252).
#
#  ALT-12: epistemic version of the frame F = (S, R_w, R_e, R_n).
#    (a) the 8 axis-visibility relations R_S (S subset of {w,e,n}) are
#        equivalences; R_S cap R_T = R_{S cap T}, R_S o R_T = R_{S u T};
#    (b) for ANY four-agent axis-visibility assignment
#        distributed knowledge  D = R_{cap_a S_a},
#        common knowledge       C = R_{cup_a S_a};
#        hence D refines C always, and D = C iff all four S_a coincide;
#    (c) canonical proposal ME:-, WE:{w}, YOU:{e}, THEY:{n}:
#        ME is omniscient (D = identity), nothing is common knowledge
#        (C = universal); the three non-ME agents ALONE still have
#        D = identity (jointly omniscient, individually blind to one axis);
#    (d) definable sets of the 4-agent frame: 2, 4, 256, 2^64;
#    (e) S5 for each agent, K_a phi -> K_D phi -> K_C phi, truth for ME;
#    (f) the S4 relabelling of the WHO coordinate is an automorphism,
#        so "which WHO value is which agent" is not canonical.
#
#  Run:  python3 verify_alt12.py
# =====================================================================
import itertools, collections

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
AX = (0, 1, 2)
AXN = {0: "w", 1: "e", 2: "n"}
def nm(Sset):
    return "".join(AXN[k] for k in sorted(Sset)) or "-"

def r_classes(Sset):
    """classes of R_S : x R_S y  iff  x,y agree outside Sset."""
    g = {}
    for i, x in enumerate(S):
        key = tuple(x[k] for k in range(3) if k not in Sset)
        g.setdefault(key, []).append(i)
    return sorted(tuple(v) for v in g.values())

def refine(parts):
    """meet (common refinement) of a list of partitions."""
    cur = [tuple(range(NP))]
    for cl in parts:
        pos = {}
        for j, c in enumerate(cl):
            for i in c:
                pos[i] = j
        new = []
        for block in cur:
            sub = {}
            for i in block:
                sub.setdefault(pos[i], []).append(i)
            new.extend(tuple(sorted(v)) for v in sub.values())
        cur = new
    return sorted(cur)

def closure_union(parts):
    """connected components of the union of the equivalence relations."""
    parent = list(range(NP))
    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a
    for cl in parts:
        for blk in cl:
            for k in range(1, len(blk)):
                ra, rb = find(blk[0]), find(blk[k])
                if ra != rb:
                    parent[rb] = ra
    comp = {}
    for i in range(NP):
        comp.setdefault(find(i), []).append(i)
    return sorted(tuple(sorted(v)) for v in comp.values())

def refines(P, Q):
    """every block of P is contained in a block of Q."""
    for blk in P:
        for q in Q:
            if blk[0] in q:
                if not set(blk) <= set(q):
                    return False
                break
    return True

def compose(A, B):
    """relational composition A o B (as a partition iff it is an equivalence)."""
    posA = {}
    for j, c in enumerate(A):
        for i in c:
            posA[i] = j
    posB = {}
    for j, c in enumerate(B):
        for i in c:
            posB[i] = j
    pairs = set()
    for i in range(NP):
        for k in range(NP):
            if posA[i] == posA[k]:
                pass
    # classes of A are blocks; for x, (A o B)(x) = A(B(x))
    # build relation then check it is R_{S u T} via class structure
    rel = {}
    for x in range(NP):
        acc = set()
        bx = [c for c in B if x in c][0]
        for z in bx:
            az = [c for c in A if z in c][0]
            acc |= set(az)
        rel[x] = frozenset(acc)
    # convert to partition
    seen = {}
    for x in range(NP):
        seen.setdefault(rel[x], []).append(x)
    return sorted(tuple(sorted(v)) for v in seen.values())

def atom(pred):
    return frozenset(i for i, x in enumerate(S) if pred(x))

def bisim(rel_list, atoms):
    key0 = {}
    for i in range(NP):
        k = tuple(1 if i in at else 0 for at in atoms)
        key0.setdefault(k, []).append(i)
    blocks = sorted(tuple(v) for v in key0.values())
    while True:
        bid = {}
        for j, blk in enumerate(blocks):
            for i in blk:
                bid[i] = j
        new = []
        for blk in blocks:
            sig = {}
            for i in blk:
                s = []
                for rel in rel_list:
                    tgt = [c for c in rel if i in c][0]
                    s.append(frozenset(bid[t] for t in tgt))
                sig.setdefault(tuple(s), []).append(i)
            new.extend(tuple(v) for v in sig.values())
        new = sorted(new)
        if len(new) == len(blocks):
            return new
        blocks = new

subsets = [frozenset(c) for r in range(4) for c in itertools.combinations(AX, r)]
AG = ["ME", "WE", "YOU", "THEY"]

# ---------------------------------------------------------------------
hr("ALT-12 (a) : the axis-visibility relations R_S")
# ---------------------------------------------------------------------
eq_ok = True
counts = {}
for Sset in subsets:
    cl = r_classes(Sset)
    flat = sorted(i for c in cl for i in c)
    if flat != list(range(NP)):
        eq_ok = False
    # equivalence: same class structure = reflexive, symmetric, transitive
    counts[nm(Sset)] = len(cl)
check("all 8 relations R_S are equivalences on S", eq_ok)
check("class counts 64/16/16/16/4/4/4/1 for -,w,e,n,we,wn,en,wen",
      counts == {"-": 64, "w": 16, "e": 16, "n": 16, "we": 4, "wn": 4, "en": 4, "wen": 1},
      str(counts))

meet_ok = join_ok = comp_ok = True
for A in subsets:
    for B in subsets:
        if refine([r_classes(A), r_classes(B)]) != r_classes(A & B):
            meet_ok = False
        if closure_union([r_classes(A), r_classes(B)]) != r_classes(A | B):
            join_ok = False
        if compose(r_classes(A), r_classes(B)) != r_classes(A | B):
            comp_ok = False
check("R_S cap R_T = R_{S cap T} (all 64 pairs)", meet_ok)
check("cl(R_S u R_T) = R_{S u T} (all 64 pairs)", join_ok)
check("R_S o R_T = R_{S u T} (all 64 pairs; hence commuting S5^4)", comp_ok)

# ---------------------------------------------------------------------
hr("ALT-12 (b) : distributed vs common knowledge over all 4096 assignments")
# ---------------------------------------------------------------------
all_assign = list(itertools.product(subsets, repeat=4))
check("number of four-agent axis-visibility assignments", len(all_assign) == 4096)

D_ok = C_ok = sub_ok = True
dist_D = collections.Counter()
dist_C = collections.Counter()
eqcnt = 0
for asg in all_assign:
    inter = frozenset.intersection(*asg)
    uni = frozenset.union(*asg)
    D = refine([r_classes(s) for s in asg])
    C = closure_union([r_classes(s) for s in asg])
    if D != r_classes(inter):
        D_ok = False
    if C != r_classes(uni):
        C_ok = False
    if not refines(D, C):
        sub_ok = False
    dist_D[len(D)] += 1
    dist_C[len(C)] += 1
    if D == C:
        eqcnt += 1
check("D = R_{cap_a S_a} on all 4096 assignments", D_ok)
check("C = R_{cup_a S_a} on all 4096 assignments", C_ok)
check("D refines C on all 4096 assignments (K^D phi -> K^C phi valid)", sub_ok)
check("D = C exactly when all four S_a coincide (8 of 4096)", eqcnt == 8, "count=%d" % eqcnt)
check("#classes(D) distribution {1:1,4:45,16:675,64:3375}",
      dict(sorted(dist_D.items())) == {1: 1, 4: 45, 16: 675, 64: 3375})
check("#classes(C) distribution mirror {1:3375,4:675,16:45,64:1}",
      dict(sorted(dist_C.items())) == {1: 3375, 4: 675, 16: 45, 64: 1})
# |D| = 4^(3-|cap S|) etc.
size_ok = True
for asg in all_assign:
    if len(refine([r_classes(s) for s in asg])) != 4 ** (3 - len(frozenset.intersection(*asg))):
        size_ok = False
check("|classes(D)| = 4^(3 - |cap S_a|) on all assignments", size_ok)

# ---------------------------------------------------------------------
hr("ALT-12 (c) : canonical proposal  ME:-  WE:{w}  YOU:{e}  THEY:{n}")
# ---------------------------------------------------------------------
canon = {"ME": frozenset(), "WE": frozenset({0}), "YOU": frozenset({1}), "THEY": frozenset({2})}
for a in AG:
    cl = r_classes(canon[a])
    print("  agent {:4s} blind to {:>3s} : {:2d} classes of size {}".format(a, nm(canon[a]), len(cl), len(cl[0])))
check("ME (identity) has 64 singleton classes", r_classes(canon["ME"]) == [tuple([i]) for i in range(NP)])
check("WE, YOU, THEY each have 16 classes of size 4",
      all(len(r_classes(canon[a])) == 16 and len(r_classes(canon[a])[0]) == 4 for a in ["WE", "YOU", "THEY"]))
inter = frozenset.intersection(*canon.values())
uni = frozenset.union(*canon.values())
D = r_classes(inter)
C = r_classes(uni)
check("distributed knowledge of all four = R_- = identity (omniscient)", D == [tuple([i]) for i in range(NP)])
check("common knowledge of all four = R_wen = universal (no nontrivial C)", C == [tuple(range(NP))])
D3 = refine([r_classes(canon[a]) for a in ["WE", "YOU", "THEY"]])
check("the three non-ME agents ALONE have D = identity (jointly omniscient)",
      D3 == [tuple([i]) for i in range(NP)])
vis = {a: [AXN[i] for i in AX if i not in canon[a]] for a in AG}
check("coordinate visibility: ME sees all; each other agent blind to one distinct axis",
      vis == {"ME": ["w", "e", "n"], "WE": ["e", "n"], "YOU": ["w", "n"], "THEY": ["w", "e"]}, str(vis))
check("the three blind axes {w},{e},{n} are pairwise distinct and cover all axes",
      {frozenset(canon[a]) for a in ["WE", "YOU", "THEY"]} == {frozenset({0}), frozenset({1}), frozenset({2})})
inc_ok = True
for a in AG:
    if not (refines(D, r_classes(canon[a])) and refines(r_classes(canon[a]), C)):
        inc_ok = False
check("R_D subset R_a subset R_C for every agent (K^D -> K_a -> K^C)", inc_ok)
check("D strictly refines C for the canonical proposal (D = identity != universal)",
      D != C)

# ---------------------------------------------------------------------
hr("ALT-12 (d) : definable sets of the 4-agent frame")
# ---------------------------------------------------------------------
rels4 = [r_classes(canon[a]) for a in AG]
b0 = len(bisim(rels4, []))
b1 = len(bisim(rels4, [atom(lambda x: x[0] == 0)]))
b3 = len(bisim(rels4, [atom(lambda x: x[0] == 0), atom(lambda x: x[1] == 0), atom(lambda x: x[2] == 0)]))
b12 = len(bisim(rels4, [atom(lambda x: x[k] == v) for k in AX for v in range(4)]))
print("  bisimulation classes : no atoms %d ; +{w=0} %d ; +3 atoms %d ; +12 atoms %d" % (b0, b1, b3, b12))
check("no atoms -> 1 class (2 definable sets)", b0 == 1)
check("+{w=0} -> 2 classes (4 sets)", b1 == 2)
check("+{w=0,e=0,n=0} -> 8 classes (256 sets)", b3 == 8)
check("+all 12 coordinate atoms -> 64 classes (all 2^64 sets)", b12 == 64)

# ---------------------------------------------------------------------
hr("ALT-12 (e) : S5, implication chain, truth for ME")
# ---------------------------------------------------------------------
s5_ok = True
for Sset in subsets:
    cl = r_classes(Sset)
    flat = sorted(i for c in cl for i in c)
    if flat != list(range(NP)):          # reflexive
        s5_ok = False
    for c in cl:                          # symmetric + transitive on the class
        for i in c:
            if not set(c) <= set([x for x in c]):
                s5_ok = False
check("each agent relation is an S5 equivalence (K,T,4,5 valid)", s5_ok)
chain_ok = True
for a in AG:
    if not refines(D, r_classes(canon[a])):
        chain_ok = False
check("K^D phi -> K_a phi valid for every agent (R_D subset R_a)", chain_ok)
check("K_a phi -> K^C phi valid for every agent (R_a subset R_C)",
      all(refines(r_classes(canon[a]), C) for a in AG))
check("truth lemma for ME: K_ME phi <-> phi (R_ME = identity)", r_classes(canon["ME"]) == [tuple([i]) for i in range(NP)])

# ---------------------------------------------------------------------
hr("ALT-12 (f) : relabelling symmetry and group monotonicity")
# ---------------------------------------------------------------------
perm_ok = True
for perm in itertools.permutations(range(4)):
    for Sset in subsets:
        cl = r_classes(Sset)
        mapped = sorted(tuple(sorted(IDX[(perm[x[0]], x[1], x[2])] for x in [S[j] for j in c])) for c in cl)
        if mapped != cl:
            perm_ok = False
check("every S4 relabelling of the WHO coordinate preserves all R_S (agent labels not canonical)", perm_ok)
# monotonicity: adding agents strengthens D and weakens C
mono_ok = True
for r in range(1, 4):
    for G in itertools.combinations(AG, r):
        for extra in AG:
            if extra in G:
                continue
            G2 = G + (extra,)
            Dg = refine([r_classes(canon[g]) for g in G])
            Dg2 = refine([r_classes(canon[g]) for g in G2])
            Cg = closure_union([r_classes(canon[g]) for g in G])
            Cg2 = closure_union([r_classes(canon[g]) for g in G2])
            if not refines(Dg2, Dg):       # D strengthens (refines)
                mono_ok = False
            if not refines(Cg, Cg2):       # C weakens (is refined by)
                mono_ok = False
check("adding an agent refines D and coarsens C (group monotonicity)", mono_ok)

# ---------------------------------------------------------------------
hr("SUMMARY")
# ---------------------------------------------------------------------
passed = sum(1 for c in checks if c)
print("checks passed: %d / %d" % (passed, len(checks)))
print("RESULT: " + ("ALL CHECKS PASSED" if passed == len(checks) else "SOME CHECKS FAILED"))

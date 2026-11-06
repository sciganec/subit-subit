# SUBIT-WARP v0.4 — W34.1.2 Reconciliation Audit

**Status:** SOURCE RECONCILIATION COMPLETED WITH REQUIRED CORRECTIONS  
**Date:** 5 November 2026  
**Repository:** sciganec/subit-subit  
**Base source commit:** e0d1254ca17fcaf30b5774523dc50ffe8c534471  
**Working branch:** work/w34-1-canonical-integration  
**Compared artifacts:** W23′ (draft_13), W30 (draft_20), W34.1 integration patch  
**Decision:** DO NOT update W23′ or W30 until the corrections below are incorporated into a revised patch.

---

## 1. Executive result

The patch is directionally compatible with the source architecture, but it is **not yet safe for canonical integration**. One mathematical statement is false as written, and several definitions need tighter scope.

### Blocking corrections

1. **W23′.5.1 / Ahlfors estimate:** the radius interval and the claimed closed-ball cylinder are inconsistent. The measure inequalities are also reversed.
2. **Tω / Tω⁺:** TC-01–TC-05 define FullTree and PartialTree coding classes, but do not by themselves define Tω. Tω is a further, non-local infinite-branch condition. The compactness proof must state this separately.
3. **W23′.3.2 / T-001:** the compactness result for the coded product classes must not be conflated with W30 T-001's specific FullTree_A result or the historically used Tree∞.
4. **Fingerprint conditions:** FP-03 must require integer-valued LCA depths; otherwise the level-set reconstruction is not properly typed.
5. **T-012:** W30's original T-012 only states boundedness and Hilbert–Schmidt thresholds. The patch's compactness and non-trace-class assertions are valid strengthening candidates, but require explicit spectral proof and must not be described as already present in W30.

### Reconciled without a blocking contradiction

- W23′.3.2's first-difference metric and W30 T-001 can be represented by total coding, provided each tree class is identified explicitly.
- W23′.5.2 and W30 T-007 agree on the domain Tω⁺ and the base estimate, but the metric-conversion result is an addition.
- W23′.9.1 uses diagonal value zero for the decreasing kernel; W30 T-008 states diagonal value one. Since the diagonal has μ_b×μ_b measure zero, these versions define the same integral operator on L². The specification should state this almost-everywhere equivalence rather than silently erase the textual difference.
- The finite matrix formula is valid for n=0 as well as n≥1 when q⁰=1 is explicit. The n=0 matrix is the 1×1 matrix [c_q].
- The q=1 finite compression is exact: T₁=P_const and P_n contains constants for every n≥0.
- The trace-norm identity ||T_q−P_const||₁=1 for 0≤q<1 is consistent with the complete spectrum, including the constant eigenspace contribution c_q−1.

---

## 2. Blocking correction A — Hausdorff balls and Ahlfors regularity

The patch currently states:

exp(−α_v(n+1)) < r ≤ exp(−α_v n)
⇒ B̄_v(ξ,r)=[ξ|n],

and then:

r^s ≤ μ_b(B̄_v(ξ,r)) < b r^s.

Both statements are incorrect under the declared metric
d_v(ξ,η)=exp(−α_v ℓ(ξ,η))
and the **closed-ball** convention d_v(ξ,η)≤r.

For a radius in the displayed interval, the closed ball is generally the cylinder of length n+1, not n. For example, when b=2, α_v=ln 2, n=0 and r=3/4, the closed ball excludes addresses with a different first symbol and is [ξ|1], not all of Σ_b.

### Correct formulation

For n≥0 and

exp(−α_v n) ≤ r < exp(−α_v(n−1)),

where the n=0 case can be handled separately (r≥1), the closed ball is

B̄_v(ξ,r)=[ξ|n].

For n≥1 this gives

μ_b(B̄_v(ξ,r))=b^(−n),

and with s=ln(b)/α_v,

b^(−n) ≤ r^s < b·b^(−n).

Equivalently,

r^s/b < μ_b(B̄_v(ξ,r)) ≤ r^s.

Thus the Ahlfors estimate holds with constants 1/b and 1 in this radius convention. At r=1, the ball is all of Σ_b and μ=1; the n=0 endpoint is consistent.

An alternative is to retain the original interval but change to an **open-ball** convention and re-derive the exact endpoint behavior. The canonical patch should choose one convention and use it consistently.

**Decision:** BLOCKER. Replace §2 of the patch before any canonical update. The dimension formula s=ln(b)/α_v remains correct; the displayed ball proof does not.

---

## 3. Blocking correction B — total coding, PartialTree, and Tω

W23′ explicitly distinguishes:
- FullTree_A^(b);
- PartialTree_A^(b), introduced as a new extension;
- FiniteTree;
- Tω, a class of partial trees satisfying an infinite-branch condition.

The patch's TC-01–TC-05 correctly describe local coding constraints for full and partial trees. However:

- TC-05 permits an INTERNAL node whose every child is ABSENT.
- Such a node is a valid PartialTree coding state under TC-05.
- It does **not** satisfy the Tω requirement that every present internal node has an infinite branch.

Therefore TC-01–TC-05 define the broad PartialTree coding class, not Tω. The statement “the subset satisfying TC-01–TC-05 is closed” proves compactness of that broad coded class, but it does not alone prove compactness or closedness of Tω.

### Required additional definition

For each present internal node u, require the existence of an infinite address ξ extending u such that every prefix along ξ after u is coded INTERNAL. Define Tω as the subset of admissible PartialTree codes satisfying this condition for every internal u.

This condition is closed in the product topology. For fixed u, the set of codes for which u is INTERNAL and has an infinite INTERNAL continuation can be written as an intersection over m of finite unions of cylinder conditions. The set where u is not INTERNAL is clopen. Their union is closed; intersecting over all u preserves closedness.

Since a valid root is either LEAF(a) or INTERNAL, and every INTERNAL root in Tω has an infinite continuation, one has:

Tω⁺ = Tω ∩ {t : t(ε)=INTERNAL}.

Consequently Tω⁺ is closed in the coded product space. This also makes explicit why the root-leaf case belongs to Tω vacuously but has empty boundary.

**Scope:** this proof concerns the total coding just defined. It does not retroactively identify every historical Tree∞ with this coded class.

**Decision:** BLOCKER for canonical wording; the mathematical repair is available and should be inserted as a separate Tω clause, not folded into TC-05.

---

## 4. Source mapping — W23′ and W30

### 4.1. W23′.3.2 and W30 T-001

W23′.3.2 states compactness of (Tree∞,d_F), while W30 T-001 specifically states compactness of FullTree_A. These are not automatically the same class.

The total coding proposal is useful, but the canonical text must distinguish:
- C_Full: root-present codes satisfying leaf closure and full branching;
- C_Partial: root-present codes satisfying absent closure and partial branching;
- C_ω: the subset of C_Partial satisfying the infinite-branch condition at every internal node;
- any historical Tree∞ class, pending an explicit equivalence/embedding theorem.

T-001 should retain its original identifier and claim for FullTree_A. Any compactness result for C_Partial or C_ω should be stated as an additional proposition, not silently substituted for T-001.

**Status:** CORRECTABLE; no theorem-number change needed.

### 4.2. W23′.5.2 and W30 T-007

Both source files use Tω⁺ as the domain of the Hausdorff boundary map and the base estimate

d_H,Σ(∂f,∂g) ≤ 2 d_F(f,g).

The patch's conversion for d_v=d_Σ^γ is a compatible strengthening:

d_H,v(∂f,∂g) = d_H,Σ(∂f,∂g)^γ
≤ 2^γ d_F(f,g)^γ.

For γ≥1 and d_F≤1 this implies a Lipschitz estimate with constant 2^γ. The equality between the induced Hausdorff metrics follows because the scalar map x↦x^γ is increasing and continuous and therefore commutes with the infimum and supremum operations in the Hausdorff construction.

**Status:** COMPATIBLE ADDITION. Keep the original T-007 statement and add a clearly labeled metric-corollary.

### 4.3. Decreasing kernel diagonal: W23′.9.1 versus W30 T-008

W23′ defines K_anc(ξ,ξ)=0. W30 T-008 states K_q(ξ,ξ)=1.

The diagonal in Σ_b×Σ_b has product measure zero under the nonatomic Bernoulli product measure. Hence the two kernels agree almost everywhere and induce the same L² integral operator. This does not make the textual definitions identical.

**Required editorial note:** preserve the canonical W23′ convention K_anc(ξ,ξ)=0 and annotate W30's value 1 as an a.e.-equivalent kernel representative. If a pointwise kernel API is later specified, it must select one convention explicitly.

**Status:** COMPATIBLE AFTER EXPLICIT A.E. NOTE.

### 4.4. W30 T-012 — increasing kernel

The existing W30 T-012 records:
- boundedness for α_w<ln b;
- Hilbert–Schmidt membership for α_w<(ln b)/2.

It does not state compactness iff t<b or non-trace-class for t>1. Those are new strengthening claims.

For t=exp(α_w)>1 and t<b, the same hierarchical decomposition gives:
- constant eigenvalue c_t=(b−1)/(b−t);
- level-j eigenvalue λ_j(t)=(t−1)t^(j−1)/[b^(j−1)(b−t)] >0;
- multiplicity m_j=(b−1)b^(j−1).

The eigenvalues tend to zero iff t<b, giving compactness in the bounded regime. The trace-norm contribution of level j is

m_j λ_j(t) = (b−1)(t−1)t^(j−1)/(b−t),

whose sum diverges for every t>1. Thus the bounded operator is not trace-class for any t>1. For t≥b, the row integral diverges and the operator is not bounded.

The Hilbert–Schmidt threshold remains t²<b, with squared Hilbert–Schmidt norm (b−1)/(b−t²).

**Status:** ANALYTICALLY DERIVABLE; NOT YET CANONICAL IN W30. Add proof and label as strengthening/corollary, not as original T-012 wording.

---

## 5. Finite approximation — n=0 and q=1

The patch currently lists n=0 as an open check. Source formulas are consistent when the convention q⁰=1 is applied.

For n=0:
- B_b^0={ε};
- H₀ is the one-dimensional constant space;
- the matrix is [c_q];
- its trace is c_q=q⁰c_q;
- its spectrum consists only of c_q;
- there are no W_j components for 1≤j≤0.

For q=1:
- c₁=1;
- λ_j(1)=0 under the endpoint convention;
- every matrix entry is b^(−n);
- the matrix is the rank-one projection onto constants;
- P_nP_constP_n=P_const for all n≥0.

**Decision:** RESOLVED. Replace the open check with an explicit n≥0 statement and retain q=1 as a separately declared endpoint operator.

---

## 6. Structural fingerprint — required typing and edge cases

W30 T-020 and T-021 are stated at a high level. The patch's primed formulations are useful but need one additional typing constraint.

### Required FP-03 correction

Require:

a(x,y) ∈ N₀ for all x,y∈L,

and for x≠y:

0 ≤ a(x,y) < min(h(x),h(y).

The existing symmetry, diagonal, and hierarchy conditions then define integer LCA depths suitable for the level-set construction.

### Reconstruction check

For each k=0,…,max h, define L_k={x:h(x)≥k} and x~_k y iff a(x,y)≥k. Under FP-01–FP-06:
- each ~_k is an equivalence relation on L_k;
- equivalence classes at level k are the vertices at depth k;
- inclusion between adjacent levels defines the unique parent relation;
- singleton classes at consecutive levels retain unary vertices;
- a single leaf at depth h reconstructs the unique unary chain of length h, including the root-leaf case h=0.

FP-07 should be phrased as a condition on the reconstructed finite tree or removed as redundant once the construction is defined. It cannot function as an independent input condition before internal vertices have been reconstructed.

For T-021′, prefix-free addresses and prefix closure reconstruct the occupied ordered trie. If absent child slots carry semantic information, they must be represented explicitly; the leaf-address set alone cannot encode a distinction between “absent” and “not recorded”.

**Status:** CORRECTABLE. Keep identifiers T-020/T-021 and label strengthened versions T-020′/T-021′.

---

## 7. Change map and disposition

| Patch section | Reconciliation result | Required action |
|---|---|---|
| §1 total coding | Partial compatibility | Separate C_Full, C_Partial, C_ω; preserve historical Tree∞ scope |
| §2 dimension / balls | BLOCKED | Correct radius interval, closed-ball cylinder and inequality |
| §3 boundary map | Compatible addition | Preserve Tω⁺ and add metric corollary |
| §4 decreasing kernel | Compatible | Preserve q endpoints, trace-norm distinction; annotate diagonal a.e. |
| §5 increasing kernel | New theorem strengthening | Add explicit eigenvalue proof and status |
| §6 finite approximation | Resolved | State n≥0 and q=1 endpoint explicitly |
| §7 fingerprint | Partial | Require integer a-values; refine FP-07 and absent-slot semantics |
| §8 theorem map | Compatible after edits | Preserve all W30 identifiers and original statements |
| §9 open checks | Update | Remove resolved n=0 check; retain remaining implementation gates |

### Current gate state

- Source retrieval: VERIFIED for W23′ and W30 files on the working branch.
- W23′/W30 statement mapping: COMPLETED for the sections reviewed above.
- Ahlfors ball estimate: BLOCKED pending correction.
- Tω coding and closedness: CORRECTABLE; additional definition required.
- Fingerprint: CORRECTABLE; integer-depth condition required.
- T-012 strengthening: ANALYTICALLY DERIVABLE; canonical proof insertion pending.
- W20 full regression: NOT EXECUTED / NOT VERIFIED.
- Lean: BLUEPRINT ONLY; NOT IMPLEMENTED.
- Rust: NOT AUDITED.
- v0.4 stable: NOT APPROVED.

**W34.1.2 decision:** RECONCILIATION AUDIT COMPLETED; PATCH REQUIRES REVISION. No canonical W23′ or W30 file has been modified by this audit.

**DO NOT COLLAPSE — CONTEXTUALIZE.**

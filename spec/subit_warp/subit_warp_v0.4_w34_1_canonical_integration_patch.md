# SUBIT-WARP v0.4 — W34.1 Canonical Integration Patch

**Status:** INTEGRATION PATCH PROPOSAL · NOT MERGED INTO CANONICAL SOURCES  
**Date:** 5 November 2026  
**Base commit:** `e0d1254ca17fcaf30b5774523dc50ffe8c534471`  
**Working branch:** `work/w34-1-canonical-integration`  
**Targets:** W23′ canonical specification; W30 theorem registry  
**Principle:** DO NOT COLLAPSE — CONTEXTUALIZE

---

## 0. Scope and change-control decision

This patch consolidates the mathematical corrections established in W33.2–W33.5. It is intentionally additive: it does not silently replace W23′ or W30, and it does not claim that those canonical files have already been modified.

The present patch is stored as a separate integration artifact so that the exact replacement of foundational definitions can be reviewed before changing the primary source. In particular, the total coding below must be read together with the distinction already present in W23′ between `FullTree`, `PartialTree`, and `FiniteTree`. It is not permission to identify these types.

No theorem status is upgraded to Lean-verified, numerically verified, or implementation-verified by this document.

---

# 1. W23′.3.2 — canonical total coding for the first-difference metric

### 1.1. Problem in the current definition

W23′.3.2 compares `f(u)` and `g(u)` over `Pos_b`, but the value of a tree below a leaf, or at an absent position of a partial tree, is not made fully explicit. The metric formula therefore needs a total representation before it can serve as the canonical definition across the declared tree classes.

### 1.2. Proposed replacement definition

Let the leaf-label alphabet be A and define the finite state alphabet

`S_A = {ABSENT, INTERNAL} ∪ {LEAF(a) : a ∈ A}`.

A coded tree is a total map

`t_f : Pos_b → S_A`.

Its admissibility conditions are:

- **TC-01 — Root:** `t_f(ε) ≠ ABSENT`.
- **TC-02 — Absent closure:** if `t_f(u)=ABSENT`, then `t_f(ui)=ABSENT` for every `i∈B_b`.
- **TC-03 — Leaf closure:** if `t_f(u)=LEAF(a)`, then `t_f(ui)=ABSENT` for every `i∈B_b`.
- **TC-04 — Full branching:** in the FullTree interpretation, if `t_f(u)=INTERNAL`, every child `ui` is a present tree state (INTERNAL or LEAF(a)).
- **TC-05 — Partial branching:** in the PartialTree interpretation, an INTERNAL node may have ABSENT children; its non-absent children are themselves admissible coded trees.

The FullTree and PartialTree classes remain distinct subspaces of the coded representation. FiniteTree remains a separate finite combinatorial type unless an explicit embedding into the coded space is supplied.

For two admissible coded trees f and g, define

`r_F(f,g) = min { |u| : t_f(u) ≠ t_g(u) }`

when the set is nonempty, and `r_F(f,f)=∞`. Then

`d_F(f,g)=2^(−r_F(f,g))`

with `2^(−∞)=0`.

### 1.3. Metric result

For any fixed admissible class using the same alphabet and coding convention, `d_F` is an ultrametric:

`d_F(f,h) ≤ max(d_F(f,g), d_F(g,h))`.

The proof is the standard first-difference argument: if f and g agree through all addresses of depth less than m, and g and h do likewise, then f and h agree through all addresses of depth less than the minimum of those two agreement depths.

### 1.4. Compactness result and scope

The full product `S_A^{Pos_b}` is compact because S_A is finite and Pos_b is countable. The subset satisfying TC-01–TC-05 is closed: each violation is witnessed by finitely many coordinates. Therefore each such fixed admissible coding class is compact in the product topology, equivalently in the first-difference ultrametric.

**Scope restriction:** this argument proves compactness for the explicitly defined coded classes. It does not, without a separate identification proof, establish that every historically named `Tree∞`, `Tω`, or other tree class in earlier drafts is exactly one of these classes.

**Canonical action:** replace the informal function-value clause in W23′.3.2 with §§1.2–1.4; preserve the historical note that the first-difference metric itself predates W23′.

---

# 2. W23′.5.1 — exact Hausdorff-dimension estimate

For the full homogeneous boundary `Σ_b=B_b^N`, equip the space with

`d_v(ξ,η)=exp(−α_v ℓ(ξ,η))`, `α_v>0`,

and the uniform Bernoulli measure `μ_b([σ])=b^(−n)` for every cylinder `[σ]` of length n.

Set

`s = ln(b)/α_v`.

For an integer n≥0 and

`exp(−α_v(n+1)) < r ≤ exp(−α_v n)`,

the closed ball is exactly the cylinder of length n:

`B̄_v(ξ,r)=[ξ|n]`.

Consequently,

`μ_b(B̄_v(ξ,r))=b^(−n)`

and

`r^s ≤ μ_b(B̄_v(ξ,r)) < b r^s`.

Thus μ_b is Ahlfors s-regular (with the displayed scale convention and constants 1 and b), and

`dim_H(Σ_b,d_v)=ln(b)/α_v`.

The upper bound follows from the b^n-cylinder cover. The lower bound follows from the mass-distribution principle applied to the displayed measure estimate.

**Scope restriction:** this result is for the full homogeneous b-ary boundary with uniform Bernoulli measure. It is not automatically a dimension formula for arbitrary partial or nonhomogeneous trees.

**Canonical action:** replace the current “proof strengthening required” paragraph in W23′.5.1 with this estimate and update the associated status only after the exact text is integrated.

---

# 3. W23′.5.2 — boundary-map domain and metric conversion

Retain the boundary-map theorem only on

`Tω⁺={f∈Tω : ∂f≠∅}`.

For the base address metric d_Σ, the established estimate is

`d_H,Σ(∂f,∂g) ≤ 2 d_F(f,g)`.

For `d_v=d_Σ^γ`, where `γ=α_v/ln 2`, the induced Hausdorff metrics satisfy

`d_H,v(∂f,∂g) = d_H,Σ(∂f,∂g)^γ`

and hence

`d_H,v(∂f,∂g) ≤ 2^γ d_F(f,g)^γ`.

Thus the estimate is Hölder for every γ>0; at γ=1 it is 2-Lipschitz. For γ>1, since d_F≤1, it also implies the Lipschitz estimate with constant 2^γ.

The theorem is not extended to empty boundaries by this patch. W23′.6's convention `d_H(∅,C)=2` defines a separate metric extension K₀; a boundary-map estimate on that extension would require its own proof.

**Canonical action:** retain Tω⁺ as the theorem domain and append the metric-conversion statement. Do not silently replace the nonempty compact hyperspace K with K₀.

---

# 4. W23′.11 / W30 — decreasing-kernel endpoints and trace distinctions

For the decreasing kernel, retain the spectral formulas for `0≤q<1`:

`c_q=(b−1)/(b−q)`

`λ_j(q)=−(1−q)q^(j−1)/[b^(j−1)(b−q)]`, `j≥1`

with multiplicity `(b−1)b^(j−1)`.

The operator norms and trace quantities are:

`||T_q||=c_q`

`||T_q||²_HS=(b−1)/(b−q²)`

`||T_q||₁=2c_q`

`Tr(T_q)=0`.

Endpoint conventions remain explicit:

- `q=0`: `c₀=(b−1)/b`, `λ₁(0)=−1/b`, and `λ_j(0)=0` for j≥2.
- `q=1`: by the separately declared endpoint definition, `T₁=P_const`, so `||T₁||=||T₁||₁=Tr(T₁)=1`.
- For all `q∈[0,1]`, `q⁰:=1`; for k≥1, `0^k=0`.

Do not infer trace-norm convergence to P_const from operator-norm convergence. For q<1:

`||T_q−P_const||₁=1`,

while

`lim(q→1−)||T_q||₁=2 ≠ 1=||P_const||₁`.

For fixed q<1, however, the finite-rank compressions `P_nT_qP_n` converge to T_q in trace norm because T_q is trace-class and P_n→I strongly.

These are two different limiting procedures and must remain explicitly distinguished.

---

# 5. W23′.12 / W30 T-012 — increasing-kernel thresholds

Set `t=exp(α_w)>1` and use the declared off-diagonal kernel `K_+(ξ,η)=t^{ℓ(ξ,η)}`, with diagonal value separately fixed as zero.

The operator thresholds are:

- bounded if and only if `t<b` (equivalently `α_w<ln b`);
- compact if and only if `t<b`;
- Hilbert–Schmidt if and only if `t²<b` (equivalently `α_w<(ln b)/2`);
- not trace-class for any `t>1`.

When `t²<b`:

`||T_+||²_HS=(b−1)/(b−t²)`.

When `t<b`:

`||T_+||=(b−1)/(b−t)`.

Keep boundedness, compactness, Hilbert–Schmidt membership, and trace-class membership as four distinct properties. The endpoint `t=1` is the separately defined constant-kernel projection case and is not included in the claim “not trace-class for t>1”.

---

# 6. W23′.14 / W30 T-013–T-018 — finite approximation

Let H_n be the functions constant on length-n cylinders, P_n the orthogonal projection onto H_n, and

`T_q^(n)=P_nT_qP_n|H_n`.

In the orthonormal cylinder basis `e_σ=b^(n/2)1_[σ]`, for `σ,τ∈B_b^n`:

- if σ≠τ: `(T_q^(n))_(σ,τ)=b^(−n)q^{ℓ(σ,τ)}`;
- if σ=τ: `(T_q^(n))_(σ,σ)=b^(−n)q^n c_q`.

The finite spectrum consists of c_q on W₀ and λ_j(q) on W_j for 1≤j≤n, with multiplicities `(b−1)b^(j−1)`.

The finite trace is

`Tr(T_q^(n))=q^n c_q`.

For fixed q<1, P_n→I strongly and T_q is trace-class; therefore

`||P_nT_qP_n−T_q||₁→0`.

This fixed-q approximation result must not be confused with q→1− convergence to P_const, which fails in trace norm.

For q=1, the endpoint operator is P_const and is already contained in H_n for every n≥0 (with the usual constant subspace), so its compression is exact.

**Canonical action:** retain the existing T-013–T-018 numbering; append the trace-norm convergence statement to the finite-approximation section and make the two limiting parameters explicit.

---

# 7. W30 T-020/T-021 — structural fingerprint admissibility

## 7.1. T-020′: unordered reconstruction

For a finite nonempty rooted tree fingerprint `F(T)=(L,h,a)`, require:

- **FP-01:** `h(x)∈N₀`.
- **FP-02:** `a(x,y)=a(y,x)`.
- **FP-03:** for x≠y, `0≤a(x,y)<min(h(x),h(y))`.
- **FP-04:** `a(x,x)=h(x)`.
- **FP-05:** `a(x,z)≥min(a(x,y),a(y,z))`.
- **FP-06:** L is finite and nonempty.
- **FP-07:** every internal vertex lies on a root-to-leaf path; unary vertices are retained.

For each k define

`L_k={x∈L : h(x)≥k}`

and

`x~_k y ⇔ a(x,y)≥k`.

The equivalence classes at each level represent vertices at that depth; parent relations are induced by inclusion of classes across adjacent levels. Unary vertices must not be suppressed.

**T-020′:** under FP-01–FP-07 and the declared unit-edge/depth convention, `(L,h,a)` determines the finite rooted tree up to root-preserving unordered isomorphism.

## 7.2. T-021′: ordered reconstruction

Add leaf addresses

`p:L→B_b^{<ω}`.

Require:

- p injective;
- the set of leaf addresses is prefix-free;
- `|p(x)|=h(x)`;
- `a(x,y)=ℓ(p(x),p(y))` for distinct leaves;
- all address symbols belong to B_b;
- the address set is compatible with the declared b-ary branching convention.

The prefix closure of the leaf addresses reconstructs the ordered tree, with child order given by B_b.

**T-021′:** under these address-consistency conditions, `(L,h,a,p)` determines the ordered finite SUBIT tree.

**Important compatibility condition:** if the class of trees permits missing child positions or non-full branching, the admissibility conditions must state whether absent positions are represented explicitly. Prefix closure alone reconstructs the occupied trie; it does not by itself prove that unoccupied child slots are semantically absent rather than omitted from the data.

**Canonical action:** keep the original identifiers T-020 and T-021 for traceability; add the primed statements as strengthened formulations. Do not claim Lean verification.

---

# 8. Theorem registry change map

| W30 item | Required action |
|---|---|
| T-001 / tree-space compactness | State explicitly which coded tree class is compact; do not infer class identity |
| T-004 / address ultrametric | No renumbering; align notation with W23′.3 |
| T-005 / Hausdorff dimension | Insert exact cylinder-ball estimate and homogeneous-measure scope |
| T-006 / boundary existence or domain result | Preserve its original statement; check dependency on Tω versus Tω⁺ |
| T-007 / boundary Lipschitz | State Tω⁺ domain and metric conversion for d_v |
| T-009 / decreasing-kernel spectrum | Preserve q endpoints and q⁰ convention |
| T-011 / operator norms and trace | Keep trace-class and endpoint distinctions |
| T-012 / increasing kernel | Add compactness iff t<b and non-trace-class for t>1 |
| T-013–T-018 / finite approximation | Add fixed-q trace-norm convergence and separate it from q→1 endpoint |
| T-020 / unordered fingerprint | Add FP-01–FP-07 and label T-020′ |
| T-021 / ordered fingerprint | Add address consistency and label T-021′ |

This map is a proposed registry edit. Exact theorem numbering and original statement text must be preserved during the final file-level merge.

---

# 9. Open integration checks

The following checks must be completed before calling W34.1 merged:

1. Verify the exact W30 wording and dependencies for T-001, T-004, T-005, T-006, T-007, T-009, T-011, T-012, and T-020–T-021.
2. Confirm that the compactness theorem for the coded product class is not being substituted for a stronger or historically different claim about Tree∞.
3. Confirm the exact definition of Tω and the proof that Tω⁺ is closed under the chosen coding.
4. Confirm that W23′.5.1's ball convention uses closed balls and the stated half-open radius interval.
5. Check the finite matrix diagonal convention at n=0 separately; the displayed matrix formula is intended for n≥1 unless the n=0 case is explicitly defined.
6. Check the endpoint q=1 in every finite-dimensional formula rather than substituting q=1 into expressions derived for q<1.
7. Confirm whether W30 T-012's “operator” includes the same diagonal convention and integral-operator domain as W23′.12.
8. Validate FP-01–FP-07 against all finite-tree edge cases, especially a single leaf at depth zero, unary chains, and unequal leaf depths.
9. Do not mark W20 full regression, Rust audit, or Lean implementation as complete on the basis of this patch.

---

# 10. W34.1 status

**PATCH ARTIFACT:** CREATED ON WORKING BRANCH.  
**CANONICAL W23′ FILE:** NOT YET REPLACED.  
**CANONICAL W30 FILE:** NOT YET REPLACED.  
**MATHEMATICAL REVIEW:** CONSOLIDATION PROPOSED; OPEN CHECKS REMAIN.  
**W20 FULL REGRESSION:** NOT CONFIRMED.  
**LEAN:** BLUEPRINT ONLY; NOT IMPLEMENTED.  
**RUST:** NOT AUDITED.  
**v0.4 STABLE:** NOT APPROVED.

The next required operation is a line-by-line reconciliation of the proposed insertions with the complete W23′ and W30 sources, followed by a separate reviewed commit that updates those canonical files. Until then, this artifact is an integration patch, not the canonical specification itself.

**DO NOT COLLAPSE — CONTEXTUALIZE.**

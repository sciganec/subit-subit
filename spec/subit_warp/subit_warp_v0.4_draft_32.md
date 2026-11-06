# SUBIT-WARP v0.4 — W34.1.3 Corrected Integration Patch

**Status:** CORRECTED INTEGRATION PROPOSAL · NOT MERGED INTO CANONICAL SOURCES  
**Date:** 5 November 2026  
**Review base:** `b6b9139415d491dba6103075e52e8ba5694334b5`  
**Source baseline:** W23′ (`draft_13_canonical`), W30 (`draft_20`), W34.1 (`draft_30`), W34.1.2 (`draft_31`)  
**Working branch:** `work/w34-1-canonical-integration`  
**Principle:** DO NOT COLLAPSE — CONTEXTUALIZE

---

## 0. Change-control decision

This document replaces the proposed mathematical content of W34.1 §1–§9 for review. It does **not** edit W23′ or W30. The canonical files remain unchanged until this patch has passed a separate source-level review.

The review of commit `b6b9139415d491dba6103075e52e8ba5694334b5` confirms that the repository contains:
- W23′ as `subit_warp_v0.4_draft_13_canonical.md`;
- W30 as `subit_warp_v0.4_draft_20.md`;
- W31 Lean blueprint as `subit_warp_v0.4_draft_21.md`;
- W34.1 proposal as `subit_warp_v0.4_draft_30.md`;
- W34.1.2 reconciliation audit as `subit_warp_v0.4_draft_31.md`.

The README still identifies W23′ as the current canonical mathematical source and v0.4 as DRAFT · NOT STABLE. W34.1 and W34.1.2 are review artifacts, not canonical replacements.

---

## 1. Canonical total coding and tree-class scope

Let (A) be the finite leaf-label alphabet, (B_b={1,ldots,b}), (bge2), and (Pos_b=B_b^{<omega}).

Define the finite state alphabet
`S_A = {ABSENT, INTERNAL} ∪ {LEAF(a) : a∈A}`.

A total code is a map `t:Pos_b→S_A`. The following local conditions define the broad coded classes:

- **TC-01 Root:** `t(ε) ≠ ABSENT`.
- **TC-02 Absent closure:** if `t(u)=ABSENT`, then `t(ui)=ABSENT` for every `i∈B_b`.
- **TC-03 Leaf closure:** if `t(u)=LEAF(a)`, then `t(ui)=ABSENT` for every `i∈B_b`.
- **TC-04 Full branching:** for `C_Full`, every child of an INTERNAL node is present (INTERNAL or LEAF).
- **TC-05 Partial branching:** for `C_Partial`, an INTERNAL node may have ABSENT children; every non-ABSENT child obeys TC-01–TC-03 relative to its subtree.

These conditions do **not** define `Tω`. Define it separately:

**TC-06 Infinite continuation:** a code belongs to `C_ω` iff it belongs to `C_Partial` and, for every address `u` with `t(u)=INTERNAL`, there exists an infinite address `ξ` extending `u` such that every node on the continuation from `u` is INTERNAL.

Set `Tω := C_ω` for this coded extension only, and
`Tω⁺ := {t∈Tω : ∂t≠∅}`.

For this coding, `Tω⁺ = {t∈Tω : t(ε)=INTERNAL}`. A root leaf belongs to `Tω` vacuously and has empty boundary; an INTERNAL root in `Tω` has an infinite continuation and therefore nonempty boundary.

**Closedness argument.** The ambient state space `S_A^{Pos_b}` is compact by Tychonoff because both factors are finite discrete spaces and `Pos_b` is countable. TC-01–TC-05 are closed local constraints. For fixed `u`, the condition “`t(u)=INTERNAL` and there exists an infinite INTERNAL continuation from `u`” is
`{t:t(u)=ABSENT or LEAF} ∪ ⋂_{m≥1} ⋃_{v∈B_b^m} [the finite path u…uv is INTERNAL]`.
Each finite union is clopen; the intersection is closed; the first set is clopen. Their union is closed. Intersecting this condition over all `u∈Pos_b` proves `C_ω` closed. Hence `C_Full`, `C_Partial`, `C_ω`, and `Tω⁺` are compact in the stated product coding.

**Scope restriction.** This compactness result concerns the explicitly coded classes above. It does not identify the historical `Tree∞` of v0.3/W23′ with any of them. W30 T-001 retains its original claim for `FullTree_A^(b)`; compactness of the new partial classes is an additional result, not a replacement of T-001.

For any one fixed coded class, define
`r_F(f,g)=min{|u|:t_f(u)≠t_g(u)}`, with `r_F(f,f)=∞`, and
`d_F(f,g)=2^(−r_F(f,g))`.
The first-difference argument proves the ultrametric inequality. This definition is a total-coded extension of W23′.3.2; it must not silently change the historical domain of that section.

---

## 2. Correct Hausdorff-ball estimate and Ahlfors regularity

Let `Σ_b=B_b^N`, let `ℓ(ξ,η)` be the common-prefix length, and define
`d_v(ξ,η)=exp(−α_v ℓ(ξ,η))` for distinct addresses, with zero on the diagonal. Let `μ_b` be the uniform Bernoulli measure and `s=ln(b)/α_v).

For a word `σ` of length `n`, the cylinder `[σ]` has
`μ_b([σ])=b^(−n)`.

Use **closed balls** throughout. For `n≥1` and
`exp(−α_v n) ≤ r < exp(−α_v(n−1))`,
`B̄_v(ξ,r)=[ξ|n]`.

Indeed, `d_v(ξ,η)≤r` iff `ℓ(ξ,η)≥n` on this radius interval. Therefore
`μ_b(B̄_v(ξ,r))=b^(−n)`.
Since `s=ln(b)/α_v`,
`b^(−n) ≤ r^s < b·b^(−n)`,
hence
`r^s/b < μ_b(B̄_v(ξ,r)) ≤ r^s`.

For `r≥1`, the closed ball is all of `Σ_b`; radii above the diameter may be omitted if the definition of Ahlfors regularity restricts to small radii. The Hausdorff dimension remains
`dim_H(Σ_b,d_v)=ln(b)/α_v`.

This replaces the incorrect interval/cylinder/inequality combination identified in W34.1.2. No open-ball convention is used in this patch.

---

## 3. Boundary map and metric conversion

Retain the W23′/W30 domain `Tω⁺` and the original base estimate:
`d_H,Σ(∂f,∂g) ≤ 2 d_F(f,g)`.

Since `d_v=d_Σ^γ`, where `γ=α_v/ln2`, the induced Hausdorff metrics satisfy
`d_H,v(A,B)=d_H,Σ(A,B)^γ`
for nonempty compact `A,B`. Consequently,
`d_H,v(∂f,∂g) ≤ 2^γ d_F(f,g)^γ`.

Thus the map is Hölder with exponent `γ`; for `γ≥1`, because `d_F≤1`, it is also Lipschitz with constant `2^γ`. This is a corollary to T-007, not a replacement of its original statement.

---

## 4. Decreasing kernel: diagonal and endpoints

Preserve W23′'s pointwise convention `K_q(ξ,ξ)=0`. W30 T-008 uses diagonal value 1. Under the nonatomic product measure `μ_b×μ_b`, the diagonal has measure zero, so the two representatives define the same integral operator on `L²(Σ_b,μ_b)`; they are not pointwise identical kernels. Any future pointwise API must select one convention.

For `0≤q<1`, retain:
`c_q=(b−1)/(b−q)`,
`λ_j(q)=−(1−q)q^(j−1)/[b^(j−1)(b−q)]`,
`m_j=(b−1)b^(j−1)`,
`||T_q||=c_q`,
`||T_q||²_HS=(b−1)/(b−q²)`,
`||T_q||₁=2c_q`,
`Tr(T_q)=0`.
Set `q^0=1` for all `q∈[0,1]`.

Endpoints remain separate:
- `q=0`: `c₀=(b−1)/b`, `λ₁=−1/b`, and `λ_j=0` for `j≥2`.
- `q=1`: define `T₁=P_const`; then `||T₁||=||T₁||₁=Tr(T₁)=1`.

Do not infer trace-norm convergence as `q→1−`. In particular,
`||T_q−P_const||₁=1` for every `0≤q<1`, even though `T_q` converges to `P_const` in operator norm.

---

## 5. Increasing kernel: T-012 strengthening

Let `t=exp(α_w)>1`. For `t<b`, the increasing-kernel operator has constant eigenvalue
`c_t=(b−1)/(b−t)`
and level-`j` eigenvalue
`λ_j(t)=(t−1)t^(j−1)/[b^(j−1)(b−t)]`
with multiplicity `m_j=(b−1)b^(j−1)`.

The eigenvalues tend to zero iff `t<b`; in the bounded regime this proves compactness. The Hilbert–Schmidt condition is `t²<b`, with
`||T_+||²_HS=(b−1)/(b−t²)`.

For every `1<t<b`,
`m_j λ_j(t)=(b−1)(t−1)t^(j−1)/(b−t)`,
so the sum of absolute eigenvalues diverges. Thus the bounded operator is not trace-class for any `t>1`.

For `t≥b`, the row integral against the constant function diverges, so the integral operator is not bounded on the stated `L²` domain.

**Registry treatment:** preserve original W30 T-012 wording (boundedness and Hilbert–Schmidt thresholds). Add compactness and non-trace-class as a separately labeled strengthening/corollary with the spectral calculation above. Do not imply these statements were already part of T-012.

---

## 6. Finite approximations: n=0 and q=1

State the finite-level formulas for all `n≥0`, with `B_b^0={ε}` and `q^0=1). At `n=0`, the compression matrix is the one-by-one matrix `[c_q]`; its trace is `c_q`, and no detail spaces `W_j` with `1≤j≤n` occur.

At `q=1`, define the endpoint operator separately as `P_const`. Every finite compression is the rank-one projection onto constants; its matrix entries in the normalized cylinder basis are `b^(−n)`. For every `n≥0`, `P_nP_constP_n=P_const`.

Keep fixed-`q<1` convergence in trace norm distinct from the `q→1−` endpoint limit. The identity `||T_q−P_const||₁=1` for `q<1` rules out trace-norm convergence in that parameter limit.

---

## 7. Structural fingerprints: typing and reconstruction conditions

For a finite nonempty leaf set `L), define depth `h:L→N₀` and LCA depth `a:L×L→N₀`. Require:

- **FP-01:** `h(x)∈N₀`.
- **FP-02:** `a(x,y)=a(y,x)`.
- **FP-03:** `a(x,y)∈N₀`; `a(x,x)=h(x)`; for `x≠y`, `0≤a(x,y)<min(h(x),h(y))`.
- **FP-04:** `a(x,z)≥min(a(x,y),a(y,z))`.
- **FP-05:** `L` is finite and nonempty.
- **FP-06:** the declared root/depth convention is fixed (root depth 0; unit edges unless otherwise stated).
- **FP-07:** after reconstruction, every internal vertex lies on a root-to-leaf path; unary vertices are retained. This is a postcondition of the reconstruction, not an input condition on vertices not yet constructed.

For `k=0,…,max h`, define `L_k={x∈L:h(x)≥k}` and `x~_k y ⇔ a(x,y)≥k`. The hierarchy condition makes each `~_k` an equivalence relation on `L_k). Equivalence classes encode vertices at depth `k`; inclusion across adjacent levels defines parent relations. Equal singleton classes at successive levels preserve unary chains. A single leaf at depth zero reconstructs the root leaf; a single leaf at depth `h>0` reconstructs a unary chain of length `h`.

**Branching constraint:** if the target is a b-ary tree, the reconstructed number of children at each internal vertex must be ≤b (or exactly b for a full tree). This admissibility condition must be explicit in T-020′.

For ordered reconstruction, retain T-021′ with an injective, prefix-free address map `p:L→B_b^{<ω}`, `|p(x)|=h(x)`, and `a(x,y)=ℓ(p(x),p(y))` for distinct leaves. Prefix closure reconstructs the occupied ordered trie. If absent child slots have semantic meaning, include an explicit occupancy/absence mask; the leaf-address set alone does not encode absent-versus-unrecorded positions.

Keep theorem identifiers T-020/T-021 and mark these as strengthened formulations T-020′/T-021′.

---

## 8. Canonical source edit map (proposed, not applied)

| Source | Proposed edit | Constraint |
|---|---|---|
| W23′.1 / W23′.3.2 | Add total coding appendix and class-specific metric domains | Do not identify historical Tree∞ with new C_ω |
| W23′.5.1 | Replace ball interval and proof with §2 above | Closed-ball convention only |
| W23′.5.2 | Add metric-conversion corollary | Preserve original Tω⁺ estimate |
| W23′.9 / W23′.10 | Add a.e. diagonal note and T-012 strengthening | Preserve pointwise W23′ diagonal value |
| W30 T-001 | Preserve FullTree_A compactness statement | Add separate compactness proposition for C_Partial/C_ω |
| W30 T-005 | Insert exact cylinder-ball estimate | Keep homogeneous Bernoulli scope |
| W30 T-007 | Add metric corollary | Preserve original theorem number and claim |
| W30 T-008 | Add a.e. diagonal-representative note | Do not silently change kernel convention |
| W30 T-012 | Add proved strengthening after original criterion | Preserve original wording |
| W30 T-020/T-021 | Add primed admissibility/reconstruction statements | Preserve identifiers and traceability |

No canonical source file is modified by this proposal.

---

## 9. Verification and release gates

- Source tree at review commit: **INSPECTED**.
- W23′ / W30 source mapping: **RECONCILED FOR THE SECTIONS LISTED ABOVE**.
- Corrected closed-ball estimate: **ANALYTICALLY DERIVED**.
- C_Full / C_Partial / C_ω compactness: **ANALYTICALLY DERIVED FOR THE EXPLICIT CODING ONLY**.
- Boundary metric conversion: **ANALYTICALLY DERIVED; T-007 BASE CLAIM RETAINED**.
- Increasing-kernel strengthening: **ANALYTICALLY DERIVED; REGISTRY INSERTION PENDING**.
- Fingerprint edge conditions: **SPECIFIED; FULL INDEPENDENT RECONSTRUCTION PROOF STILL REQUIRED**.
- W20 full regression: **NOT EXECUTED / NOT VERIFIED**.
- Lean: **W31 BLUEPRINT ONLY; NOT IMPLEMENTED**.
- Rust: **NOT AUDITED**.
- v0.4 STABLE: **NOT APPROVED**.

### Mandatory next review before canonical edits

1. Independently verify the fingerprint reconstruction theorem for unequal leaf depths, unary chains, b-ary branching, and the single-leaf cases.
2. Reconcile the exact W23′.5.1 and W30 T-005 text, including radius endpoint conventions.
3. Reconcile the exact W23′.9/W30 T-008 diagonal wording and the operator-domain assumptions for T-012.
4. Only then prepare a separate file-level canonical patch for W23′ and W30. No silent replacement or theorem renumbering is permitted.

**W34.1.3 status:** CORRECTED PATCH PROPOSAL PREPARED; CANONICAL INTEGRATION NOT YET PERFORMED.

**DO NOT COLLAPSE — CONTEXTUALIZE.**

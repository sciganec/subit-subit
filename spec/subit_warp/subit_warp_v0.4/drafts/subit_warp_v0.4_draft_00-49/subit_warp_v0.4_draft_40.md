# SUBIT-WARP v0.4
# W40 — MATHEMATICAL CONSISTENCY AUDIT

**Version:** 0.1  
**Status:** INDEPENDENT AUDIT · DRAFT  
**Date:** 6 November 2026  
**Scope:** W23′ / W30 / W34.1.3 / W39  
**Integration:** NOT MERGED  
**GitHub modifications:** NONE

## 0. Audit objective

W40 independently evaluates the mathematical consistency of the SUBIT-WARP v0.4 architecture.

The audit distinguishes:

1. correctness of definitions;
2. correctness of individual proofs;
3. compatibility between mathematical objects;
4. validity of theorem transfer;
5. boundary and endpoint behavior;
6. formalization requirements.

A theorem is not considered established merely because its formula appears in an earlier document.

## 1. Total coding architecture

Let:

Pos_b = B_b^{<ω}

and:

S_A = {ABSENT, INTERNAL} ∪ {LEAF(a): a∈A}.

Define:

Code_b(A) = S_A^{Pos_b}.

The product topology is compact because S_A is finite and Pos_b is countable.

The first-disagreement metric:

d_code(t,s) = 2^(−r(t,s))

is an ultrametric.

### Audit result M-001

ACCEPT.

### Audit result M-002

ACCEPT.

The metric induces the product topology.

The depth-zero case must remain explicitly defined:

r(t,s)=0 when the roots differ.

## 2. Local admissibility and compactness

The following local constraints are sufficient:

- ABSENT closure;
- LEAF closure;
- root restriction;
- optional full branching.

Every violation is detectable through finitely many coordinates.

Consequently, the admissible classes are closed.

By Tychonoff compactness:

C_Full and C_Partial are compact.

### Audit result M-003

ACCEPT.

### Audit result M-004

ACCEPT.

The result applies to the specified total coding representation.

It does not establish equivalence with every historical tree representation.

## 3. Infinite continuation

Define:

IB(u,t)

by existence of an infinite INTERNAL path extending u.

Then:

C_ω = {t∈C_Partial :

∀u, t(u)=INTERNAL ⇒ IB(u,t)}.

For each fixed u, the witness relation in:

C_Partial × [u]

is closed.

Its projection is compact and therefore closed.

The non-INTERNAL alternative is clopen.

Thus C_ω is closed.

Therefore:

C_ω is compact.

### Audit result M-005

ACCEPT, conditional on the exact coding and rooted-domain conventions.

The proof must not be generalized to infinite branching without additional assumptions.

## 4. Boundary and Ahlfors regularity

For:

d_v(ξ,η)=exp(−α_vℓ(ξ,η))

and uniform Bernoulli measure:

μ_b([σ])=b^(−|σ|),

set:

s=ln(b)/α_v.

For:

exp(−α_v n) ≤ r < exp(−α_v(n−1)),

the closed ball is:

B̄_v(ξ,r)=[ξ|n].

Therefore:

μ_b(B̄_v(ξ,r))=b^(−n).

Consequently:

r^s/b < μ_b(B̄_v(ξ,r)) ≤ r^s.

Hence:

dim_H(Σ_b,d_v)=ln(b)/α_v.

### Audit result M-006

ACCEPT.

Scope restriction:

The result concerns the full homogeneous boundary space.

It is not automatically a theorem about arbitrary partial trees.

## 5. Boundary map

The intended estimate is:

d_H,Σ(∂f,∂g) ≤ 2d_F(f,g).

The visual metric conversion:

d_v=d_Σ^γ

gives:

d_H,v(∂f,∂g) ≤ 2^γ d_F(f,g)^γ.

The conversion is valid for nonempty compact boundary sets.

### Audit result M-007

CONDITIONALLY ACCEPTED.

Required corrections:

1. Define the exact domain of d_F.
2. Establish whether d_F is the restriction of d_code.
3. Do not use an undefined d_P.
4. Separate the rooted boundary domain from the unrestricted coding domain.
5. Treat the depth-zero disagreement case as impossible on the rooted INTERNAL boundary domain.

The empty-boundary case remains outside the theorem.

## 6. Decreasing spectral kernel

For 0≤q<1:

c_q=(b−1)/(b−q).

λ_j(q)=−(1−q)q^(j−1)/[b^(j−1)(b−q)].

m_j=(b−1)b^(j−1).

The eigenvalue multiplicities and norm formulas are mutually consistent.

In particular:

‖T_q‖=c_q,

‖T_q‖²_HS=(b−1)/(b−q²),

‖T_q‖₁=2c_q,

Tr(T_q)=0.

At q=1:

T₁=P_const.

The endpoint is a separate operator definition.

### Audit result M-008

ACCEPT, subject to verification against the exact original W30 operator definition.

## 7. Increasing spectral kernel

Let:

t=exp(α_w)>1.

For t<b, the proposed eigenvalues are:

λ_j(t)=(t−1)t^(j−1)/[b^(j−1)(b−t)].

The constant eigenvalue is:

c_t=(b−1)/(b−t).

The multiplicities are:

m_j=(b−1)b^(j−1).

These formulas imply:

‖T_t‖=c_t,

‖T_t‖²_HS=(b−1)/(b−t²)

when t²<b.

The operator is compact for t<b.

For 1<t<b, the sum of absolute eigenvalues diverges.

Therefore it is not trace-class.

### Audit result M-009

ACCEPT CONDITIONALLY.

The spectral decomposition must be independently derived from the exact hierarchical subspaces.

## 8. Unboundedness threshold

The proposed threshold is:

T_t bounded ⇔ t<b.

The divergent row integral is insufficient as a standalone operator-norm proof.

Define:

K_t^(N)(ξ,η)=t^{min(ℓ(ξ,η),N)}.

Let T_t^(N) be the corresponding bounded finite-level operator.

For the constant unit vector:

⟨1,T_t^(N)1⟩ =

Σₖ₌₀ᴺ⁻¹ (b−1)b^(−k−1)tᵏ + (t/b)^N.

For t≥b, this quantity diverges as N→∞.

Therefore:

‖T_t^(N)‖→∞.

This establishes the required obstruction to a bounded positive integral-operator extension agreeing with the limiting kernel form.

### Audit result M-010

ANALYTICAL ARGUMENT STRENGTHENED.

Final proof closure assigned to W42.

## 9. Finite approximations

Let:

H_n = functions constant on cylinders of length n.

Then:

dim(H_n)=b^n.

For n=0:

H₀ is one-dimensional.

The matrix is:

[c_q].

For q=1:

T₁=P_const.

The finite matrix has rank one and all entries b^(−n).

For fixed q<1:

‖P_nT_qP_n−T_q‖₁→0.

This does not imply trace-norm convergence to P_const as q→1−.

### Audit result M-011

ACCEPT.

The two limiting procedures must remain distinct.

## 10. Structural reconstruction

For T-020′, the equivalence relations:

x~_k y ⇔ a(x,y)≥k

are justified by reflexivity, symmetry and the hierarchical triangle inequality.

The nesting of equivalence classes across consecutive levels defines parent relations.

Unary chains must be preserved.

For T-021′, prefix-free leaf addresses determine the occupied ordered trie.

However, occupied-trie reconstruction does not automatically recover the semantic state of every absent slot.

### Audit result M-012

CONDITIONALLY ACCEPTED.

Additional proof obligation:

Show that the level-class construction produces exactly one parent for each non-root vertex and that the resulting graph is connected and acyclic.

### Audit result M-013

ACCEPTED FOR OCCUPIED TRIES ONLY.

Absent-slot semantics remain a separate data structure.

## 11. W39 architectural consistency

The W39 architecture introduces a useful separation between:

- total codes;
- rooted codes;
- full codes;
- partial codes;
- infinite-continuation codes;
- coinductive tree objects.

However, the notation d_P is not yet sufficiently defined.

The boundary theorem must use one explicitly established metric.

The historical Tω and the new Tω_P must remain separate until correspondence is proved.

### Audit result M-014

ARCHITECTURAL CORRECTION REQUIRED.

## 12. Consolidated issue register

| ID | Issue | Severity | Next action |
|---|---|---|---|
| M-001 | Total coding | None | Preserve |
| M-002 | Ultrametric | None | Preserve |
| M-003 | Full compactness | None | Preserve |
| M-004 | Partial compactness | None | Preserve |
| M-005 | Infinite continuation | Low | Formalize |
| M-006 | Ahlfors regularity | None | Preserve |
| M-007 | Boundary metric | High | W41 |
| M-008 | Decreasing spectrum | Medium | W42 source verification |
| M-009 | Increasing spectrum | Medium | W42 derivation |
| M-010 | Unboundedness | High | W42 proof closure |
| M-011 | Finite approximations | Low | Regression |
| M-012 | Unordered reconstruction | Medium | W43 |
| M-013 | Ordered reconstruction | Medium | W43 |
| M-014 | Metric architecture | High | W39 correction |

## 13. Release implications

W40 does not authorize canonical integration.

The following remain open:

- historical-to-new type correspondence;
- complete boundary-map proof;
- independent spectral derivation;
- reconstruction uniqueness;
- Lean kernel verification;
- W20 regression;
- Rust implementation audit.

## 14. Final decision

**W40 v0.1 — PARTIAL MATHEMATICAL AUDIT COMPLETED.**

The principal definitions and several analytical constructions are consistent.

However, the architecture still contains unresolved type and metric interfaces.

**SUBIT-WARP v0.4 remains DRAFT / NOT STABLE.**

No canonical files have been modified.

DO NOT COLLAPSE — CONTEXTUALIZE.
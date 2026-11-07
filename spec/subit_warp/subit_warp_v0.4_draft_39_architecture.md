# SUBIT-WARP v0.4
# W39 — CONSOLIDATION ARCHITECTURE

**Version:** 0.1  
**Status:** ARCHITECTURE PROPOSAL · DRAFT  
**Date:** 6 November 2026  
**Repository:** sciganec/subit-subit  
**Target:** SUBIT-WARP v0.4  
**Predecessors:** W23′, W30, W31, W32, W34.1.3–W34.1.9  
**Next stages:** W40–W46  
**Integration:** NOT MERGED  
**GitHub modifications:** NONE

**Governing principle: DO NOT COLLAPSE — CONTEXTUALIZE.**

---

# 0. PURPOSE

W39 establishes a unified mathematical architecture for SUBIT-WARP v0.4.

Its purpose is not to introduce new mathematical results.

It establishes:

1. canonical mathematical objects;
2. canonical type distinctions;
3. admissible mappings between representations;
4. metric ownership and compatibility;
5. operator and spectral interfaces;
6. theorem dependency structure;
7. proof and implementation boundaries;
8. rules for integrating historical and corrected specifications.

W39 is an architectural consolidation document.

It does not establish that every proposed correspondence has already been proved.

## 0.1. Source hierarchy

The following hierarchy governs consolidation:

| Layer | Source | Responsibility |
|---|---|---|
| Mathematical foundation | W23′ | Definitions and mathematical structures |
| Theorem registry | W30 | Theorem statements and dependencies |
| Formalization architecture | W31 | Lean 4 design |
| Corrected integration | W34.1.3–W34.1.9 | Corrected definitions and correspondence proposals |
| Consolidation | W39 | Unified type and dependency architecture |
| Independent audit | W40 | Mathematical consistency |
| Formal closure | W41–W45 | Proofs, regression, Lean |
| Release decision | W46 | Independent release assessment |

A later document can refine an earlier proposal but cannot silently redefine an established mathematical object.

---

# 1. CANONICAL MATHEMATICAL UNIVERSE

## 1.1. Parameters

Let:

- b ∈ ℕ, b ≥ 2;
- B_b = {1,…,b};
- A be a finite alphabet of leaf labels;
- Pos_b = B_b^{<ω};
- Σ_b = B_b^ℕ.

The empty word ε is the root.

For u ∈ Pos_b:

- |u| denotes its depth;
- ui denotes the child in position i;
- [u] denotes the cylinder of infinite addresses extending u.

These definitions are shared by all subsequent tree and boundary constructions.

## 1.2. Finite state alphabet

Define:

S_A = {ABSENT, INTERNAL} ∪ {LEAF(a) : a ∈ A}.

The total coding space is:

Code_b(A) = S_A^{Pos_b}.

An element t ∈ Code_b(A) is a total function:

t : Pos_b → S_A.

Totality is essential.

Every address has a state, including addresses beneath leaves and absent positions.

This makes the representation independent of the particular finite shape of a tree.

## 1.3. Coordinate topology

Equip S_A with the discrete topology.

Equip Code_b(A) with the product topology.

Because S_A is finite and Pos_b is countable:

Code_b(A) is compact and metrizable.

Define the first-difference depth:

r_code(t,s) = min{|u| : t(u) ≠ s(u)}.

For t = s:

r_code(t,t) = ∞.

Define:

d_code(t,s) = 2^(−r_code(t,s)),

with 2^(−∞) = 0.

This is an ultrametric on the total coding space.

Its restrictions to closed admissible subclasses remain ultrametrics.

**Architectural decision:** d_code is the metric of the total coding representation. It must not automatically replace historical tree metrics.

---

# 2. CANONICAL TREE TYPES

This section establishes the most important type distinction in W39.

## 2.1. Unrestricted total codes

Define:

C_Partial^all ⊆ Code_b(A)

as the set of codes satisfying:

TC-02 — ABSENT closure:

t(u) = ABSENT ⇒ t(ui) = ABSENT.

TC-03 — LEAF closure:

t(u) = LEAF(a) ⇒ t(ui) = ABSENT.

No restriction is imposed on the root.

In particular:

t(ε) = ABSENT

is permitted.

This is the representation-level class.

## 2.2. Rooted partial codes

Define:

C_Partial ⊆ C_Partial^all

by:

t(ε) ≠ ABSENT.

This is the rooted partial-tree class.

An INTERNAL node may have any subset of its b child positions occupied.

The remaining positions are ABSENT.

Importantly, an INTERNAL node with no occupied children is permitted in C_Partial.

It is not automatically an element of the infinite-continuation subclass.

## 2.3. Full codes

Define:

C_Full ⊆ C_Partial

by adding:

TC-04:

t(u) = INTERNAL ⇒ t(ui) ≠ ABSENT

for every i ∈ B_b.

Thus every INTERNAL node has exactly b occupied child positions.

C_Full and C_Partial are distinct types.

## 2.4. Coinductive partial-tree representation

Define the coinductive representation:

PartialTree∞_A^(b) := νX.

None ⊔ Leaf(A) ⊔ Node(X^b).

Interpretation:

- None represents an absent position;
- Leaf(a) represents a labelled leaf;
- Node(children) represents an internal node with b ordered child positions.

The root may be None in the unrestricted type.

Define the rooted subtype:

PartialTree∞_A,root^(b).

It excludes None at the root.

**Important:** the coinductive representation is not automatically identical to the total coding space.

A correspondence must explicitly establish:

- preservation of root state;
- preservation of child positions;
- preservation of ABSENT closure;
- preservation of LEAF closure;
- preservation of order;
- preservation of the intended equality.

## 2.5. Historical finite and partial types

Preserve the legacy types:

FiniteTree_A^(b)

PartialTree_A^(b)

They must not be silently replaced by PartialTree∞.

The finite and infinite representations have different semantic commitments.

A finite inductive object does not automatically acquire coinductive semantics merely because it is embedded into a total coding space.

---

# 3. INFINITE CONTINUATION TYPES

## 3.1. Infinite branch predicate

For t ∈ C_Partial and u ∈ Pos_b, define:

IB(u,t)

if and only if:

1. t(u) = INTERNAL;
2. there exists ξ ∈ [u] such that every subsequent prefix of ξ has state INTERNAL.

Formally:

IB(u,t) ⇔

t(u) = INTERNAL ∧

∃ξ ∈ [u], ∀k ≥ |u|,

t(ξ|k) = INTERNAL.

## 3.2. Partial infinite-continuation class

Define:

C_ω,P = {t ∈ C_Partial :

∀u, t(u) = INTERNAL ⇒ IB(u,t)}.

Define:

Tω_P := C_ω,P.

This notation identifies the infinite-continuation class generated by the new partial-tree coding.

It does not redefine the historical Tω.

## 3.3. Nonempty-boundary subclass

Define:

∂t = {ξ ∈ Σ_b :

∀k ≥ 0, t(ξ|k) = INTERNAL}.

Define:

Tω_P⁺ = {t ∈ Tω_P : ∂t ≠ ∅}.

For the specified rooted coding:

Tω_P⁺ =

{t ∈ Tω_P : t(ε) = INTERNAL}.

This follows because an INTERNAL root in Tω_P has an infinite INTERNAL continuation.

## 3.4. Historical compatibility

Preserve separately:

- historical Tω;
- historical Tω⁺;
- new Tω_P;
- new Tω_P⁺.

No equality between these spaces is assumed.

Any identification requires a separate correspondence theorem.

This is a mandatory architectural restriction.

---

# 4. CANONICAL ENCODING AND DECODING

## 4.1. Encoding

Introduce:

Enc_sub :

PartialTree∞_A^(b) → C_Partial^all.

The intended mapping is structural:

None → ABSENT

Leaf(a) → LEAF(a)

Node(children) → INTERNAL at the current position, with recursively encoded children.

## 4.2. Decoding

Introduce:

Dec_sub :

C_Partial^all → PartialTree∞_A^(b).

The intended decoding is:

ABSENT → None

LEAF(a) → Leaf(a)

INTERNAL → Node(decoded children).

The local closure conditions guarantee that the coding is structurally admissible.

## 4.3. Required correctness theorems

W43 must establish:

ENC-01:

Dec_sub(Enc_sub(x)) = x.

ENC-02:

Enc_sub(Dec_sub(t)) = t.

ENC-03:

Enc_sub preserves root state.

ENC-04:

Enc_sub preserves ordered child positions.

ENC-05:

Enc_sub preserves the distinction between ABSENT and LEAF.

ENC-06:

Enc_sub preserves the distinction between INTERNAL and terminal states.

ENC-07:

The rooted restriction maps rooted trees to rooted codes.

ENC-08:

The full-tree restriction maps full trees to C_Full.

## 4.4. Critical distinction

The following must remain separate:

- a missing child;
- a known ABSENT child;
- an unknown or unrecorded child.

The total coding space explicitly represents ABSENT.

It does not automatically represent epistemic uncertainty.

If uncertainty is required, it must be introduced through an additional information-state layer.

This distinction is essential for T-021 and future implementations.

---

# 5. METRIC ARCHITECTURE

W39 prohibits accidental identification of metrics.

## 5.1. Coding metric

d_code:

Metric on Code_b(A), induced by first coordinate disagreement.

## 5.2. Full-tree metric

d_Full:

Historical metric associated with the full-tree representation.

Its relationship with d_code requires a dedicated isometry or metric-equivalence theorem.

## 5.3. Partial-tree metric

d_P:

Metric associated with the partial-tree representation.

Its relationship with d_code must be established through Enc_sub.

Do not assume that the two metrics coincide.

## 5.4. Historical forest metric

d_F:

Preserve the established W23′/W34 first-difference metric where its original domain is intended.

If its domain changes, record the change explicitly.

## 5.5. Boundary metric

On:

Σ_b = B_b^ℕ

define:

d_Σ(ξ,η) = 2^(−ℓ(ξ,η)),

where ℓ is the common-prefix length.

For α_v > 0:

d_v(ξ,η) = exp(−α_v ℓ(ξ,η)).

Equivalently:

d_v = d_Σ^γ,

where:

γ = α_v / ln 2.

## 5.6. Hausdorff metric

For nonempty compact subsets of Σ_b:

d_H,Σ.

For the visual metric:

d_H,v.

The metric conversion must preserve:

d_H,v(C,D) = d_H,Σ(C,D)^γ.

## 5.7. Metric compatibility register

| Metric | Domain | Status |
|---|---|---|
| d_code | Total coding space | Defined |
| d_Full | Full-tree space | Historical |
| d_P | Partial-tree space | Historical/new correspondence pending |
| d_F | Established first-difference domain | Preserve |
| d_Σ | Infinite boundary | Defined |
| d_v | Visual boundary | Defined |
| d_H,Σ | Nonempty compact boundaries | Defined |
| d_H,v | Visual compact boundaries | Defined |

No metric conversion is accepted without an explicit theorem.

---

# 6. BOUNDARY MAP ARCHITECTURE

Define the boundary map on the correct domain:

∂ : Tω_P⁺ → K(Σ_b),

where K(Σ_b) denotes nonempty compact subsets.

The principal estimate to be independently audited is:

d_H,Σ(∂f,∂g) ≤ 2d_P(f,g).

The corresponding visual estimate is:

d_H,v(∂f,∂g) ≤

2^γ d_P(f,g)^γ.

These estimates are not interchangeable without the required metric correspondence.

## 6.1. Required proof cases

W41 must examine:

1. first disagreement at the root;
2. first disagreement at depth m > 0;
3. different INTERNAL/ABSENT states;
4. different INTERNAL/LEAF states;
5. different leaf labels;
6. existence of nonempty boundaries;
7. the relationship between first-difference depth and common boundary prefixes.

## 6.2. Empty boundaries

The domain K(Σ_b) excludes empty sets.

Do not extend the theorem to empty boundaries by convention alone.

An extension to K₀(Σ_b) requires its own Hausdorff metric definition and proof.

**Status:** OPEN until W41 closes the required cases.

---

# 7. SPECTRAL ARCHITECTURE

The spectral theory operates on the boundary probability space, not directly on the combinatorial tree representation.

## 7.1. Base probability space

Let:

H = L²(Σ_b, μ_b),

where μ_b is the uniform Bernoulli measure.

For a finite word σ of length n:

μ_b([σ]) = b^(−n).

## 7.2. Finite-level subspaces

Let H_n be the subspace of functions constant on cylinders of length n.

Let P_n be the orthogonal projection onto H_n.

Define:

T_q^(n) = P_n T_q P_n | H_n.

## 7.3. Decreasing kernel

Preserve the W30 spectral definitions:

c_q = (b−1)/(b−q).

λ_j(q) =

−(1−q)q^(j−1) /
[b^(j−1)(b−q)].

m_j = (b−1)b^(j−1).

The endpoint conventions remain explicit:

q = 0:

λ₁(0) = −1/b,

λ_j(0) = 0 for j ≥ 2.

q = 1:

T₁ = P_const.

The trace, operator norm, Hilbert–Schmidt norm and trace norm are separate properties.

## 7.4. Increasing kernel

Set:

t = exp(α_w) > 1.

The principal boundedness threshold is:

t < b.

Equivalently:

α_w < ln b.

The Hilbert–Schmidt threshold is:

t² < b.

Equivalently:

α_w < (ln b)/2.

The compactness and non-trace-class results are extensions of the original T-012.

Preserve separate identifiers:

- T-012 — primary result;
- T-012a — compactness;
- T-012b — non-trace-class result.

## 7.5. Spectral proof obligation

W42 must independently establish the unboundedness claim for t ≥ b.

The divergence of the kernel row sum is not, by itself, a complete formal proof of unboundedness.

The audit must construct truncated kernels and suitable quadratic forms whose values become unbounded.

It must also verify:

- domain assumptions;
- positivity;
- convergence of truncated operators;
- endpoint behavior;
- consistency of eigenvalue multiplicities.

---

# 8. FINITE APPROXIMATION ARCHITECTURE

For n ≥ 0:

dim(H_n) = b^n.

In the normalized cylinder basis:

e_σ = b^(n/2)1_[σ].

The finite approximation is:

T_q^(n) = P_n T_q P_n | H_n.

The following cases must remain explicit.

### n = 0

H₀ is one-dimensional.

The matrix is:

[c_q].

### q = 1

T₁ = P_const.

Its finite-level matrix has all entries equal to b^(−n).

It has rank one.

### Fixed q < 1

The established trace-norm approximation is:

‖P_nT_qP_n − T_q‖₁ → 0.

This must not be confused with:

‖T_q − P_const‖₁

as q → 1−.

The two limits represent different processes.

---

# 9. STRUCTURAL RECONSTRUCTION

Preserve two distinct reconstruction systems.

## 9.1. Unordered reconstruction

T-020′ uses:

F(T) = (L,h,a).

The admissibility conditions FP-01–FP-06 must remain explicit.

The relation:

x ~_k y ⇔ a(x,y) ≥ k

constructs equivalence classes at each depth.

The reconstruction must preserve unary chains.

The uniqueness claim is up to rooted unordered isomorphism.

## 9.2. Ordered reconstruction

T-021′ adds:

p : L → B_b^{<ω}.

The address map must be:

- injective;
- prefix-free;
- depth-preserving;
- compatible with common-prefix lengths.

This reconstructs an occupied ordered trie.

It does not independently encode epistemic uncertainty about absent positions.

That information requires a separate slot-state structure.

---

# 10. DEPENDENCY GRAPH

The following dependency graph governs the next stages.

```text
PARAMETERS
    │
    ▼
BASE ALPHABETS
    │
    ▼
TOTAL CODING SPACE
    │
    ├───────────────┐
    ▼               ▼
C_FULL          C_PARTIAL_ALL
                    │
                    ▼
                C_PARTIAL
                    │
                    ▼
                Tω_P
                    │
                    ▼
               Tω_P_PLUS
                    │
                    ▼
                BOUNDARY
                    │
                    ▼
               BOUNDARY MAP
                    │
                    ▼
             HAUSDORFF ESTIMATES


COINDUCTIVE TREE TYPE
          │
          ▼
      Enc_sub
          │
          ▼
    TOTAL CODING
          │
          ▼
      Dec_sub
          │
          ▼
  CORRESPONDENCE THEOREMS


BOUNDARY PROBABILITY SPACE
          │
          ▼
       L² SPACE
          │
          ▼
    SPECTRAL OPERATORS
          │
          ├──────────────┐
          ▼              ▼
     INFINITE        FINITE-LEVEL
     OPERATORS       APPROXIMATIONS
          │              │
          └──────┬───────┘
                 ▼
          SPECTRAL AUDIT
```

The graph is intentionally acyclic.

No theorem may depend on its own unproved correspondence.

---

# 11. CANONICAL MODULE ARCHITECTURE

W31's Lean blueprint should follow the same conceptual separation.

Proposed modules:

| Module | Responsibility |
|---|---|
| Basic | Parameters, alphabets, addresses |
| Coding | Total codes and local admissibility |
| TreeTypes | Finite, partial, full, coinductive types |
| Encoding | Enc_sub and Dec_sub |
| Metrics | Coding and tree metrics |
| Boundary | Infinite addresses and boundary sets |
| Geometry | Hausdorff and visual metrics |
| Measure | Bernoulli measure |
| Operators | Integral operators |
| Spectral | Eigenvalues and operator classes |
| Approximation | Finite-level projections |
| Structure | Fingerprints and reconstruction |
| Verification | Main theorem interfaces |

Each module must depend only on earlier modules in the dependency graph.

Avoid importing the entire project into every theorem file.

---

# 12. PROOF STATUS AND EVIDENCE POLICY

Every mathematical claim must carry one of the following statuses:

**ANALYTICAL**

A mathematical proof has been provided and independently checked.

**NUMERICAL**

A finite computational experiment supports the claim.

**LEAN-CHECKED**

The relevant theorem has been accepted by the Lean kernel.

**IMPLEMENTATION-VERIFIED**

The corresponding implementation has passed the specified tests and audit.

These statuses are independent.

For example:

ANALYTICAL ≠ LEAN-CHECKED.

NUMERICAL ≠ PROOF.

IMPLEMENTATION-VERIFIED ≠ MATHEMATICAL COMPLETENESS.

No document may promote a result from one category to another without evidence.

---

# 13. W39 CONSOLIDATION DECISIONS

The following decisions are proposed as architectural constraints:

| ID | Decision | Status |
|---|---|---|
| C-01 | Total coding space is the common representation layer | ACCEPT |
| C-02 | Rooted and root-unrestricted codes are separate | ACCEPT |
| C-03 | Full and partial trees are separate | ACCEPT |
| C-04 | Historical Tω is preserved | ACCEPT |
| C-05 | New partial infinite-continuation class is Tω_P | ACCEPT |
| C-06 | Tω_P and Tω_P⁺ are separate | ACCEPT |
| C-07 | PartialTree∞ remains coinductive | ACCEPT |
| C-08 | Enc_sub and Dec_sub require inverse proofs | OPEN |
| C-09 | Historical metrics cannot be silently replaced | ACCEPT |
| C-10 | Boundary map excludes empty boundaries | ACCEPT |
| C-11 | Spectral operators belong to boundary L² | ACCEPT |
| C-12 | Finite approximations are separate operator objects | ACCEPT |
| C-13 | Fingerprint reconstruction preserves ordered/unordered distinction | ACCEPT |
| C-14 | Lean and numerical evidence remain separate | ACCEPT |

---

# 14. REMAINING ARCHITECTURAL RISKS

W39 identifies the following unresolved questions.

### R-01 — Coinductive correspondence

Does Enc_sub establish a genuine bijection between the intended coinductive tree type and the total coding class?

### R-02 — Metric preservation

Does Enc_sub preserve d_P and d_code exactly, or only up to a controlled equivalence?

### R-03 — Historical compatibility

Which historical W23′ and W30 objects correspond to the newly defined partial-tree spaces?

### R-04 — Infinite continuation

Does the proposed compactness proof transfer without additional hypotheses to the final canonical type Tω_P?

### R-05 — Boundary estimate

Does T-007 remain valid under the precise metric selected for the new partial-tree representation?

### R-06 — Spectral unboundedness

Can the t ≥ b claim be established through explicit truncated quadratic forms?

### R-07 — Reconstruction semantics

Does the fingerprint contain sufficient information for every intended tree interpretation?

### R-08 — Formalization

Can the proposed type distinctions be represented in Lean without introducing unjustified axioms or collapsing distinct structures?

---

# 15. W39 EXIT CRITERIA

W39 is ready for architectural review when:

1. every canonical object has a unique type;
2. every mapping has a declared domain and codomain;
3. every metric has an explicit domain;
4. historical and corrected objects are distinguishable;
5. theorem dependencies are acyclic;
6. unresolved correspondences are explicitly marked;
7. mathematical claims are not promoted beyond their evidence;
8. W40 can audit the architecture without reconstructing definitions from several documents.

W39 does not require that all mathematical proofs be complete.

Those belong to subsequent stages.

---

# 16. FINAL STATUS

**W39 — CONSOLIDATION ARCHITECTURE**

ARCHITECTURE PROPOSAL · READY FOR REVIEW.

**SUBIT-WARP v0.4**

DRAFT · NOT STABLE.

**W40–W46**

NOT YET COMPLETED.

**Canonical integration:** NOT PERFORMED.

**GitHub modifications:** NONE.

The governing principle remains:

**DO NOT COLLAPSE — CONTEXTUALIZE.**
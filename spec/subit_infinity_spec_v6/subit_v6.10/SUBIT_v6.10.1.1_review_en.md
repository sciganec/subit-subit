# Self-Reference, Stability, and Formal Humility

## The SUBIT-∞ system at v6.10.1.1-STABLE

---

## Abstract

SUBIT-∞ is a formal notation system for self-referential dynamical systems: systems in which the rule of evolution is a component of the state rather than an external parameter. This article introduces the system to a philosophical audience, presents the first STABLE release of its formal specification (v6.10.1.1), situates it within established traditions of coalgebra, four-valued logic, dynamic topology, and intensional type theory, and reflects on the epistemological significance of its explicit proof-status registry. The central philosophical claim advanced here is modest: SUBIT-∞ does not propose a new foundation for mathematics or logic, nor does it make empirical claims about any concrete system. It proposes a structuring vocabulary for hypotheses about self-referential dynamics, together with an unusually explicit accounting of what within that vocabulary is proved, what is provable only conditionally, and what remains open. In this respect it constitutes a case study in what Ferdinand Gonseth called *philosophie ouverte* — a formal apparatus whose epistemic honesty consists less in the strength of its theorems than in the transparency with which it records the limits of its own justification.

---

## 1. Introduction

Contemporary philosophy of mathematics has largely settled into two broad attitudes toward formal systems. On one side, foundationalism: a formal system is judged by the strength and reliability of its foundations, and its philosophical interest derives from the theorems it makes available. On the other side, a looser structuralism: formal systems are treated as instruments whose value is measured by their capacity to organize mathematical practice, without strong foundational commitments. Between these attitudes lies a less discussed middle ground, occupied by what one might call **specifications with explicit epistemic accounting**: formal documents that record, for every nontrivial claim, precisely what is proved, what is assumed, and what remains open, and that refuse to blur the boundary between these categories.

SUBIT-∞, whose first STABLE release is dated 11 October 2026, belongs to this third category. Its declared purpose is to provide a notation for **self-referential dynamical systems** — systems in which the rule of evolution is not an external parameter but a component of the state itself. Its formal apparatus is deliberately modest: a finite alphabet of four symbols, a finite state space of 64 states, a coalgebra of trees with labels from that alphabet, an ultrametric on those trees, a stability classifier taking values in a finite chain, and a modal language for reasoning about trajectories. What is unusual is not the mathematics but the **administrative discipline** with which the system records its own epistemic status.

This article has three aims. First, to introduce SUBIT-∞ to a philosophical audience unfamiliar with its architecture. Second, to explain what is genuinely novel in the recent STABLE release, especially its explicit handling of conditional proofs. Third, to argue that the system's main philosophical interest lies not in its individual theorems but in the pattern of epistemic accounting it exemplifies — a pattern that may be of use to philosophers working on the epistemology of formalized theories more broadly.

The article proceeds as follows. §2 describes the four-level architecture. §3 details the specific content of the STABLE release and the four changes it introduces relative to its predecessor. §4 discusses the philosophical significance of the proof-status registry. §5 situates SUBIT-∞ within established traditions. §6 identifies open questions of philosophical interest. §7 concludes.

---

## 2. The architecture of SUBIT-∞

### 2.1 Four cumulative levels

SUBIT-∞ is organized as a cumulative hierarchy of four levels, each adding a single structural layer to the previous one:

```text
SUBIT-64 ≼ₐ SUBIT⁺ ≼ₐ SUBIT-CAT ≼ₐ SUBIT-∞
```

The symbol `≼ₐ` denotes **architectural extension** rather than set-theoretic inclusion: the later level does not literally contain the earlier one, but enriches the descriptive apparatus in a way that supersedes it for the purposes of the specification. This cautious choice of notation is itself philosophically motivated — it refuses to claim what has not been proved.

**SUBIT-64** fixes a finite alphabet of four symbols, coded as two-bit words, together with a 64-element state space S₀ = A × A × A. Two mutually isomorphic interpretations of A are provided: a semantic one (WHO × WHERE × WHEN with four values each) and a logical one (Belnap's four-valued bilattice). The level is explicitly *static*: no transition operator, no dynamics.

**SUBIT⁺** adds internal rule dynamics. A rule ρ : S₀ → S₀ is not an external parameter of evolution but a component of the extended state ŝ = (s, ρ) ∈ S₀ × ℛ. The evolution operator

```text
D₀(s, ρ) := ( ρ(s), g₀(ρ, s) )
```

applies the current rule to the state and updates the rule via a metaevolution g₀. This yields the four levels of self-reference familiar from the theory of reflective systems, but with a crucial clarification: SUBIT⁺ is **not** claimed to be more expressive than a finite automaton. The specification explicitly withdraws any such claim, retaining only the narrow result that autonomous finite automata with at most 64 states embed into SUBIT⁺ (A4).

**SUBIT-CAT** introduces three classifiers working over the same domain:

- `Classify⁺_D(P) = (OrbitType, InclusionType, ChaosStatus, Min)`, a four-component classification of *sets* under a dynamics D.
- `Ω_point^fin` and `Ω_point^∞`, pointwise classifiers for the finite and infinite levels.
- `Ω_set`, a projection of `Classify⁺` onto a six-element chain, from CHAOTIC_set to INVARIANT_FIXED.

The level also introduces the category SUBIT of self-referential systems, its subcategory SUBIT_full with g-compatible morphisms, and the category Dyn of ordinary dynamical systems with its standard embedding into SUBIT.

**SUBIT-∞** extends the state space to a coalgebra of trees

```text
S∞ := Tree∞
```

whose definition is given by four local conditions (T1)–(T4) on functions f : Pos → Λ, with Pos = {1,2,3}^{<ω} and Λ = {None, node} ∪ {leaf(a) : a ∈ A}. On S∞ one defines an ultrametric d_S, a space ℛ₀ of 1-Lipschitz ("causal") rules, and under an assumption (H) on the space R ⊆ ℛ₀ and metaevolution g∞, a dynamics D∞ on the product X = S∞ × R. The classification of trajectories proceeds via ω-limits, giving six classes S(τ): FIXED, PERIODIC, MIN_ZERO, MIN_POS, NONMIN_ZERO, NONMIN_POS. The system also introduces a trajectory metric d_Ω_traj — a Hamming distance on diagnostic codes — and a finite registry of witnesses W1–W5 for the realizability table.

### 2.2 The classifier Ω and its logical structure

The stability classifier Ω is a six-element chain:

```text
CHAOTIC_set < APERIODIC_NON_CHAOTIC < EVENTUALLY_PERIODIC
            < PERIODIC_SET < INVARIANT_DYNAMIC < INVARIANT_FIXED
```

With ∧ = min, ∨ = max, and relative pseudocomplementation a → b := ⊤ if a ≤ b, b otherwise, Ω forms a **Heyting algebra** — a linear model of intuitionistic logic. The law of excluded middle fails: for any intermediate element a, we have a ∨ ¬a = a ≠ ⊤. This is not presented as a metaphysical claim about dynamics but as a structural consequence of the six-element chain's order theory.

The specification is careful to note that Ω is a **syntactic tool** and is not formally connected to the Belnap bilattice carried by the base alphabet A. This separation prevents an easy but unfounded identification between the semantics of the alphabet and the syntax of classification.

### 2.3 The modal layer

Two modal systems are developed in parallel and kept strictly separated. The first is an LTL-like semantics of trajectories, with the usual next-step, eventually, always, and recurrence operators. The second is a Heyting-valued semantics for algebraic propositions about Ω. The specification explicitly proves (M3) that the classical duality ◇_H U = ¬_H □_H ¬_H U fails in the Heyting-valued semantics, exhibiting a two-point countermodel. This failure is presented not as a defect but as a structural feature of intuitionistic-valued dynamics.

A dynamic type theory is also developed, with the judgment Γ ⊢ t : U @ τ interpreted as "the term t has type U at time τ". The stable type rule uses D[U] ⊆ U rather than D[U] = U — a deliberate weakening with a philosophical motivation: the weaker condition suffices for the preservation of modal stability, and the stronger condition would impose an unnecessary constraint.

---

## 3. What is new in v6.10.1.1-STABLE

The v6.10.1.1 release integrates four changes from a broader development line (v6.10.2–v6.10.12) that did not conflict with the proofs already present in v6.10.1. The changes are the following.

### 3.1 Explicit contract (H1)–(H3) for the infinite level

Earlier editions used an assumption (H) whose content was scattered through the text. The STABLE release consolidates it into three explicit conditions:

- **(H1)** (S∞, d_S) is a compact ultrametric space.
- **(H2)** R ⊆ ℛ₀ is a nonempty compact subspace under the metric d_ℛ.
- **(H3)** g∞ : R × S∞ → R is continuous and total.

The reason this matters philosophically is that H1 depends on two theorems — T3 (that d_S is an ultrametric) and T5 (that Tree∞ is compact) — and both are *proved* in the STABLE release. H2, by contrast, is assumed: the compactness of R is not derived from the compactness of ℛ₀ in this release, because the latter (T6) has the status DP-s rather than DP-f. The specification is honest about this distinction, and the registry labels every theorem that relies on H1–H3 with the qualifier "за H" (conditional on H).

### 3.2 Complete proof of the upper entropy bound in W5

Earlier editions established only the lower bound for the topological entropy of the full shift on two symbols: h_top ≥ log 2. The STABLE release contains the complete proof of the upper bound, using the standard argument: for any ε > 0, choose L with 2^{−(L+1)} < ε; sequences agreeing on the first n + L symbols are not (n, ε)-separated, so s(n, ε) ≤ 2^{n+L}, whence limsup (1/n) log s(n, ε) ≤ log 2. Passing to ε → 0⁺ and combining with the lower bound gives h_top = log 2.

This proof matters because it completes the construction of the witness `NONMIN_POS × ATTAINED` — a trajectory whose ω-limit is infinite, non-minimal, and has positive topological entropy, with the trajectory itself attaining that limit. It is the only witness for this cell of the realizability table that does not depend on the external theorem EXT-1.

### 3.3 Typization of the odometer witness W4

An earlier version of the odometer construction (W4, `MIN_ZERO × ATTAINED`) used the notation "α = 0, β = 1" for the two letters α, β ∈ A. This was a type error: 0 and 1 are not elements of A = {00, 01, 10, 11}. The STABLE release fixes this by introducing an explicit coordinate bijection

```text
enc_αβ : {0,1}^ℕ → {α, β}^ℕ,  enc_αβ(a)_i := α if a_i = 0, β if a_i = 1
```

and defining the odometer on C = {α, β}^ℕ by conjugation: Õ := enc_αβ ∘ O ∘ enc_αβ⁻¹. This yields three distinct maps — O on B = {0,1}^ℕ, Õ on C, and T = t ∘ Õ ∘ t⁻¹ on Y ⊆ S∞ — that were previously conflated. The proof of the witness then uses each map in its proper domain.

The philosophical interest of this correction is not that it changes any mathematical result, but that it illustrates a general hazard in formalization: an identity of notation across distinct domains can hide a type error that is invisible at the level of prose but fatal in a proof assistant.

### 3.4 Conditional qualifiers in the registry

The final change is administrative. The registry (Appendix D) now carries explicit qualifiers for theorems that are proved only under the assumptions of §10.2. Thus W1–W5, D4, D3′, T7, T8, C5b, D1, and D6 are labeled "DP-f за H" rather than plain "DP-f". The qualifier signals that the proof is complete but conditional: if (H1)–(H3) hold, the theorem holds; if they fail, the theorem is not asserted.

This may seem like a small bookkeeping matter, but it is precisely the point of the STABLE release's epistemology, discussed in §4 below.

---

## 4. The epistemology of proof-status registries

The most interesting philosophical feature of SUBIT-∞ v6.10.1.1 is not any of its theorems but the registry of proof statuses that accompanies them. The registry uses a small vocabulary:

- **DP-f**: a complete proof is written out in the text.
- **DP-s**: the proof is sketched, or follows from a standard theorem without the intermediate steps being reproduced.
- **DP-f за H**: a complete proof, conditional on the explicit assumptions H1–H3.
- **DP-f за EXT-1**: a complete proof, conditional on the external theorem EXT-1.
- **ВИЗНАЧЕНО**: a definition or convention, not a theorem.
- **ВІДКРИТО**: an open question.
- **НЕ ПІДТВЕРДЖЕНО**: no evidence of implementation, testing, or proof.

### 4.1 Against proof-status inflation

The registry is designed to resist what one might call **proof-status inflation**: the tendency of formal documents to claim more epistemic warrant than they possess. In particular, the release's rule for assigning DP-f is stated explicitly: *DP-f is assigned only when the proof is actually present in the document*. The consequence is that a theorem can be *true* and *known to the author to be true* and yet receive a lower status than DP-f, if the proof in the text has been shortened to a sketch or replaced by a reference to a standard result.

This rule has philosophical precedents. The intuitionist tradition has always insisted on the distinction between "true" and "provable", but that distinction is usually about the mathematics. The SUBIT registry applies it to the *documentation*: within a single formal document, a claim's status is determined by what the document itself contains, not by what the mathematical community knows. The registry thus becomes a local epistemology of the document, self-contained and self-auditing.

### 4.2 Two kinds of conditionality

The registry distinguishes two forms of conditional proof, which have different philosophical profiles.

**Conditional on (H1)–(H3)** is a form of *internal* conditionality: the assumptions are stated within the specification, they are recognizable mathematical properties (compactness, continuity), and the theorems derived from them would remain valid if the assumptions were subsequently proved or disproved within the same framework. The reader is invited to consider the theorems as implications: (H1)–(H3) ⇒ T7, etc.

**Conditional on EXT-1** is a form of *external* conditionality: EXT-1 asserts the existence of a minimal subshift of positive topological entropy over the binary alphabet, and its proof lies outside the specification, in the symbolic dynamics literature (Grillenberger 1973; Jewett 1970; Krieger 1972; and, for the one-sided case, Moothathu–Oprocha 2013). The specification does not reconstruct this proof. It cites it and marks every result that depends on it.

The distinction is not merely pragmatic. Internal conditionality is a form of *parametric generality*: the theorems are true for any system satisfying H1–H3. External conditionality is a form of *bibliographic reliance*: the theorems are true for the specific construction that EXT-1 provides, on the authority of the cited sources. The registry keeps the two forms separate.

### 4.3 Honest limitation as content

A striking feature of the STABLE release is that the limits of the system are stated as part of the content, not as an appendix. The flag panel declares eight status flags, of which only two are green: DEFINED and PROVED ON PAPER. The remaining six — AUDITED BY EXECUTION, LEAN-CHECKED, BUILD-PASSED, IMPLEMENTED (conformant), EMPIRICALLY SUPPORTED — are red. This is not a temporary state to be remedied but a declaration of the release's epistemic scope: it is a paper specification, no more.

The registry also contains a number of open cells in the realizability table (§11.5). Six cells are proved without external theorems; one is proved conditionally on EXT-1; five are open. The open cells are not hidden; they are enumerated, and the corresponding questions (Q10′, Q10″) are listed in the open-questions appendix.

---

## 5. Relationship to established frameworks

SUBIT-∞ does not claim originality in any of its individual components. Its components are drawn from established traditions, and the philosophical interest lies in how they are combined.

### 5.1 Coalgebra

The space S∞ is defined as the final coalgebra of the functor Φ(X) = A ⊔ X³. This construction belongs to the standard theory of coalgebra (Aczel 1988; Rutten 2000) and is closely related to the space of *labelled trees* studied in computer science and modal logic. The four local conditions (T1)–(T4) on functions f : Pos → Λ give an explicit presentation of this coalgebra as a closed subset of the product space Λ^Pos, which is where the compactness of S∞ (theorem T5) comes from. The choice to work with an explicit address-based presentation rather than with the abstract coalgebra is motivated, as the specification notes, by the desire to have a compactness proof that does not depend on more abstract theory.

### 5.2 Four-valued logic

The base alphabet A carries the structure of Belnap's four-valued bilattice (Belnap 1977a/b; Dunn 1976), with two orders — truth and information — that are independent and neither of which is a total order. The specification is careful not to transfer this structure automatically to the dynamics on S∞; the bilattice structure is a property of the alphabet, not of the tree space.

The classification lattice Ω, by contrast, is a six-element *chain*, and carries the structure of a Heyting algebra (a linear model of intuitionistic logic). This is different from Belnap's bilattice: intuitionistic logic has a linear semantics with a non-classical negation, whereas Belnap's logic has a non-linear semantics with two independent negations. The specification explicitly notes that Ω is "not formally connected" to the Belnap bilattice.

### 5.3 Symbolic dynamics and the transfer operator

The constructions of §9.5 (the "spine" embedding t : C → S∞, the space Y = t[C], and the shift T = t ∘ σ ∘ t⁻¹ on Y) belong to the transfer-operator tradition in symbolic dynamics. The witness W5 uses a *complete* sequence a ∈ {α, β}^ℕ (one in which every finite word occurs infinitely often) to produce a ω-limit equal to the whole shift space, and the entropy calculation uses the standard combinatorial argument for the full shift.

The witness W4 (the odometer) uses the 2-adic structure of {0,1}^ℕ, which is a standard model of minimal, non-periodic, measure-preserving dynamics with zero entropy. The witness's role in the realizability table is to demonstrate that `MIN_ZERO × ATTAINED` is realized by a system satisfying the hypothesis (H) of the specification.

### 5.4 Categorical logic

The category SUBIT of self-referential systems, its subcategory SUBIT_full, and the category Dyn of ordinary dynamical systems are defined in the style of Lawvere's categorical logic (Lawvere 1964, 1970; Lambek & Scott 1986). The embedding Dyn₊ → SUBIT (theorem K5) is a full and faithful functor from the category of dynamical systems with nonempty state space. The specification is careful to note that the topos structure of Dyn does not transfer automatically to SUBIT, and the corresponding open question (Q2′) is registered.

### 5.5 Gonseth's *philosophie ouverte*

The Swiss philosophical tradition offers a natural point of reference for the epistemic attitude of SUBIT-∞. Ferdinand Gonseth (1890–1975), founder of *Dialectica* and central figure in twentieth-century Swiss philosophy of science, argued for a *philosophie ouverte* in which formal systems are not judged by their foundational completeness but by their capacity to be revised in the light of experience and formal development. The SUBIT registry — with its explicit statuses, its conditional proofs, and its open cells — is a formal realization of this attitude. The system does not present itself as a closed theory; it presents itself as an instrument whose epistemic scope is delimited by explicit registries and whose open questions are enumerated rather than hidden.

---

## 6. Open questions of philosophical interest

The specification lists a number of open questions, some of which have philosophical as well as mathematical interest.

**Q1 — Cartesian closedness of SUBIT.** The exponential object Yˣ is defined only for objects X with invertible dynamics. Whether SUBIT is cartesian closed in full generality is open. This matters for the categorical-logical interpretation of the system: without cartesian closedness, the internal language of the category is not automatically a typed λ-calculus.

**Q2′ — Intermediate topos between Dyn and SUBIT.** Whether there exists a category C with Dyn ⊆ C ⊆ SUBIT that is a topos and preserves nontrivial metaevolution is open. This is a question about the extent to which the standard topos-theoretic tools of categorical logic transfer to the self-referential setting.

**Q7 — Universal object with proved universal property.** Earlier editions of the specification proposed a universal object U that would interpret any system in the category. The current release withdraws this claim and registers it as open. The philosophical interest lies in the fact that the withdrawal is explicit: the universal object is not claimed, only conjectured.

**Q10′ and Q10″ — realizability of open cells.** Five cells of the realizability table for trajectory classes remain open, including the question whether `CHAOTIC × NONATTAINED` (positive entropy with a trajectory that does not attain its ω-limit) is realizable. Q10″ asks a related question about zero entropy for a particular candidate class.

**Q9 — Consistency of the modal system.** The consistency of the Heyting-valued modal logic together with the six-element Ω is registered as open. This is a question of the sort usually addressed by algebraic semantics.

**Q25-new — Density of computable causal rules.** Whether the intersection ℛ_comp ∩ ℛ_caus is dense in ℛ_caus under the uniform metric is open. This connects the specification's treatment of causality (a metric condition) to its treatment of computability (a description-based condition).

The philosophical interest of these open questions is that they are not merely technical. Each of them concerns a place where the specification has deliberately refrained from claiming more than its arguments support. The registry treats them as content, not as defects.

---

## 7. Conclusion: SUBIT-∞ as an instrument

The central thesis of SUBIT-∞ — stated at the end of the specification itself — is that "the rule belongs to the state". This is not a metaphysical claim about the nature of reality but a **notation choice**: the system is designed so that rule-dynamics and state-dynamics are treated in a single framework, and metadynamics is a first-class object rather than an external parameter.

The philosophical contribution of the system, on the reading presented here, is not the strength of its theorems but the *discipline of its documentation*. In a period when formal systems are increasingly produced by and for machine verification, and when the boundary between proof and assertion can easily be blurred, the SUBIT registry proposes a model: every nontrivial claim carries an explicit status, every conditional proof carries an explicit qualifier, every open question is enumerated, and the boundaries of the release's epistemic scope are declared in the flag panel at the top.

Whether the system will prove useful for concrete philosophical or scientific work is an empirical question that only use can answer. But the *form* of the release — its registry, its conditional qualifiers, its honest limitation of scope — is itself an object of philosophical interest. It is a small case study in what Gonseth called *philosophie ouverte*, and it demonstrates that a formal specification can be rigorous without being arrogant, complete within its stated scope without claiming universal applicability.

The v6.10.1.1-STABLE release is the system's first stable published edition. It is not a conclusion but a checkpoint: a moment at which the architecture is fixed, the proofs are collected, the open questions are enumerated, and the system is declared ready for the next phase of work — Lean formalization, implementation, and use. Nothing in this article claims that the system will succeed at that next phase. What is claimed is that the form of its presentation deserves philosophical attention in its own right.

---

## References

Aczel, P. (1988). *Non-Well-Founded Sets*. CSLI Lecture Notes 14.

Belnap, N. D. (1977a). A useful four-valued logic. In *Modern Uses of Multiple-Valued Logic*, eds. J. M. Dunn and G. Epstein, 5–37. Reidel.

Belnap, N. D. (1977b). How a computer should think. In *Contemporary Aspects of Philosophy*, ed. G. Ryle, 30–56. Oriel Press.

Dummett, M. (1959). A propositional calculus with denumerable matrix. *Journal of Symbolic Logic* 24(2), 97–106.

Dunn, J. M. (1976). Intuitive semantics for first-degree entailments and 'coupled trees'. *Philosophical Studies* 29(3), 149–168.

Glasner, E., and Weiss, B. (1994). Strictly ergodic, uniform positive entropy models. *Bulletin de la Société Mathématique de France* 122(3), 399–412.

Gonseth, F. (1936). *Les mathématiques et la réalité*. Alcan.

Gödel, K. (1932). Zum intuitionistischen Aussagenkalkül. *Anzeiger der Akademie der Wissenschaften in Wien* 69, 65–66.

Grillenberger, C. (1973). Constructions of strictly ergodic systems I. Given entropy. *Zeitschrift für Wahrscheinlichkeitstheorie und verwandte Gebiete* 25, 323–334.

Hensel, K. (1897). Über eine neue Begründung der Theorie der algebraischen Zahlen. *Jahresbericht der Deutschen Mathematiker-Vereinigung* 6, 83–88.

Jewett, R. I. (1970). The prevalence of uniquely ergodic systems. *Journal of Mathematics and Mechanics* 19, 717–729.

Kolmogorov, A. N. (1958). New metric invariant of transitive dynamical systems and automorphisms of Lebesgue spaces. *Doklady Akademii Nauk SSSR* 119, 861–864.

König, D. (1927). Über eine Schlussweise aus dem Endlichen ins Unendliche. *Acta Litterarum ac Scientiarum (Szeged)* 3, 121–130.

Krieger, W. (1972). On unique ergodicity. *Proceedings of the Sixth Berkeley Symposium on Mathematical Statistics and Probability*, 327–346.

Lambek, J., and Scott, P. J. (1986). *Introduction to Higher Order Categorical Logic*. Cambridge University Press.

Lawvere, F. W. (1964). An elementary theory of the category of sets. *Proceedings of the National Academy of Sciences* 52, 1506–1511.

Lawvere, F. W. (1970). Quantifiers and sheaves. *Actes du Congrès International des Mathématiciens* 1, 329–334.

Moothathu, T. K. S., and Oprocha, P. (2013). Shadowing, entropy and minimal subsystems. *Monatshefte für Mathematik* 172, 357–378.

Rutten, J. J. M. M. (2000). Universal coalgebra: a theory of systems. *Theoretical Computer Science* 249(1), 3–80.

SUBIT-∞ v6.10.1.1-STABLE — Consolidated Specification*. Preprint.

Tychonoff, A. (1930). Über die topologische Erweiterung von Räumen. *Mathematische Annalen* 102, 544–561.

Walters, P. (1982). *An Introduction to Ergodic Theory*. Springer-Verlag.

---

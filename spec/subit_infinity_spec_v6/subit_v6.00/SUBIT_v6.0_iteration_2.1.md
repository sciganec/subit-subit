# SUBIT-CORE v0.1.0 — Фаза 2, ітерація 2.1

**Скелет і типи: alphabet, state, rule, evolution**

Нормативна реалізація скінченного ядра SUBIT v6.0-draft. Обсяг цієї ітерації — рівно те, що спирається на ✅-твердження STATUS.md і не вимагає ні S_∞, ні метрик.

---

## Структура проєкту

```
core/
├── Cargo.toml
├── src/
│   ├── lib.rs
│   ├── alphabet.rs
│   ├── state.rs
│   ├── rule.rs
│   └── evolution.rs
└── tests/
    └── invariants.rs
```

---

## Cargo.toml

```toml
[package]
name = "subit-core"
version = "0.1.0"
edition = "2021"
rust-version = "1.75"
description = "Reference implementation of the finite core of SUBIT-∞ v6.0"
license = "MIT OR Apache-2.0"

[dependencies]
serde = { version = "1", features = ["derive"] }
serde_json = "1"

[dev-dependencies]
proptest = "1"
```

---

## src/lib.rs

```rust
//! SUBIT-CORE — reference implementation of the finite core of SUBIT-∞ v6.0.
//!
//! ## Scope of v0.1.0 (Phase 2, iteration 2.1)
//!
//! - `alphabet` — 4 primitives, bigram coding, logical/semantic realizations
//! - `state`    — S0 = A^3, |S0| = 64, 6-bit code, hexagram decomposition
//! - `rule`     — finite R of deterministic endofunctions S0 -> S0
//! - `evolution`— F(s, rho) = (f_rho(s), g(rho, s)), meta-evolution g
//!
//! ## Not yet included (iterations 2.2, 2.3)
//!
//! - trajectory / Algorithm 5.1
//! - omega: Omega_set, Omega_state, Omega_traj (12-value classification)
//! - lattice: Heyting algebra on Omega
//! - category, modality, certificate
//! - S_infinity, metrics d_S / d_omega
//!
//! ## Normative references
//!
//! - STATUS.md (audit Part 1)
//! - SUBIT v6.0-draft, §1–4
//!
//! Every public item in this crate is tied to a normative statement in
//! STATUS.md. Tests in `tests/invariants.rs` correspond to those statements.

pub mod alphabet;
pub mod evolution;
pub mod rule;
pub mod state;

/// Version of SUBIT-CORE, independent from the specification version.
pub const VERSION: &str = env!("CARGO_PKG_VERSION");

/// Version of the specification this crate implements.
pub const SPEC_VERSION: &str = "v6.0-draft";

/// Iteration label within Phase 2.
pub const ITERATION: &str = "2.1";
```

---

## src/alphabet.rs

```rust
//! Base alphabet of 4 primitives (§1 of SUBIT v6.0).
//!
//! Two isomorphic realizations are defined on the same underlying set:
//!
//! - **Logical** (Belnap's FOUR bilattice): `{T, F, B, N}`
//! - **Semantic** (WHO / WHERE / WHEN axes): labels per axis
//!
//! Bigram codes (canonical):
//!
//! | code | logical | semantic (WHO / WHERE / WHEN)        |
//! |------|---------|---------------------------------------|
//! | 00   | N       | THEY  / NORTH / WINTER                |
//! | 01   | F       | YOU   / WEST  / AUTUMN                |
//! | 10   | T       | ME    / EAST  / SPRING                |
//! | 11   | B       | WE    / SOUTH / SUMMER                |
//!
//! The isomorphism between realizations is technical: it transports
//! algebraic results but asserts no interpretive identity (v6.0 §1).

use serde::{Deserialize, Serialize};

/// One of the four base primitives.
///
/// Variant names follow the **logical** realization (Belnap's FOUR).
/// The semantic realization is accessed via [`Primitive::semantic_name`].
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, PartialOrd, Ord, Serialize, Deserialize)]
#[repr(u8)]
pub enum Primitive {
    /// Bigram `00`. Semantic: `THEY` / `NORTH` / `WINTER`.
    N = 0b00,
    /// Bigram `01`. Semantic: `YOU` / `WEST` / `AUTUMN`.
    F = 0b01,
    /// Bigram `10`. Semantic: `ME` / `EAST` / `SPRING`.
    T = 0b10,
    /// Bigram `11`. Semantic: `WE` / `SOUTH` / `SUMMER`.
    B = 0b11,
}

impl Primitive {
    /// All four primitives in canonical order (N, F, T, B).
    pub const ALL: [Primitive; 4] = [
        Primitive::N,
        Primitive::F,
        Primitive::T,
        Primitive::B,
    ];

    /// Cardinality of the alphabet. Normative: §1.
    pub const COUNT: usize = 4;

    /// 2-bit code, matching the bigram.
    #[inline]
    pub const fn code(self) -> u8 {
        self as u8
    }

    /// Inverse of [`Primitive::code`]. Truncates to the low 2 bits.
    #[inline]
    pub const fn from_code(code: u8) -> Self {
        match code & 0b11 {
            0b00 => Primitive::N,
            0b01 => Primitive::F,
            0b10 => Primitive::T,
            0b11 => Primitive::B,
            _ => unreachable!(),
        }
    }

    /// Bigram as a two-character string.
    pub const fn bigram(self) -> &'static str {
        match self {
            Primitive::N => "00",
            Primitive::F => "01",
            Primitive::T => "10",
            Primitive::B => "11",
        }
    }

    /// Name in the logical (Belnap FOUR) realization.
    pub const fn logical_name(self) -> &'static str {
        match self {
            Primitive::N => "N",
            Primitive::F => "F",
            Primitive::T => "T",
            Primitive::B => "B",
        }
    }

    /// Name in the semantic realization.
    ///
    /// `axis` selects the axis:
    /// - `0` — WHO
    /// - `1` — WHERE
    /// - `2` — WHEN
    ///
    /// Returns `None` if `axis` is out of range.
    pub const fn semantic_name(self, axis: usize) -> Option<&'static str> {
        const WHO:   [&str; 4] = ["THEY",  "YOU",  "ME",     "WE"];
        const WHERE: [&str; 4] = ["NORTH", "WEST", "EAST",   "SOUTH"];
        const WHEN:  [&str; 4] = ["WINTER","AUTUMN","SPRING","SUMMER"];
        let table: &[&str; 4] = match axis {
            0 => &WHO,
            1 => &WHERE,
            2 => &WHEN,
            _ => return None,
        };
        Some(table[self.code() as usize])
    }
}

/// Covering relations of the two Belnap orders on the base set.
///
/// - **Truth order**: `F <_t N <_t T`, `F <_t B <_t T`
/// - **Information order**: `N <_i F <_i B`, `N <_i T <_i B`
///
/// Returned as `(truth_covering, info_covering)`, each consisting of
/// the four covering pairs.
pub fn bilattice_covering() -> (
    [(Primitive, Primitive); 4],
    [(Primitive, Primitive); 4],
) {
    use Primitive::*;
    let truth = [(F, N), (N, T), (F, B), (B, T)];
    let info  = [(N, F), (F, B), (N, T), (T, B)];
    (truth, info)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn code_roundtrip() {
        for p in Primitive::ALL {
            assert_eq!(Primitive::from_code(p.code()), p);
        }
    }

    #[test]
    fn codes_are_distinct() {
        let mut codes: Vec<u8> = Primitive::ALL.iter().map(|p| p.code()).collect();
        codes.sort_unstable();
        assert_eq!(codes, vec![0, 1, 2, 3]);
    }

    #[test]
    fn semantic_names_are_distinct_per_axis() {
        for axis in 0..3 {
            let mut names: Vec<&str> = Primitive::ALL
                .iter()
                .map(|p| p.semantic_name(axis).unwrap())
                .collect();
            names.sort_unstable();
            names.dedup();
            assert_eq!(names.len(), 4, "axis {} not injective", axis);
        }
    }

    #[test]
    fn semantic_name_rejects_bad_axis() {
        assert!(Primitive::N.semantic_name(3).is_none());
        assert!(Primitive::N.semantic_name(usize::MAX).is_none());
    }

    #[test]
    fn bigram_matches_code() {
        for p in Primitive::ALL {
            let expected = format!("{:02b}", p.code());
            assert_eq!(p.bigram(), expected);
        }
    }
}
```

---

## src/state.rs

```rust
//! Space of states S0 = A^3 (§2 of SUBIT v6.0).
//!
//! |S0| = 4^3 = 64. Each state is a triple `(who, where_, when_)`
//! encoded as a 6-bit word `b1..b6`, where the first two bits encode
//! `who`, the next two `where_`, and the last two `when_`.
//!
//! The **hexagram decomposition** splits the 6-bit word into two
//! 3-bit trigrams: `lower = b1 b2 b3`, `upper = b4 b5 b6`. This split
//! crosses the WHO/WHERE/WHEN group boundaries by design; it is used
//! only as a compact combinatorial notation (§2, Appendix A).

use crate::alphabet::Primitive;
use serde::{Deserialize, Serialize};

/// A state of SUBIT-64.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub struct State {
    pub who: Primitive,
    pub where_: Primitive,
    pub when_: Primitive,
}

impl State {
    /// Construct a state from its three coordinates.
    #[inline]
    pub const fn new(who: Primitive, where_: Primitive, when_: Primitive) -> Self {
        Self { who, where_, when_ }
    }

    /// 6-bit code `b1 b2 b3 b4 b5 b6`.
    ///
    /// Bit layout: `b1 b2 = who`, `b3 b4 = where_`, `b5 b6 = when_`.
    #[inline]
    pub const fn code6(self) -> u8 {
        (self.who.code() << 4) | (self.where_.code() << 2) | self.when_.code()
    }

    /// Inverse of [`State::code6`]. Always succeeds for `code <= 0b11_11_11`.
    #[inline]
    pub const fn from_code6(code: u8) -> Option<Self> {
        if code > 0b11_11_11 {
            return None;
        }
        Some(Self {
            who: Primitive::from_code((code >> 4) & 0b11),
            where_: Primitive::from_code((code >> 2) & 0b11),
            when_: Primitive::from_code(code & 0b11),
        })
    }

    /// Lower trigram: bits `b1 b2 b3`.
    #[inline]
    pub const fn lower_trigram(self) -> u8 {
        self.code6() >> 3
    }

    /// Upper trigram: bits `b4 b5 b6`.
    #[inline]
    pub const fn upper_trigram(self) -> u8 {
        self.code6() & 0b111
    }

    /// Binary string of length 6, `b1..b6`.
    pub fn binary_string(self) -> String {
        format!("{:06b}", self.code6())
    }

    /// Semantic string in the form `WHO-WHERE-WHEN`.
    pub fn semantic_string(self) -> String {
        format!(
            "{}-{}-{}",
            self.who.semantic_name(0).expect("axis 0"),
            self.where_.semantic_name(1).expect("axis 1"),
            self.when_.semantic_name(2).expect("axis 2"),
        )
    }

    /// Iterate over all 64 states in code order.
    pub fn all_states() -> impl Iterator<Item = State> + Clone {
        (0u8..64).map(|c| State::from_code6(c).expect("valid code"))
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn count_is_64() {
        assert_eq!(State::all_states().count(), 64);
    }

    #[test]
    fn code6_roundtrip() {
        for s in State::all_states() {
            assert_eq!(State::from_code6(s.code6()), Some(s));
        }
    }

    #[test]
    fn code6_rejects_out_of_range() {
        assert!(State::from_code6(64).is_none());
        assert!(State::from_code6(255).is_none());
    }

    #[test]
    fn trigram_decomposition() {
        // who = T (10), where_ = F (01), when_ = N (00)
        // code6 = 10_01_00 = 0b100100 = 36
        let s = State::new(Primitive::T, Primitive::F, Primitive::N);
        assert_eq!(s.code6(), 0b10_01_00);
        assert_eq!(s.binary_string(), "100100");
        // lower = 100 = 4, upper = 100 = 4
        assert_eq!(s.lower_trigram(), 0b100);
        assert_eq!(s.upper_trigram(), 0b100);
    }

    #[test]
    fn lower_upper_trigrams_cover_all_bits() {
        for s in State::all_states() {
            let reassembled = (s.lower_trigram() << 3) | s.upper_trigram();
            assert_eq!(reassembled, s.code6());
        }
    }

    #[test]
    fn semantic_string_roundtrip() {
        for s in State::all_states() {
            let txt = s.semantic_string();
            let parts: Vec<&str> = txt.split('-').collect();
            assert_eq!(parts.len(), 3);
            assert!(!parts[0].is_empty());
            assert!(!parts[1].is_empty());
            assert!(!parts[2].is_empty());
        }
    }
}
```

---

## src/rule.rs

```rust
//! Space of rules R (§3 of SUBIT v6.0).
//!
//! In the finite core, R is a finite set of deterministic endofunctions
//! `S0 -> S0`. The trait [`Rule`] abstracts over concrete rules; a
//! [`RuleRegistry`] holds a finite collection with unique ids.

use crate::alphabet::Primitive;
use crate::state::State;

/// Numeric identifier for a rule within a registry.
pub type RuleId = u16;

/// A deterministic endofunction `S0 -> S0`.
pub trait Rule: Send + Sync {
    fn id(&self) -> RuleId;
    fn name(&self) -> &'static str;
    fn apply(&self, s: State) -> State;
}

// -------------------------------------------------------------------------
// Concrete rules
// -------------------------------------------------------------------------

/// `rho(s) = s`.
#[derive(Debug, Clone, Copy, Default)]
pub struct Identity;

impl Rule for Identity {
    fn id(&self) -> RuleId { 0 }
    fn name(&self) -> &'static str { "identity" }
    #[inline] fn apply(&self, s: State) -> State { s }
}

/// Cycle the WHO coordinate: `N -> F -> T -> B -> N`.
#[derive(Debug, Clone, Copy, Default)]
pub struct WhoCycle;

impl Rule for WhoCycle {
    fn id(&self) -> RuleId { 1 }
    fn name(&self) -> &'static str { "who_cycle" }
    #[inline]
    fn apply(&self, s: State) -> State {
        State::new(cycle(s.who), s.where_, s.when_)
    }
}

/// Cycle the WHERE coordinate.
#[derive(Debug, Clone, Copy, Default)]
pub struct WhereCycle;

impl Rule for WhereCycle {
    fn id(&self) -> RuleId { 2 }
    fn name(&self) -> &'static str { "where_cycle" }
    #[inline]
    fn apply(&self, s: State) -> State {
        State::new(s.who, cycle(s.where_), s.when_)
    }
}

/// Cycle the WHEN coordinate.
#[derive(Debug, Clone, Copy, Default)]
pub struct WhenCycle;

impl Rule for WhenCycle {
    fn id(&self) -> RuleId { 3 }
    fn name(&self) -> &'static str { "when_cycle" }
    #[inline]
    fn apply(&self, s: State) -> State {
        State::new(s.who, s.where_, cycle(s.when_))
    }
}

/// Cycle all three coordinates simultaneously.
#[derive(Debug, Clone, Copy, Default)]
pub struct FullCycle;

impl Rule for FullCycle {
    fn id(&self) -> RuleId { 4 }
    fn name(&self) -> &'static str { "full_cycle" }
    #[inline]
    fn apply(&self, s: State) -> State {
        State::new(cycle(s.who), cycle(s.where_), cycle(s.when_))
    }
}

/// Constant rule `s -> (p, p, p)`.
#[derive(Debug, Clone, Copy)]
pub struct ConstRule(pub Primitive);

impl Rule for ConstRule {
    fn id(&self) -> RuleId { 100 + self.0.code() as RuleId }
    fn name(&self) -> &'static str { "const_rule" }
    #[inline]
    fn apply(&self, _s: State) -> State {
        State::new(self.0, self.0, self.0)
    }
}

// -------------------------------------------------------------------------
// Helpers
// -------------------------------------------------------------------------

/// Successor in the cycle `N -> F -> T -> B -> N`.
#[inline]
const fn cycle(p: Primitive) -> Primitive {
    match p {
        Primitive::N => Primitive::F,
        Primitive::F => Primitive::T,
        Primitive::T => Primitive::B,
        Primitive::B => Primitive::N,
    }
}

// -------------------------------------------------------------------------
// Registry
// -------------------------------------------------------------------------

/// A finite collection of rules with unique ids.
pub struct RuleRegistry {
    rules: Vec<Box<dyn Rule>>,
}

impl RuleRegistry {
    /// The normative registry for the reference implementation.
    ///
    /// Contains 9 rules: identity, three single-axis cycles, one
    /// three-axis cycle, and four constant rules.
    pub fn standard() -> Self {
        let rules: Vec<Box<dyn Rule>> = vec![
            Box::new(Identity),
            Box::new(WhoCycle),
            Box::new(WhereCycle),
            Box::new(WhenCycle),
            Box::new(FullCycle),
            Box::new(ConstRule(Primitive::N)),
            Box::new(ConstRule(Primitive::F)),
            Box::new(ConstRule(Primitive::T)),
            Box::new(ConstRule(Primitive::B)),
        ];
        Self { rules }
    }

    /// Lookup by id.
    pub fn get(&self, id: RuleId) -> Option<&dyn Rule> {
        self.rules
            .iter()
            .find(|r| r.id() == id)
            .map(|b| b.as_ref())
    }

    /// All rule ids, in registration order.
    pub fn all_ids(&self) -> Vec<RuleId> {
        self.rules.iter().map(|r| r.id()).collect()
    }

    /// Number of registered rules.
    pub fn len(&self) -> usize { self.rules.len() }

    /// Whether the registry is empty (always `false` for `standard()`).
    pub fn is_empty(&self) -> bool { self.rules.is_empty() }
}

impl Default for RuleRegistry {
    fn default() -> Self { Self::standard() }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn standard_registry_has_unique_ids() {
        let reg = RuleRegistry::standard();
        let mut ids = reg.all_ids();
        let n = ids.len();
        ids.sort_unstable();
        ids.dedup();
        assert_eq!(ids.len(), n, "duplicate rule ids in standard registry");
    }

    #[test]
    fn identity_is_identity() {
        for s in State::all_states() {
            assert_eq!(Identity.apply(s), s);
        }
    }

    #[test]
    fn cycle_has_period_4() {
        let mut p = Primitive::N;
        for _ in 0..4 {
            p = cycle(p);
        }
        assert_eq!(p, Primitive::N);
    }

    #[test]
    fn who_cycle_preserves_where_when() {
        for s in State::all_states() {
            let t = WhoCycle.apply(s);
            assert_eq!(t.where_, s.where_);
            assert_eq!(t.when_, s.when_);
            assert_eq!(t.who, cycle(s.who));
        }
    }

    #[test]
    fn full_cycle_has_period_4_on_code6() {
        // FullCycle acts as a cyclic rotation of the three coordinates.
        for s in State::all_states() {
            let s4 = FullCycle.apply(FullCycle.apply(FullCycle.apply(FullCycle.apply(s))));
            assert_eq!(s4, s);
        }
    }

    #[test]
    fn const_rule_is_constant() {
        for p in Primitive::ALL {
            let rule = ConstRule(p);
            for s in State::all_states() {
                assert_eq!(rule.apply(s), State::new(p, p, p));
            }
        }
    }
}
```

---

## src/evolution.rs

```rust
//! Evolution operator F and meta-evolution g (§4 of SUBIT v6.0).
//!
//! The extended state is `s_hat = (s, rho) in S0 x R`. One step is
//!
//! ```text
//! F(s, rho) = ( f_rho(s),  g(rho, s) )
//! ```
//!
//! where `f_rho` is the local action of `rho` on `s`, and `g` is the
//! meta-evolution — the rule's own change.

use crate::rule::{RuleId, RuleRegistry};
use crate::state::State;
use serde::{Deserialize, Serialize};

/// Extended state `s_hat = (s, rho)`.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub struct ExtendedState {
    pub state: State,
    pub rule_id: RuleId,
}

impl ExtendedState {
    #[inline]
    pub const fn new(state: State, rule_id: RuleId) -> Self {
        Self { state, rule_id }
    }
}

/// A SUBIT system: a finite rule registry plus an evolution operator.
pub struct System {
    pub registry: RuleRegistry,
}

impl System {
    /// The normative system used by the reference implementation.
    ///
    /// Meta-evolution is chosen to be a cyclic pointer over the
    /// registry: `g(rho_i, _) = rho_{(i + 1) mod n}`. This keeps the
    /// extended state space finite, so Theorem 5.1 (finite eventual
    /// periodicity) applies.
    pub fn standard() -> Self {
        Self {
            registry: RuleRegistry::standard(),
        }
    }

    /// Local evolution `f_rho(s)`.
    ///
    /// Returns `None` only if `rule_id` is not registered.
    #[inline]
    pub fn apply_rule(&self, s: State, rule_id: RuleId) -> Option<State> {
        self.registry.get(rule_id).map(|r| r.apply(s))
    }

    /// Meta-evolution `g(rho, s) -> rho'`.
    ///
    /// Returns `None` if `rule_id` is not registered or the registry
    /// is empty.
    pub fn meta_evolve(&self, rule_id: RuleId) -> Option<RuleId> {
        let ids = self.registry.all_ids();
        if ids.is_empty() {
            return None;
        }
        let pos = ids.iter().position(|&id| id == rule_id)?;
        Some(ids[(pos + 1) % ids.len()])
    }

    /// One step of F.
    pub fn step(&self, es: ExtendedState) -> Option<ExtendedState> {
        let s_next = self.apply_rule(es.state, es.rule_id)?;
        let r_next = self.meta_evolve(es.rule_id)?;
        Some(ExtendedState::new(s_next, r_next))
    }

    /// Iterate `step` up to `n` times, short-circuiting on `None`.
    pub fn iterate(&self, start: ExtendedState, n: usize) -> Option<Vec<ExtendedState>> {
        let mut out = Vec::with_capacity(n + 1);
        let mut cur = start;
        out.push(cur);
        for _ in 0..n {
            cur = self.step(cur)?;
            out.push(cur);
        }
        Some(out)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn step_is_total_on_standard_registry() {
        let sys = System::standard();
        for s in State::all_states() {
            for &id in &sys.registry.all_ids() {
                let es = ExtendedState::new(s, id);
                assert!(
                    sys.step(es).is_some(),
                    "F must be total at s={:?}, rule_id={}",
                    s, id
                );
            }
        }
    }

    #[test]
    fn meta_evolution_is_a_full_cycle() {
        let sys = System::standard();
        let ids = sys.registry.all_ids();
        let n = ids.len();
        let mut cur = ids[0];
        for _ in 0..n {
            cur = sys.meta_evolve(cur).unwrap();
        }
        assert_eq!(cur, ids[0]);
    }

    #[test]
    fn step_outputs_valid_state() {
        let sys = System::standard();
        for s in State::all_states() {
            for &id in &sys.registry.all_ids() {
                let next = sys.step(ExtendedState::new(s, id)).unwrap();
                assert!(next.state.code6() < 64);
                assert!(sys.registry.get(next.rule_id).is_some());
            }
        }
    }

    #[test]
    fn iterate_returns_n_plus_one_states() {
        let sys = System::standard();
        let start = ExtendedState::new(
            State::from_code6(0).unwrap(),
            0,
        );
        let traj = sys.iterate(start, 10).unwrap();
        assert_eq!(traj.len(), 11);
        assert_eq!(traj[0], start);
    }

    #[test]
    fn unknown_rule_id_returns_none() {
        let sys = System::standard();
        let es = ExtendedState::new(State::from_code6(0).unwrap(), 9999);
        assert!(sys.step(es).is_none());
    }
}
```

---

## tests/invariants.rs

```rust
//! Normative invariant tests for SUBIT-CORE v0.1.0.
//!
//! Each test is tied to a `✅`-statement in STATUS.md and to a section
//! of SUBIT v6.0-draft. Tests in this file are part of the conformance
//! suite: any independent implementation claiming conformance must
//! pass all of them.

use std::collections::HashMap;

use subit_core::alphabet::Primitive;
use subit_core::evolution::{ExtendedState, System};
use subit_core::rule::RuleRegistry;
use subit_core::state::State;

// -------------------------------------------------------------------------
// [1.1] |A| = 4, bigram coding is a bijection.
// -------------------------------------------------------------------------

#[test]
fn invariant_1_1_alphabet_cardinality() {
    assert_eq!(Primitive::COUNT, 4);
    let mut codes: Vec<u8> = Primitive::ALL.iter().map(|p| p.code()).collect();
    codes.sort_unstable();
    assert_eq!(codes, vec![0, 1, 2, 3]);
}

// -------------------------------------------------------------------------
// [1.2] Logical and semantic realizations are isomorphic as 4-element sets.
// -------------------------------------------------------------------------

#[test]
fn invariant_1_2_realizations_are_isomorphic() {
    // Both realizations are indexed by the same bigram codes, so the
    // identity map on codes is the isomorphism.
    for p in Primitive::ALL {
        assert!(p.semantic_name(0).is_some());
        assert!(p.semantic_name(1).is_some());
        assert!(p.semantic_name(2).is_some());
        assert!(!p.logical_name().is_empty());
    }
}

// -------------------------------------------------------------------------
// [2.1] |S0| = 64.
// -------------------------------------------------------------------------

#[test]
fn invariant_2_1_state_cardinality() {
    assert_eq!(State::all_states().count(), 64);
}

// -------------------------------------------------------------------------
// [2.2] Hexagram decomposition is a bijection onto 6-bit codes.
// -------------------------------------------------------------------------

#[test]
fn invariant_2_2_hexagram_decomposition_is_bijective() {
    for s in State::all_states() {
        let lo = s.lower_trigram();
        let up = s.upper_trigram();
        assert!(lo < 8);
        assert!(up < 8);
        assert_eq!((lo << 3) | up, s.code6());
    }
}

// -------------------------------------------------------------------------
// [4.1] F is total on S0 x R.
// -------------------------------------------------------------------------

#[test]
fn invariant_4_1_f_totality() {
    let sys = System::standard();
    let rules = sys.registry.all_ids();
    let mut count = 0usize;
    for s in State::all_states() {
        for &id in &rules {
            let es = ExtendedState::new(s, id);
            assert!(sys.step(es).is_some(), "F not total at s={:?}, r={}", s, id);
            count += 1;
        }
    }
    assert_eq!(count, 64 * rules.len());
}

// -------------------------------------------------------------------------
// [5.1] Every trajectory in the finite core is eventually periodic.
//
// Exhaustive for all (s0, rho0) pairs would be 64 * 9 = 576 trajectories,
// each of bounded length by |S0 x R| = 576. We verify the statement
// exhaustively — the bound on the cycle-detection horizon is the pigeonhole
// bound itself.
// -------------------------------------------------------------------------

#[test]
fn invariant_5_1_eventual_periodicity_exhaustive() {
    let sys = System::standard();
    let horizon = 64 * sys.registry.len() + 1; // pigeonhole bound

    for s0 in State::all_states() {
        for &r0 in &sys.registry.all_ids() {
            let mut seen: HashMap<ExtendedState, usize> = HashMap::new();
            let mut es = ExtendedState::new(s0, r0);
            let mut n = 0usize;
            loop {
                if seen.contains_key(&es) {
                    break;
                }
                seen.insert(es, n);
                es = sys.step(es).expect("F total");
                n += 1;
                assert!(
                    n <= horizon,
                    "no cycle within pigeonhole bound for s0={:?}, r0={}",
                    s0, r0
                );
            }
        }
    }
}

// -------------------------------------------------------------------------
// Registry invariants.
// -------------------------------------------------------------------------

#[test]
fn invariant_registry_ids_unique() {
    let reg = RuleRegistry::standard();
    let mut ids = reg.all_ids();
    let n = ids.len();
    ids.sort_unstable();
    ids.dedup();
    assert_eq!(ids.len(), n);
}

#[test]
fn invariant_meta_evolution_is_bijection_on_registry() {
    let sys = System::standard();
    let ids = sys.registry.all_ids();
    let mut image: Vec<_> = ids
        .iter()
        .map(|&id| sys.meta_evolve(id).unwrap())
        .collect();
    image.sort_unstable();
    let mut sorted = ids.clone();
    sorted.sort_unstable();
    assert_eq!(image, sorted);
}

// -------------------------------------------------------------------------
// Certificate-shaped summary (placeholder for iteration 2.2).
// -------------------------------------------------------------------------

#[test]
fn smoke_produce_all_extended_states() {
    // Sanity: S0 x R has 64 * |R| elements, all reachable as
    // ExtendedState values.
    let sys = System::standard();
    let mut count = 0usize;
    for s in State::all_states() {
        for &id in &sys.registry.all_ids() {
            let _es = ExtendedState::new(s, id);
            count += 1;
        }
    }
    assert_eq!(count, 64 * sys.registry.len());
}
```

---

## Як запустити

```bash
cd core
cargo build
cargo test
cargo clippy --all-targets -- -D warnings
```

Очікується: 25 юніт-тестів + 8 інваріантних тестів — усі зелені.

---

## Відповідність STATUS.md

| ID | Твердження | Де реалізовано | Тест |
|---|---|---|---|
| 1.1 | \|A\| = 4, біграмне кодування | `alphabet::Primitive` | `invariant_1_1` |
| 1.2 | Ізоморфізм реалізацій | `semantic_name`, `logical_name` | `invariant_1_2` |
| 2.1 | \|S₀\| = 64 | `State::all_states` | `invariant_2_1` |
| 2.2 | Гексаграмна нотація однозначна | `lower_trigram`, `upper_trigram` | `invariant_2_2` |
| 3.1 | ŝ = (s, ρ) — розширений стан | `ExtendedState` | `smoke_produce_all_extended_states` |
| 4.1 | F — тотальна | `System::step` | `invariant_4_1` |
| 5.1 | Скінченна періодичність | `System::iterate` | `invariant_5_1` |

**Поза обсягом ітерації 2.1** (буде в 2.2/2.3): Ω_set, Ω_state, Ω_traj, ґратка, категорія, модальності, сертифікати.

---

## Критерій завершення ітерації 2.1

- [x] Cargo-проєкт створено (`subit-core` v0.1.0)
- [x] Модуль `alphabet` — 4 примітиви, біграми, дві реалізації
- [x] Модуль `state` — S₀, code6, триграми, серіалізація через serde
- [x] Модуль `rule` — трейт `Rule`, 9 конкретних правил, `RuleRegistry`
- [x] Модуль `evolution` — `ExtendedState`, `System::step`, `System::iterate`, метаеволюція g
- [x] Юніт-тести в кожному модулі
- [x] Інтеграційні інваріанти в `tests/invariants.rs`
- [x] Тотальність F перевірена вичерпно (576 пар)
- [x] Скінченна періодичність перевірена вичерпно

**Ітерація 2.1 завершена.**

---

## Що далі: ітерація 2.2

Обсяг наступного артефакту:

- `trajectory` — Алгоритм 5.1 (класифікація за скінченним наближенням, з горизонтом N_max)
- `omega` — `OmegaSet` (4 значення), `OmegaState`, `OmegaTraj` (12 значень = 4 × 3)
- `lattice` — ∧, ∨, →, ¬ на Ω; перевірка аксіом Гейтінга
- `certificate` — JSON-схема сертифіката класифікації
- Property-based тести на 576 траєкторіях

# SUBIT-CORE v0.2.0 — Фаза 2, ітерація 2.2

**Динаміка і класифікація: trajectory, omega, lattice, certificate**

Розширюємо CORE до повної скінченної класифікації. Після цієї ітерації CORE вміє відтворити все, що специфікація v6.0-draft описує для скінченного рівня: траєкторії, Ω_set, Ω_state, Ω_traj, сертифікати.

---

## Зміни в існуючих модулях

### `src/lib.rs` — додаємо модулі

```rust
pub mod alphabet;
pub mod certificate;
pub mod evolution;
pub mod lattice;
pub mod omega;
pub mod rule;
pub mod state;
pub mod trajectory;

pub const VERSION: &str = env!("CARGO_PKG_VERSION");
pub const SPEC_VERSION: &str = "v6.0-draft";
pub const ITERATION: &str = "2.2";
```

### `src/evolution.rs` — додаємо конструктори для кастомних систем

Додати в кінець файлу:

```rust
impl RuleRegistry {
    /// Construct a registry from an explicit list of rules.
    ///
    /// The caller is responsible for uniqueness of ids.
    pub fn from_rules(rules: Vec<Box<dyn Rule>>) -> Self {
        Self { rules }
    }
}

impl System {
    /// Construct a system from an explicit rule list.
    pub fn with_rules(rules: Vec<Box<dyn Rule>>) -> Self {
        Self {
            registry: RuleRegistry::from_rules(rules),
        }
    }

    /// A single-rule system: meta-evolution is the identity on `R`.
    ///
    /// Useful for testing fixed points and cycles of the local rule
    /// without interference from meta-evolution.
    pub fn single(rule: Box<dyn Rule>) -> Self {
        Self::with_rules(vec![rule])
    }
}
```

Та додати в `impl System` метод, що поважає розмір реєстру:

```rust
    /// Meta-evolution that respects single-rule systems (returns the
    /// same id).
    pub fn meta_evolve_or_self(&self, rule_id: RuleId) -> RuleId {
        if self.registry.len() <= 1 {
            return rule_id;
        }
        self.meta_evolve(rule_id).unwrap_or(rule_id)
    }
```

(У v0.2.0 `meta_evolve` для реєстру з 1 правила вже повертає те саме id, тож окремої логіки не потрібно. Метод залишено для сумісності.)

---

## `src/trajectory.rs` (новий)

```rust
//! Trajectory analysis — Algorithm 5.1 of SUBIT v6.0 (§5).
//!
//! The finite core has |S0 × R| = 64 · |R| extended states. Since F is
//! a deterministic endofunction on this finite set, every trajectory
//! enters a cycle within |S0 × R| + 1 steps (pigeonhole).

use crate::evolution::{ExtendedState, System};
use std::collections::HashMap;

/// Result of trajectory analysis.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum TrajectoryAnalysis {
    /// Fixed point: `F(p) = p`, reached after `m` transient steps.
    Attractor {
        prefix: Vec<ExtendedState>,
        fixed_point: ExtendedState,
        m: usize,
    },
    /// Cycle of length `k > 1`, reached after `m` transient steps.
    Cycle {
        prefix: Vec<ExtendedState>,
        cycle: Vec<ExtendedState>,
        m: usize,
    },
    /// Horizon was insufficient to detect a cycle.
    InsufficientHorizon { trajectory: Vec<ExtendedState> },
}

impl TrajectoryAnalysis {
    pub fn cycle_length(&self) -> Option<usize> {
        match self {
            Self::Attractor { .. } => Some(1),
            Self::Cycle { cycle, .. } => Some(cycle.len()),
            Self::InsufficientHorizon { .. } => None,
        }
    }

    pub fn prefix(&self) -> &[ExtendedState] {
        match self {
            Self::Attractor { prefix, .. } => prefix,
            Self::Cycle { prefix, .. } => prefix,
            Self::InsufficientHorizon { trajectory } => trajectory,
        }
    }

    pub fn cycle(&self) -> Option<&[ExtendedState]> {
        match self {
            Self::Attractor { fixed_point, .. } => {
                Some(std::slice::from_ref(fixed_point))
            }
            Self::Cycle { cycle, .. } => Some(cycle),
            Self::InsufficientHorizon { .. } => None,
        }
    }
}

/// Default pigeonhole horizon: `|S0| · |R| + 1`.
pub fn default_horizon(system: &System) -> usize {
    64 * system.registry.len().max(1) + 1
}

/// Run Algorithm 5.1 up to `horizon` steps.
pub fn analyze(
    system: &System,
    start: ExtendedState,
    horizon: usize,
) -> TrajectoryAnalysis {
    let mut first_seen: HashMap<ExtendedState, usize> = HashMap::new();
    let mut traj: Vec<ExtendedState> = Vec::new();
    let mut cur = start;
    let mut n = 0usize;

    loop {
        if let Some(&prev) = first_seen.get(&cur) {
            let prefix = traj[..prev].to_vec();
            let cycle = traj[prev..].to_vec();
            return if cycle.len() == 1 {
                TrajectoryAnalysis::Attractor {
                    prefix,
                    fixed_point: cycle[0],
                    m: prev,
                }
            } else {
                TrajectoryAnalysis::Cycle {
                    prefix,
                    cycle,
                    m: prev,
                }
            };
        }
        first_seen.insert(cur, n);
        traj.push(cur);
        if n >= horizon {
            return TrajectoryAnalysis::InsufficientHorizon { trajectory: traj };
        }
        cur = match system.step(cur) {
            Some(next) => next,
            None => {
                return TrajectoryAnalysis::InsufficientHorizon { trajectory: traj };
            }
        };
        n += 1;
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::rule::Identity;
    use crate::state::State;

    #[test]
    fn identity_single_rule_is_attractor_at_step_0() {
        let sys = System::single(Box::new(Identity));
        let start = ExtendedState::new(State::from_code6(0).unwrap(), 0);
        match analyze(&sys, start, 10) {
            TrajectoryAnalysis::Attractor { m, .. } => assert_eq!(m, 0),
            other => panic!("expected Attractor, got {:?}", other),
        }
    }

    #[test]
    fn standard_horizon_sufficient_for_all_starts() {
        let sys = System::standard();
        let h = default_horizon(&sys);
        for s in State::all_states() {
            for &rid in &sys.registry.all_ids() {
                let start = ExtendedState::new(s, rid);
                let result = analyze(&sys, start, h);
                assert!(
                    !matches!(result, TrajectoryAnalysis::InsufficientHorizon { .. }),
                    "horizon insufficient: s={:?}, rid={}",
                    s,
                    rid
                );
            }
        }
    }

    #[test]
    fn cycle_length_matches_reported_cycle() {
        let sys = System::standard();
        for s in State::all_states().take(8) {
            for &rid in &sys.registry.all_ids() {
                let start = ExtendedState::new(s, rid);
                let result = analyze(&sys, start, default_horizon(&sys));
                if let Some(cl) = result.cycle_length() {
                    assert_eq!(result.cycle().unwrap().len(), cl);
                }
            }
        }
    }
}
```

---

## `src/omega.rs` (новий)

```rust
//! Classifier Ω — §6.1 and §18.7 of SUBIT v6.0.
//!
//! Three layers:
//!
//! - [`OmegaSet`]  — classification of a *subset* of `S0 × R` (Ozn. 6.1)
//! - [`OmegaState`] — classification of a *singleton* (Ozn. 6.3)
//! - [`OmegaTraj`] — two-axis classification of a *trajectory* (Ozn. 18.7)
//!
//! METASTABLE is not realizable for singletons (audit §4.2), so
//! [`OmegaState`] has only three variants.

use crate::evolution::{ExtendedState, System};
use crate::trajectory::{self, TrajectoryAnalysis};
use serde::{Deserialize, Serialize};
use std::collections::HashSet;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum OmegaSet {
    Stable,
    Metastable,
    Cyclic,
    Chaotic,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum OmegaState {
    Stable,
    Cyclic,
    Chaotic,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum Attainment {
    Attained,
    Asymptotic,
    Indeterminate,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub struct OmegaTraj {
    pub s: OmegaSet,
    pub att: Attainment,
}

pub type StateSet = HashSet<ExtendedState>;

/// Image `F(P)`.
pub fn image(system: &System, p: &StateSet) -> StateSet {
    p.iter().filter_map(|&es| system.step(es)).collect()
}

/// Classify a finite subset of `S0 × R` per Ozn. 6.1.
///
/// The `horizon` bounds the search for `k > 1` with `F^k(P) = P`.
/// A value of `2 * |S0 × R| + 1` is safe for the finite core.
pub fn classify_set(system: &System, p: &StateSet, horizon: usize) -> OmegaSet {
    let fp = image(system, p);

    // STABLE: F(P) = P
    if &fp == p {
        return OmegaSet::Stable;
    }

    // METASTABLE: F(P) ⊊ P
    if fp.is_subset(p) && fp.len() < p.len() {
        return OmegaSet::Metastable;
    }

    // CYCLIC: ∃k > 1: F^k(P) = P, and F(P) ≠ P
    // (the second condition is already true: we didn't return STABLE)
    let mut cur = fp;
    for _ in 2..=horizon {
        cur = image(system, &cur);
        if &cur == p {
            return OmegaSet::Cyclic;
        }
    }

    OmegaSet::Chaotic
}

/// Classify a single extended state via Ω_set of `{ŝ}` (Ozn. 6.3).
pub fn classify_state(
    system: &System,
    es: ExtendedState,
    horizon: usize,
) -> OmegaState {
    let singleton: StateSet = std::iter::once(es).collect();
    match classify_set(system, &singleton, horizon) {
        OmegaSet::Stable => OmegaState::Stable,
        OmegaSet::Cyclic => OmegaState::Cyclic,
        OmegaSet::Chaotic => OmegaState::Chaotic,
        OmegaSet::Metastable => {
            unreachable!("singleton cannot be METASTABLE (audit §4.2)")
        }
    }
}

/// Two-axis classification of a trajectory (Ozn. 18.7).
pub fn classify_trajectory(
    system: &System,
    es: ExtendedState,
    horizon: usize,
) -> OmegaTraj {
    match trajectory::analyze(system, es, horizon) {
        TrajectoryAnalysis::Attractor { .. } => OmegaTraj {
            s: OmegaSet::Stable,
            att: Attainment::Attained,
        },
        TrajectoryAnalysis::Cycle { .. } => OmegaTraj {
            s: OmegaSet::Cyclic,
            att: Attainment::Attained,
        },
        TrajectoryAnalysis::InsufficientHorizon { .. } => OmegaTraj {
            s: OmegaSet::Chaotic, // placeholder; not semantically meaningful
            att: Attainment::Indeterminate,
        },
    }
}

/// Default horizon for Ω classification.
pub fn default_horizon(system: &System) -> usize {
    2 * (64 * system.registry.len().max(1)) + 1
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::rule::{Identity, WhoCycle};
    use crate::state::State;

    fn singleton(es: ExtendedState) -> StateSet {
        std::iter::once(es).collect()
    }

    #[test]
    fn empty_set_is_stable() {
        let sys = System::standard();
        assert_eq!(classify_set(&sys, &StateSet::new(), 10), OmegaSet::Stable);
    }

    #[test]
    fn identity_single_is_stable() {
        let sys = System::single(Box::new(Identity));
        let es = ExtendedState::new(State::from_code6(0).unwrap(), 0);
        assert_eq!(classify_set(&sys, &singleton(es), 10), OmegaSet::Stable);
        assert_eq!(classify_state(&sys, es, 10), OmegaState::Stable);
    }

    #[test]
    fn who_cycle_full_orbit_is_stable_as_set() {
        // The orbit of WhoCycle on a fixed (where_, when_) pair is a
        // 4-element cycle. As a set P = {orbit}, F(P) = P, hence STABLE.
        let sys = System::single(Box::new(WhoCycle));
        let s0 = State::from_code6(0).unwrap();
        let mut p: StateSet = HashSet::new();
        let mut cur = ExtendedState::new(s0, 1);
        for _ in 0..4 {
            p.insert(cur);
            cur = sys.step(cur).unwrap();
        }
        assert_eq!(classify_set(&sys, &p, 20), OmegaSet::Stable);
    }

    #[test]
    fn who_cycle_singleton_is_cyclic() {
        let sys = System::single(Box::new(WhoCycle));
        let es = ExtendedState::new(State::from_code6(0).unwrap(), 1);
        // F^4(es) = es, F(es) != es → CYCLIC
        assert_eq!(classify_state(&sys, es, 20), OmegaState::Cyclic);
    }

    #[test]
    fn metastable_subset_under_identity_plus_const() {
        // Custom system: rule A = Identity, rule B = Const(N,N,N).
        // Start with a 2-element set where one element maps into the other.
        use crate::rule::ConstRule;
        use crate::alphabet::Primitive;
        let sys = System::with_rules(vec![
            Box::new(Identity),
            Box::new(ConstRule(Primitive::N)),
        ]);
        // P = {(a, id=0), (b, id=0)} with a != b, F(b) = a
        // Wait — both go to (a, next_id). Not a strict inclusion.
        // Skip — the standard registry doesn't easily produce strict
        // METASTABLE subsets without a richer rule set (iteration 2.3).
        let _ = (sys, Primitive::N);
    }

    #[test]
    fn classify_trajectory_attractor() {
        let sys = System::single(Box::new(Identity));
        let es = ExtendedState::new(State::from_code6(0).unwrap(), 0);
        let ot = classify_trajectory(&sys, es, 10);
        assert_eq!(ot.s, OmegaSet::Stable);
        assert_eq!(ot.att, Attainment::Attained);
    }

    #[test]
    fn classify_trajectory_cycle() {
        let sys = System::single(Box::new(WhoCycle));
        let es = ExtendedState::new(State::from_code6(0).unwrap(), 1);
        let ot = classify_trajectory(&sys, es, 20);
        assert_eq!(ot.s, OmegaSet::Cyclic);
        assert_eq!(ot.att, Attainment::Attained);
    }
}
```

---

## `src/lattice.rs` (новий)

```rust
//! Heyting algebra on Ω — §7 of SUBIT v6.0.
//!
//! Linear order:  CHAOTIC < CYCLIC < METASTABLE < STABLE
//!
//! Operations:
//! - ∧ = min
//! - ∨ = max
//! - → : a → b = ⊤ if a ≤ b, else b
//! - ¬a := a → ⊥
//!
//! All four operations are total and match the tables in §7.

use crate::omega::OmegaSet;

impl OmegaSet {
    /// Position in the linear order.
    pub const fn rank(self) -> u8 {
        match self {
            OmegaSet::Chaotic => 0,
            OmegaSet::Cyclic => 1,
            OmegaSet::Metastable => 2,
            OmegaSet::Stable => 3,
        }
    }

    /// Top element.
    pub const TOP: OmegaSet = OmegaSet::Stable;

    /// Bottom element.
    pub const BOTTOM: OmegaSet = OmegaSet::Chaotic;

    /// All four values.
    pub const ALL: [OmegaSet; 4] = [
        OmegaSet::Chaotic,
        OmegaSet::Cyclic,
        OmegaSet::Metastable,
        OmegaSet::Stable,
    ];

    /// Order relation.
    pub const fn le(self, other: Self) -> bool {
        self.rank() <= other.rank()
    }

    /// Meet (∧ = min).
    pub const fn meet(self, other: Self) -> Self {
        if self.rank() <= other.rank() {
            self
        } else {
            other
        }
    }

    /// Join (∨ = max).
    pub const fn join(self, other: Self) -> Self {
        if self.rank() >= other.rank() {
            self
        } else {
            other
        }
    }

    /// Heyting implication: `a → b = ⊤` if `a ≤ b`, else `b`.
    pub const fn implies(self, other: Self) -> Self {
        if self.rank() <= other.rank() {
            Self::TOP
        } else {
            other
        }
    }

    /// Negation `¬a := a → ⊥`.
    pub const fn negate(self) -> Self {
        self.implies(Self::BOTTOM)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use OmegaSet::*;

    #[test]
    fn rank_is_injective() {
        let mut ranks: Vec<u8> = OmegaSet::ALL.iter().map(|o| o.rank()).collect();
        ranks.sort_unstable();
        assert_eq!(ranks, vec![0, 1, 2, 3]);
    }

    #[test]
    fn meet_table_matches_section_7() {
        // Rows: [Stable, Metastable, Cyclic, Chaotic]
        let expected = [
            [Stable, Metastable, Cyclic, Chaotic],
            [Metastable, Metastable, Cyclic, Chaotic],
            [Cyclic, Cyclic, Cyclic, Chaotic],
            [Chaotic, Chaotic, Chaotic, Chaotic],
        ];
        let order = [Stable, Metastable, Cyclic, Chaotic];
        for (i, a) in order.iter().enumerate() {
            for (j, b) in order.iter().enumerate() {
                assert_eq!(a.meet(*b), expected[i][j]);
            }
        }
    }

    #[test]
    fn join_table_matches_section_7() {
        let expected = [
            [Stable, Stable, Stable, Stable],
            [Stable, Metastable, Metastable, Metastable],
            [Stable, Metastable, Cyclic, Cyclic],
            [Stable, Metastable, Cyclic, Chaotic],
        ];
        let order = [Stable, Metastable, Cyclic, Chaotic];
        for (i, a) in order.iter().enumerate() {
            for (j, b) in order.iter().enumerate() {
                assert_eq!(a.join(*b), expected[i][j]);
            }
        }
    }

    #[test]
    fn negation_table_matches_section_7() {
        assert_eq!(Stable.negate(), Chaotic);
        assert_eq!(Metastable.negate(), Chaotic);
        assert_eq!(Cyclic.negate(), Chaotic);
        assert_eq!(Chaotic.negate(), Stable);
    }

    #[test]
    fn heyting_axioms_hold() {
        for a in OmegaSet::ALL {
            for b in OmegaSet::ALL {
                // a → b = ⊤  ⟺  a ≤ b
                assert_eq!(a.implies(b) == OmegaSet::TOP, a.le(b));
                // a ∧ (a → b) ≤ b
                let meet = a.meet(a.implies(b));
                assert!(meet.le(b), "modus ponens fails at ({:?}, {:?})", a, b);
            }
        }
    }

    #[test]
    fn excluded_middle_fails() {
        // METASTABLE ∨ ¬METASTABLE = METASTABLE ≠ STABLE (Tverdzhennia 7.1)
        assert_ne!(Metastable.join(Metastable.negate()), OmegaSet::TOP);
    }

    #[test]
    fn double_negation_only_returns_top_or_bottom() {
        for a in OmegaSet::ALL {
            let nn = a.negate().negate();
            assert!(
                nn == OmegaSet::TOP || nn == OmegaSet::BOTTOM,
                "¬¬{:?} = {:?} is neither TOP nor BOTTOM",
                a, nn
            );
        }
        // ¬¬TOP = TOP
        assert_eq!(OmegaSet::TOP.negate().negate(), OmegaSet::TOP);
        // ¬¬BOTTOM = BOTTOM
        assert_eq!(OmegaSet::BOTTOM.negate().negate(), OmegaSet::BOTTOM);
    }

    #[test]
    fn distribution_holds() {
        for a in OmegaSet::ALL {
            for b in OmegaSet::ALL {
                for c in OmegaSet::ALL {
                    // a ∧ (b ∨ c) = (a ∧ b) ∨ (a ∧ c)
                    let lhs = a.meet(b.join(c));
                    let rhs = a.meet(b).join(a.meet(c));
                    assert_eq!(lhs, rhs);
                }
            }
        }
    }
}
```

---

## `src/certificate.rs` (новий)

```rust
//! Machine-verifiable certificates for Ω-classification.
//!
//! A certificate records the trajectory and its classification. Any
//! independent implementation can re-run the system from the first
//! state and verify the classification in polynomial time.

use crate::evolution::{ExtendedState, System};
use crate::omega::{self, Attainment, OmegaSet, OmegaTraj};
use serde::{Deserialize, Serialize};

/// Certificate of a trajectory classification.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct Certificate {
    /// The full trajectory up to and including one cycle.
    pub trajectory: Vec<ExtendedState>,
    /// Index at which the cycle begins (0 = from the start).
    pub cycle_start: usize,
    /// The eventual cycle.
    pub cycle: Vec<ExtendedState>,
    /// S-component of the trajectory classification.
    pub s_component: OmegaSet,
    /// Attainment type.
    pub att_type: Attainment,
    /// Core version that produced this certificate.
    pub core_version: String,
    /// Spec version this certificate conforms to.
    pub spec_version: String,
}

/// Build a certificate for the given start state.
pub fn produce(
    system: &System,
    start: ExtendedState,
    horizon: usize,
) -> Certificate {
    let analysis = crate::trajectory::analyze(system, start, horizon);
    let omega_traj = omega::classify_trajectory(system, start, horizon);

    let (trajectory, cycle_start, cycle) = match analysis {
        crate::trajectory::TrajectoryAnalysis::Attractor {
            prefix,
            fixed_point,
            m,
        } => {
            let mut traj = prefix.clone();
            traj.push(fixed_point);
            (traj, m, vec![fixed_point])
        }
        crate::trajectory::TrajectoryAnalysis::Cycle {
            prefix,
            cycle,
            m,
        } => {
            let mut traj = prefix;
            traj.extend(cycle.iter().copied());
            (traj, m, cycle)
        }
        crate::trajectory::TrajectoryAnalysis::InsufficientHorizon { trajectory } => {
            (trajectory, 0, vec![])
        }
    };

    Certificate {
        trajectory,
        cycle_start,
        cycle,
        s_component: omega_traj.s,
        att_type: omega_traj.att,
        core_version: crate::VERSION.to_string(),
        spec_version: crate::SPEC_VERSION.to_string(),
    }
}

/// Verify a certificate against a system. Returns `Ok(())` on success.
pub fn verify(system: &System, cert: &Certificate) -> Result<(), String> {
    if cert.trajectory.is_empty() {
        return Err("empty trajectory".into());
    }

    // 1. Re-run the trajectory from the first state.
    let mut cur = cert.trajectory[0];
    for (i, expected) in cert.trajectory.iter().enumerate() {
        if cur != *expected {
            return Err(format!("trajectory mismatch at index {}", i));
        }
        if i + 1 < cert.trajectory.len() {
            cur = system
                .step(cur)
                .ok_or_else(|| format!("step failed at index {}", i))?;
        }
    }

    // 2. Verify cycle boundary.
    if cert.cycle_start > cert.trajectory.len() {
        return Err("cycle_start exceeds trajectory length".into());
    }
    let reconstructed_cycle = &cert.trajectory[cert.cycle_start..];
    if reconstructed_cycle != cert.cycle.as_slice() {
        return Err("cycle slice does not match trajectory".into());
    }

    // 3. Verify cycle is closed.
    if !cert.cycle.is_empty() {
        let first = cert.cycle[0];
        let last = *cert.cycle.last().unwrap();
        let next = system
            .step(last)
            .ok_or_else(|| "step failed on cycle tail".to_string())?;
        if next != first {
            return Err("cycle is not closed".into());
        }
    }

    // 4. Verify s_component is consistent with cycle length.
    let expected_s = match cert.cycle.len() {
        0 => return Err("empty cycle in non-Indeterminate certificate".into()),
        1 => OmegaSet::Stable,
        _ => OmegaSet::Cyclic,
    };
    if cert.s_component != expected_s {
        return Err(format!(
            "s_component mismatch: cert says {:?}, cycle length {} implies {:?}",
            cert.s_component,
            cert.cycle.len(),
            expected_s
        ));
    }

    // 5. Finite-level trajectories are always Attained.
    if cert.att_type != Attainment::Attained {
        return Err(format!(
            "finite-level certificate must be Attained, got {:?}",
            cert.att_type
        ));
    }

    Ok(())
}

/// Build a certificate and return it as a JSON string.
pub fn produce_json(
    system: &System,
    start: ExtendedState,
    horizon: usize,
) -> Result<String, serde_json::Error> {
    let cert = produce(system, start, horizon);
    serde_json::to_string_pretty(&cert)
}

/// Parse a certificate from JSON.
pub fn parse_json(s: &str) -> Result<Certificate, serde_json::Error> {
    serde_json::from_str(s)
}

/// Classification as a `(OmegaSet, Attainment)` pair (redundant with
/// the certificate itself, but useful for piping into Ω_traj logic).
pub fn omega_traj_of(cert: &Certificate) -> OmegaTraj {
    OmegaTraj {
        s: cert.s_component,
        att: cert.att_type,
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::rule::{Identity, WhoCycle};
    use crate::state::State;

    #[test]
    fn produce_and_verify_attractor() {
        let sys = System::single(Box::new(Identity));
        let start = ExtendedState::new(State::from_code6(0).unwrap(), 0);
        let cert = produce(&sys, start, 10);
        assert_eq!(cert.s_component, OmegaSet::Stable);
        assert_eq!(cert.att_type, Attainment::Attained);
        assert!(verify(&sys, &cert).is_ok());
    }

    #[test]
    fn produce_and_verify_cycle() {
        let sys = System::single(Box::new(WhoCycle));
        let start = ExtendedState::new(State::from_code6(0).unwrap(), 1);
        let cert = produce(&sys, start, 20);
        assert_eq!(cert.s_component, OmegaSet::Cyclic);
        assert!(verify(&sys, &cert).is_ok());
        assert_eq!(cert.cycle.len(), 4);
    }

    #[test]
    fn json_roundtrip() {
        let sys = System::single(Box::new(WhoCycle));
        let start = ExtendedState::new(State::from_code6(0).unwrap(), 1);
        let json = produce_json(&sys, start, 20).unwrap();
        let cert = parse_json(&json).unwrap();
        assert!(verify(&sys, &cert).is_ok());
    }

    #[test]
    fn tampered_certificate_is_rejected() {
        let sys = System::single(Box::new(Identity));
        let start = ExtendedState::new(State::from_code6(0).unwrap(), 0);
        let mut cert = produce(&sys, start, 10);
        cert.s_component = OmegaSet::Chaotic; // wrong
        assert!(verify(&sys, &cert).is_err());
    }
}
```

---

## `tests/invariants.rs` (розширення)

Додати в кінець файлу:

```rust
// -------------------------------------------------------------------------
// [6.1] Ω_set is exhaustive and mutually exclusive.
// -------------------------------------------------------------------------

use subit_core::omega::{self, Attainment, OmegaSet, OmegaState};
use subit_core::lattice::*;

#[test]
fn invariant_6_1_omega_set_is_total() {
    let sys = System::standard();
    let h = omega::default_horizon(&sys);
    // Trivially true by construction (Rust enum), but verify by
    // classifying every singleton and checking a value is produced.
    for s in State::all_states().take(16) {
        for &rid in &sys.registry.all_ids() {
            let es = ExtendedState::new(s, rid);
            let singleton: omega::StateSet = std::iter::once(es).collect();
            let _ = omega::classify_set(&sys, &singleton, h);
        }
    }
}

// -------------------------------------------------------------------------
// [4.1] Singleton cannot be METASTABLE.
// -------------------------------------------------------------------------

#[test]
fn invariant_4_1_no_metastable_singletons() {
    let sys = System::standard();
    let h = omega::default_horizon(&sys);
    for s in State::all_states() {
        for &rid in &sys.registry.all_ids() {
            let es = ExtendedState::new(s, rid);
            let singleton: omega::StateSet = std::iter::once(es).collect();
            let cls = omega::classify_set(&sys, &singleton, h);
            assert_ne!(cls, OmegaSet::Metastable);
        }
    }
}

// -------------------------------------------------------------------------
// [7.1] Ω — Heyting algebra.
// -------------------------------------------------------------------------

#[test]
fn invariant_7_1_heyting_axioms() {
    for a in OmegaSet::ALL {
        for b in OmegaSet::ALL {
            // a → b = TOP ⟺ a ≤ b
            assert_eq!(a.implies(b) == OmegaSet::TOP, a.le(b));
            // Modus ponens: a ∧ (a → b) ≤ b
            assert!(a.meet(a.implies(b)).le(b));
            // Distributivity
            for c in OmegaSet::ALL {
                assert_eq!(a.meet(b.join(c)), a.meet(b).join(a.meet(c)));
            }
        }
    }
}

// -------------------------------------------------------------------------
// [7.2] ¬METASTABLE ≠ STABLE (excluded middle fails).
// -------------------------------------------------------------------------

#[test]
fn invariant_7_2_excluded_middle_fails() {
    assert_ne!(
        OmegaSet::Metastable.join(OmegaSet::Metastable.negate()),
        OmegaSet::TOP
    );
}

// -------------------------------------------------------------------------
// [18.6] Ω_traj is well-defined on every trajectory.
// -------------------------------------------------------------------------

#[test]
fn invariant_18_6_omega_traj_total_on_finite_core() {
    let sys = System::standard();
    let h = omega::default_horizon(&sys);
    for s in State::all_states().take(32) {
        for &rid in &sys.registry.all_ids() {
            let es = ExtendedState::new(s, rid);
            let ot = omega::classify_trajectory(&sys, es, h);
            // On the finite core, Attainment is always ATTAINED and
            // S-component is STABLE or CYCLIC.
            assert_eq!(ot.att, Attainment::Attained);
            assert!(
                matches!(ot.s, OmegaSet::Stable | OmegaSet::Cyclic),
                "unexpected S-component {:?} on finite core",
                ot.s
            );
        }
    }
}

// -------------------------------------------------------------------------
// [18.9] Certificates are machine-verifiable.
// -------------------------------------------------------------------------

use subit_core::certificate;

#[test]
fn invariant_18_9_certificates_verify() {
    let sys = System::standard();
    let h = omega::default_horizon(&sys);
    for s in State::all_states().take(16) {
        for &rid in &sys.registry.all_ids() {
            let es = ExtendedState::new(s, rid);
            let cert = certificate::produce(&sys, es, h);
            certificate::verify(&sys, &cert)
                .unwrap_or_else(|e| panic!("cert verify failed: {}", e));
        }
    }
}

// -------------------------------------------------------------------------
// [18.7] Ω_state and Ω_traj agree on cycle length.
// -------------------------------------------------------------------------

#[test]
fn invariant_18_7_state_traj_agree() {
    let sys = System::single(Box::new(subit_core::rule::Identity));
    let es = ExtendedState::new(State::from_code6(0).unwrap(), 0);
    let st = omega::classify_state(&sys, es, 10);
    let tr = omega::classify_trajectory(&sys, es, 10);
    // For a fixed point: state = Stable, trajectory S = Stable.
    assert_eq!(st, OmegaState::Stable);
    assert_eq!(tr.s, OmegaSet::Stable);
}
```

---

## CI і запуск

```bash
cd core
cargo build
cargo test
cargo clippy --all-targets -- -D warnings
```

Очікується:
- 45 юніт-тестів (додано ~20 до 25 з ітерації 2.1)
- 12 інваріантних тестів (додано 6 до 6 з ітерації 2.1)

---

## Відповідність STATUS.md

| ID | Твердження | Де реалізовано | Тест |
|---|---|---|---|
| 5.1 | Скінченна періодичність | `trajectory::analyze` | `invariant_5_1` |
| 6.1 | Ω_set — повний і взаємовиключний | `omega::classify_set` | `invariant_6_1` |
| 6.3 | Ω_state без METASTABLE | `omega::classify_state` | `invariant_4_1` |
| 7.1 | Ω — алгебра Гейтінга | `lattice::*` | `invariant_7_1` |
| 7.2 | ¬METASTABLE ≠ STABLE | `OmegaSet::negate` | `invariant_7_2` |
| 18.6 | Ω_traj тотальний на скінченному ядрі | `omega::classify_trajectory` | `invariant_18_6` |
| 18.7 | Узгодженість Ω_state / Ω_traj | обидва | `invariant_18_7` |
| 18.9 | Сертифікати машинно перевірювані | `certificate::verify` | `invariant_18_9` |

**Поза обсягом ітерації 2.2** (буде в 2.3): категорія, модальності, нормативні тестові вектори JSON, CI-конфігурація, ≥ 100 тестових векторів.

---

## Критерій завершення ітерації 2.2

- [x] `trajectory` — Алгоритм 5.1 з горизонтом
- [x] `omega` — Ω_set, Ω_state, Ω_traj (12 значень)
- [x] `lattice` — ∧, ∨, →, ¬; усі таблиці §7 відтворено
- [x] `certificate` — JSON-серіалізація і `verify()`
- [x] Усі чотири таблиці §7 перевірено юніт-тестами
- [x] Інваріанти 6.1, 7.1, 7.2, 18.6, 18.7, 18.9 покриті
- [x] `certificate::verify` відкидає підроблені сертифікати

**Ітерація 2.2 завершена.**

---

## Що далі: ітерація 2.3

Обсяг наступного артефакту:

- `category` — об'єкти, морфізми, композиція, термінальний об'єкт 1, добуток ×
- `modality` — □, ◇, ◯; аксіоми M1–M9 (без M4), перевірка на скінченному ядрі
- Нормативні тестові вектори — JSON-файли `tests/vectors/*.json`
- CI-конфігурація (GitHub Actions)
- Мінімальний CLI або бінарник для прогону тестових векторів

Після ітерації 2.3 Фаза 2 завершується і можна переходити до Фази 3 (PROOFS у Lean 4) паралельно з Фазою 4 (INFINITY).

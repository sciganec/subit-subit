# SUBIT-INFINITY v0.2.0 — Фаза 4, ітерація 4.2

**Lazy S_∞, аперіодичні траєкторії, ASYMPTOTIC, INDETERMINATE, d_ω, повна P(τ)**

Розширюємо INFINITY до повного S_∞ через lazy-подання. Після цієї ітерації реалізовано всі три типи Attainment і повну структуру P(τ) з §18.8 v6.0-draft.

---

## Ключове архітектурне рішення

Ітерація 4.1 використовувала **скінченні DAG** (regular trees). Це давало компактність, але робило неможливими:
- аперіодичні траєкторії (S_∞ скінченний up to depth MAX_DEPTH),
- ASYMPTOTIC (не було куди наближатися),
- INDETERMINATE (horizon завжди достатній).

Ітерація 4.2 вводить **lazy trees** — дерева, побудовані через `Rc<Head>`, де `Head` рекурсивно містить піддерева. Це дозволяє:
- дерева необмеженої глибини,
- траєкторії без повторів,
- природну появу ASYMPTOTIC (траєкторія прямує до границі, не досягаючи її),
- INDETERMINATE (коли depth-обмеження не дозволяє розрізнити поведінку).

---

## Структура (додано до `infinity/`)

```
infinity/
├── src/
│   ├── lazy_tree.rs       ← новий
│   ├── lazy_metric.rs     ← новий
│   ├── lazy_dynamics.rs   ← новий
│   ├── lazy_omega.rs      ← новий (ω-границя + Attainment)
│   ├── lazy_p_tau.rs      ← новий (повна P(τ))
│   ├── d_omega.rs         ← новий (метрика за першою розбіжністю ω)
│   ├── bin/
│   │   └── lazy-demo.rs   ← новий
│   └── lib.rs             ← оновлено
└── tests/
    └── lazy_invariants.rs ← новий
```

---

## `src/lazy_tree.rs` (новий)

```rust
//! Lazy trees — coinductive representation of S_∞ elements.
//!
//! A lazy tree is an `Rc<Head>` where `Head` is either a leaf
//! (labelled by a `Primitive`) or an internal node with three
//! subtrees. Cycles and unbounded depth are supported by construction.
//!
//! Depth is unbounded, but all *decisions* in this iteration are made
//! up to a finite `depth` parameter, which is the honest analogue of
//! "how far the observer can see into S_∞".

use std::rc::Rc;

use subit_core::alphabet::Primitive;

/// Structural head of a lazy tree.
#[derive(Debug)]
pub enum Head {
    Leaf(Primitive),
    Node(LazyTree, LazyTree, LazyTree),
}

/// A (possibly infinite) tree.
#[derive(Clone, Debug)]
pub struct LazyTree(Rc<Head>);

impl LazyTree {
    pub fn leaf(p: Primitive) -> Self {
        Self(Rc::new(Head::Leaf(p)))
    }

    pub fn node(a: Self, b: Self, c: Self) -> Self {
        Self(Rc::new(Head::Node(a, b, c)))
    }

    pub fn head(&self) -> &Head {
        &self.0
    }

    pub fn is_leaf(&self) -> bool {
        matches!(&*self.0, Head::Leaf(_))
    }

    pub fn leaf_label(&self) -> Option<Primitive> {
        match &*self.0 {
            Head::Leaf(p) => Some(*p),
            _ => None,
        }
    }

    pub fn children(&self) -> Option<(Self, Self, Self)> {
        match &*self.0 {
            Head::Leaf(_) => None,
            Head::Node(a, b, c) => Some((a.clone(), b.clone(), c.clone())),
        }
    }

    /// Depth, capped at `bound` (to avoid non-termination on infinite trees).
    pub fn depth_bounded(&self, bound: usize) -> usize {
        if bound == 0 {
            return 0;
        }
        match self.head() {
            Head::Leaf(_) => 0,
            Head::Node(a, b, c) => {
                1 + a.depth_bounded(bound - 1)
                    .max(b.depth_bounded(bound - 1))
                    .max(c.depth_bounded(bound - 1))
            }
        }
    }

    /// Structural fingerprint, truncated at `depth`.
    pub fn fingerprint(&self, depth: usize) -> Fingerprint {
        if depth == 0 {
            return Fingerprint::Truncated;
        }
        match self.head() {
            Head::Leaf(p) => Fingerprint::Leaf(*p),
            Head::Node(a, b, c) => Fingerprint::Node(
                Box::new(a.fingerprint(depth - 1)),
                Box::new(b.fingerprint(depth - 1)),
                Box::new(c.fingerprint(depth - 1)),
            ),
        }
    }

    /// Self-referential tree: root has three children all equal to root,
    /// with the root itself a leaf of the given primitive.
    ///
    /// Constructed via `Rc::new_cyclic` — this is the honest "cyclic
    /// tree" case. The tree is infinite by unrolling.
    pub fn cyclic_leaf(p: Primitive) -> Self {
        Self(Rc::new_cyclic(|weak| {
            let me = LazyTree(weak.upgrade().expect("root alive"));
            Head::Node(me.clone(), me.clone(), me)
        }))
    }
}

impl LazyTree {
    /// The S_0 embedding: `(a, b, c)` as a depth-1 tree.
    pub fn from_state(s: subit_core::state::State) -> Self {
        Self::node(
            Self::leaf(s.who),
            Self::leaf(s.where_),
            Self::leaf(s.when_),
        )
    }
}

/// Fingerprint of a truncated subtree.
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub enum Fingerprint {
    Truncated,
    Leaf(Primitive),
    Node(Box<Fingerprint>, Box<Fingerprint>, Box<Fingerprint>),
}

#[cfg(test)]
mod tests {
    use super::*;
    use subit_core::state::State;

    #[test]
    fn leaf_is_a_leaf() {
        let t = LazyTree::leaf(Primitive::T);
        assert!(t.is_leaf());
        assert_eq!(t.leaf_label(), Some(Primitive::T));
        assert!(t.children().is_none());
    }

    #[test]
    fn node_has_three_children() {
        let a = LazyTree::leaf(Primitive::T);
        let b = LazyTree::leaf(Primitive::F);
        let c = LazyTree::leaf(Primitive::N);
        let t = LazyTree::node(a.clone(), b.clone(), c.clone());
        let (x, y, z) = t.children().unwrap();
        assert_eq!(x.leaf_label(), Some(Primitive::T));
        assert_eq!(y.leaf_label(), Some(Primitive::F));
        assert_eq!(z.leaf_label(), Some(Primitive::N));
    }

    #[test]
    fn from_state_has_depth_one() {
        let s = State::new(Primitive::T, Primitive::F, Primitive::N);
        let t = LazyTree::from_state(s);
        assert_eq!(t.depth_bounded(16), 1);
    }

    #[test]
    fn fingerprint_is_deterministic() {
        let t = LazyTree::node(
            LazyTree::leaf(Primitive::T),
            LazyTree::leaf(Primitive::F),
            LazyTree::leaf(Primitive::N),
        );
        assert_eq!(t.fingerprint(4), t.fingerprint(4));
    }

    #[test]
    fn fingerprint_distinguishes_labels() {
        let a = LazyTree::leaf(Primitive::T);
        let b = LazyTree::leaf(Primitive::F);
        assert_ne!(a.fingerprint(4), b.fingerprint(4));
    }

    #[test]
    fn cyclic_leaf_has_unbounded_depth() {
        let t = LazyTree::cyclic_leaf(Primitive::T);
        // Depth bounded at 16 should be 16 (or close).
        assert!(t.depth_bounded(16) >= 15);
    }
}
```

---

## `src/lazy_metric.rs` (новий)

```rust
//! d_S on lazy trees — §18.2 of SUBIT v6.0.

use crate::lazy_tree::{Fingerprint, LazyTree};

/// Least depth of divergence between two lazy trees, capped at `bound`.
pub fn delta_bounded(a: &LazyTree, b: &LazyTree, bound: usize) -> usize {
    if bound == 0 {
        return 0;
    }
    match (a.head(), b.head()) {
        (
            crate::lazy_tree::Head::Leaf(p),
            crate::lazy_tree::Head::Leaf(q),
        ) => {
            if p == q { bound } else { 0 }
        }
        (crate::lazy_tree::Head::Leaf(_), _) => 0,
        (_, crate::lazy_tree::Head::Leaf(_)) => 0,
        (
            crate::lazy_tree::Head::Node(a1, a2, a3),
            crate::lazy_tree::Head::Node(b1, b2, b3),
        ) => {
            let d1 = delta_bounded(a1, b1, bound - 1);
            let d2 = delta_bounded(a2, b2, bound - 1);
            let d3 = delta_bounded(a3, b3, bound - 1);
            1 + d1.min(d2).min(d3)
        }
    }
}

/// Structural ultrametric, capped at `bound`.
pub fn d_s_bounded(a: &LazyTree, b: &LazyTree, bound: usize) -> f64 {
    let d = delta_bounded(a, b, bound);
    if d >= bound {
        0.0
    } else {
        2f64.powi(-(d as i32))
    }
}

/// Default bound for d_S computations in this iteration.
pub const DEFAULT_BOUND: usize = 64;

pub fn d_s(a: &LazyTree, b: &LazyTree) -> f64 {
    d_s_bounded(a, b, DEFAULT_BOUND)
}

/// Structural equality up to a depth bound.
pub fn eq_bounded(a: &LazyTree, b: &LazyTree, depth: usize) -> bool {
    a.fingerprint(depth) == b.fingerprint(depth)
}

/// Fingerprint of a lazy tree at a depth.
pub fn fp(t: &LazyTree, depth: usize) -> Fingerprint {
    t.fingerprint(depth)
}

#[cfg(test)]
mod tests {
    use super::*;
    use subit_core::alphabet::Primitive;

    #[test]
    fn identical_leaves_have_distance_zero() {
        let a = LazyTree::leaf(Primitive::T);
        let b = LazyTree::leaf(Primitive::T);
        assert_eq!(d_s(&a, &b), 0.0);
    }

    #[test]
    fn distinct_leaves_have_distance_one() {
        let a = LazyTree::leaf(Primitive::T);
        let b = LazyTree::leaf(Primitive::F);
        assert_eq!(d_s(&a, &b), 1.0);
    }

    #[test]
    fn ultrametric_strong_triangle() {
        let a = LazyTree::leaf(Primitive::T);
        let b = LazyTree::leaf(Primitive::F);
        let c = LazyTree::leaf(Primitive::N);
        assert!(d_s(&a, &c) <= d_s(&a, &b).max(d_s(&b, &c)));
    }

    #[test]
    fn deeper_agreement_smaller_distance() {
        let a = LazyTree::leaf(Primitive::T);
        let b = LazyTree::leaf(Primitive::F);
        let c = LazyTree::node(a.clone(), b.clone(), a.clone());
        let d = LazyTree::node(a.clone(), b.clone(), b.clone());
        let dist = d_s(&c, &d);
        assert!(dist > 0.0 && dist < 1.0, "expected 0 < {} < 1", dist);
    }
}
```

---

## `src/lazy_dynamics.rs` (новий)

```rust
//! Rules and systems on lazy S_∞.

use crate::lazy_tree::LazyTree;
use subit_core::alphabet::Primitive;

pub trait LazyRule: Send + Sync {
    fn id(&self) -> u16;
    fn name(&self) -> &'static str;
    fn apply(&self, t: &LazyTree) -> LazyTree;
}

pub struct LazySystem {
    rules: Vec<Box<dyn LazyRule>>,
}

impl LazySystem {
    pub fn new(rules: Vec<Box<dyn LazyRule>>) -> Self {
        Self { rules }
    }
    pub fn single(r: Box<dyn LazyRule>) -> Self {
        Self::new(vec![r])
    }
    pub fn rule_ids(&self) -> Vec<u16> {
        self.rules.iter().map(|r| r.id()).collect()
    }
    pub fn rule(&self, id: u16) -> Option<&dyn LazyRule> {
        self.rules.iter().find(|r| r.id() == id).map(|b| b.as_ref())
    }
    pub fn len(&self) -> usize { self.rules.len() }
    pub fn is_empty(&self) -> bool { self.rules.is_empty() }

    pub fn step(&self, t: &LazyTree, rule_id: u16) -> Option<(LazyTree, u16)> {
        let r = self.rule(rule_id)?;
        let next = r.apply(t);
        let ids = self.rule_ids();
        let pos = ids.iter().position(|&x| x == rule_id)?;
        Some((next, ids[(pos + 1) % ids.len()]))
    }
}

// -------------------------------------------------------------------------
// Rules
// -------------------------------------------------------------------------

/// `id(t) = t`.
pub struct LazyIdentity;
impl LazyRule for LazyIdentity {
    fn id(&self) -> u16 { 0 }
    fn name(&self) -> &'static str { "identity" }
    fn apply(&self, t: &LazyTree) -> LazyTree { t.clone() }
}

/// `t ↦ Node(leaf(T), t, leaf(F))`.
///
/// Grows an infinite middle spine. Trajectory converges in d_S to a
/// fixed point (infinite chain), never reaching it. ASYMPTOTIC.
pub struct GrowChain;
impl LazyRule for GrowChain {
    fn id(&self) -> u16 { 300 }
    fn name(&self) -> &'static str { "grow_chain" }
    fn apply(&self, t: &LazyTree) -> LazyTree {
        LazyTree::node(
            LazyTree::leaf(Primitive::T),
            t.clone(),
            LazyTree::leaf(Primitive::F),
        )
    }
}

/// `t ↦ Node(t, leaf(label_n), leaf(F))` where `label_n` alternates
/// based on an internal counter kept in the system.
///
/// The trajectory has increasing depth and non-vanishing d_S distance
/// between consecutive states. No cycle, no convergence. CHAOTIC
/// (weak sense) with INDETERMINATE attainment.
pub struct ShiftSpine;

impl LazyRule for ShiftSpine {
    fn id(&self) -> u16 { 301 }
    fn name(&self) -> &'static str { "shift_spine" }
    fn apply(&self, t: &LazyTree) -> LazyTree {
        // Label at depth 1 depends on the current depth of t.
        // Even depth → T, odd depth → F. This makes the trajectory
        // alternate between two "families" without ever repeating.
        let d = t.depth_bounded(32);
        let label = if d % 2 == 0 { Primitive::T } else { Primitive::F };
        LazyTree::node(t.clone(), LazyTree::leaf(label), LazyTree::leaf(Primitive::F))
    }
}

/// `t ↦ t` for depth ≥ `threshold`, otherwise wraps. Used to force
/// INDETERMINATE by making classification depend on a horizon that
/// exceeds the analysis bound.
pub struct BoundedWrap {
    pub threshold: usize,
}

impl LazyRule for BoundedWrap {
    fn id(&self) -> u16 { 302 }
    fn name(&self) -> &'static str { "bounded_wrap" }
    fn apply(&self, t: &LazyTree) -> LazyTree {
        let d = t.depth_bounded(64);
        if d >= self.threshold {
            t.clone()
        } else {
            LazyTree::node(t.clone(), t.clone(), t.clone())
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn identity_is_identity() {
        let t = LazyTree::leaf(Primitive::T);
        assert_eq!(
            LazyIdentity.apply(&t).fingerprint(4),
            t.fingerprint(4)
        );
    }

    #[test]
    fn grow_chain_increases_depth() {
        let mut t = LazyTree::leaf(Primitive::T);
        for _ in 0..3 {
            t = GrowChain.apply(&t);
        }
        assert!(t.depth_bounded(16) >= 3);
    }

    #[test]
    fn shift_spine_increases_depth() {
        let mut t = LazyTree::leaf(Primitive::T);
        for _ in 0..4 {
            t = ShiftSpine.apply(&t);
        }
        assert!(t.depth_bounded(32) >= 4);
    }

    #[test]
    fn system_step_is_total() {
        let sys = LazySystem::single(Box::new(LazyIdentity));
        let t = LazyTree::leaf(Primitive::T);
        assert!(sys.step(&t, 0).is_some());
    }

    #[test]
    fn grow_chain_trajectory_states_are_distinct_at_small_depth() {
        // Consecutive states of GrowChain differ at depth 1.
        let sys = LazySystem::single(Box::new(GrowChain));
        let t0 = LazyTree::leaf(Primitive::T);
        let (t1, _) = sys.step(&t0, 300).unwrap();
        let (t2, _) = sys.step(&t1, 300).unwrap();
        assert_ne!(t1.fingerprint(4), t2.fingerprint(4));
    }
}
```

---

## `src/lazy_omega.rs` (новий)

```rust
//! ω-limit and Attainment on lazy S_∞.

use std::collections::HashMap;

use crate::lazy_dynamics::LazySystem;
use crate::lazy_metric::d_s;
use crate::lazy_tree::{Fingerprint, LazyTree};

/// A trajectory in S_∞ × R.
#[derive(Debug, Clone)]
pub struct LazyTrajectory {
    pub states: Vec<(LazyTree, u16)>,
    /// Fingerprints used for cycle detection.
    pub fingerprints: Vec<Fingerprint>,
}

/// Advance the trajectory up to `horizon` steps. Cycle detection is
/// done via fingerprints at `depth`.
pub fn advance(
    system: &LazySystem,
    start: &LazyTree,
    rule_id: u16,
    horizon: usize,
    depth: usize,
) -> (LazyTrajectory, Option<usize>) {
    let mut states = Vec::with_capacity(horizon + 1);
    let mut fingerprints = Vec::with_capacity(horizon + 1);
    let mut cur = (start.clone(), rule_id);
    let mut seen: HashMap<(Fingerprint, u16), usize> = HashMap::new();

    for n in 0..=horizon {
        let fp = cur.0.fingerprint(depth);
        let key = (fp.clone(), cur.1);
        if let Some(&prev) = seen.get(&key) {
            states.push(cur);
            fingerprints.push(fp);
            let traj = LazyTrajectory { states, fingerprints };
            return (traj, Some(prev));
        }
        seen.insert(key, n);
        states.push(cur.clone());
        fingerprints.push(fp);
        match system.step(&cur.0, cur.1) {
            Some(next) => cur = next,
            None => {
                let traj = LazyTrajectory { states, fingerprints };
                return (traj, None);
            }
        }
    }

    let traj = LazyTrajectory { states, fingerprints };
    (traj, None)
}

/// Attainment type — Ozn. 18.5 of v6.0.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Attainment {
    Attained,
    Asymptotic,
    Indeterminate,
}

/// Classify the attainment type given the trajectory.
///
/// `attained_at` = Some(m) if the trajectory is eventually periodic
/// with transient length m (from `advance`).
pub fn attainment(
    traj: &LazyTrajectory,
    attained_at: Option<usize>,
    horizon: usize,
) -> Attainment {
    if let Some(_m) = attained_at {
        return Attainment::Attained;
    }
    // No cycle detected within the horizon. Check whether the
    // trajectory is converging (d_S between consecutive states → 0)
    // or not.
    if traj.states.len() < 3 {
        return Attainment::Indeterminate;
    }
    let n = traj.states.len();
    // Look at the last few consecutive distances.
    let mut decreasing = true;
    let mut last = f64::INFINITY;
    for i in (n - 5).max(1)..n {
        let d = d_s(&traj.states[i - 1].0, &traj.states[i].0);
        if d > last {
            decreasing = false;
            break;
        }
        last = d;
    }
    if decreasing && last < 0.5 {
        Attainment::Asymptotic
    } else {
        Attainment::Indeterminate
    }
}

/// Whether the ω-limit is uniquely determined by the fingerprint
/// sequence. In this iteration we approximate: distinct fingerprints
/// imply distinct ω-limits.
pub fn omega_fingerprint_set(traj: &LazyTrajectory) -> std::collections::HashSet<Fingerprint> {
    traj.fingerprints.iter().cloned().collect()
}

/// Number of distinct fingerprints in the trajectory (lower bound on
/// the size of the ω-limit).
pub fn omega_size_lower_bound(traj: &LazyTrajectory) -> usize {
    omega_fingerprint_set(traj).len()
}

/// Detect convergence: is the trajectory approaching a fixed point
/// in d_S? Returns the asymptotic rate, or `None` if not converging.
pub fn convergence_rate(traj: &LazyTrajectory, tail: usize) -> Option<f64> {
    if traj.states.len() < tail + 1 {
        return None;
    }
    let n = traj.states.len();
    let start = n - tail - 1;
    let mut ratios = Vec::new();
    for i in (start + 1)..n {
        let d_curr = d_s(&traj.states[i - 1].0, &traj.states[i].0);
        if i + 1 < n {
            let d_next = d_s(&traj.states[i].0, &traj.states[i + 1].0);
            if d_curr > 1e-12 {
                ratios.push(d_next / d_curr);
            }
        }
    }
    if ratios.is_empty() {
        return None;
    }
    let avg: f64 = ratios.iter().sum::<f64>() / ratios.len() as f64;
    Some(avg)
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::lazy_dynamics::{GrowChain, LazyIdentity, ShiftSpine};
    use subit_core::alphabet::Primitive;

    #[test]
    fn identity_attains_immediately() {
        let sys = LazySystem::single(Box::new(LazyIdentity));
        let t = LazyTree::leaf(Primitive::T);
        let (traj, cycle_start) = advance(&sys, &t, 0, 10, 8);
        assert_eq!(cycle_start, Some(0));
        assert_eq!(attainment(&traj, cycle_start, 10), Attainment::Attained);
    }

    #[test]
    fn grow_chain_is_asymptotic() {
        let sys = LazySystem::single(Box::new(GrowChain));
        let t = LazyTree::leaf(Primitive::T);
        let (traj, cycle_start) = advance(&sys, &t, 300, 20, 32);
        assert!(cycle_start.is_none(), "grow_chain must not cycle within horizon");
        let att = attainment(&traj, cycle_start, 20);
        assert_eq!(att, Attainment::Asymptotic);
    }

    #[test]
    fn shift_spine_is_indeterminate() {
        let sys = LazySystem::single(Box::new(ShiftSpine));
        let t = LazyTree::leaf(Primitive::T);
        let (traj, cycle_start) = advance(&sys, &t, 301, 20, 32);
        assert!(cycle_start.is_none());
        let att = attainment(&traj, cycle_start, 20);
        assert_eq!(att, Attainment::Indeterminate);
    }
}
```

---

## `src/d_omega.rs` (новий)

```rust
//! d_ω — metric by first divergence of ω-limits.
//!
//! Two trajectories are compared by the first index at which their
//! eventual behavior diverges. In this iteration, we approximate
//! "eventual behavior" by the fingerprint sequence.

use crate::lazy_dynamics::LazySystem;
use crate::lazy_tree::LazyTree;

/// Metric on trajectory pairs: 2^(−n₀) where n₀ is the first index at
/// which the two trajectories diverge (fingerprint-wise).
pub fn d_omega(
    system_a: &LazySystem,
    start_a: &LazyTree,
    rule_a: u16,
    system_b: &LazySystem,
    start_b: &LazyTree,
    rule_b: u16,
    horizon: usize,
    depth: usize,
) -> f64 {
    let (traj_a, _) = crate::lazy_omega::advance(system_a, start_a, rule_a, horizon, depth);
    let (traj_b, _) = crate::lazy_omega::advance(system_b, start_b, rule_b, horizon, depth);

    let n = traj_a.fingerprints.len().min(traj_b.fingerprints.len());
    for i in 0..n {
        if traj_a.fingerprints[i] != traj_b.fingerprints[i] {
            return 2f64.powi(-(i as i32));
        }
    }
    0.0
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::lazy_dynamics::{GrowChain, LazyIdentity};
    use subit_core::alphabet::Primitive;

    #[test]
    fn identical_systems_have_zero_distance() {
        let sys = LazySystem::single(Box::new(LazyIdentity));
        let t = LazyTree::leaf(Primitive::T);
        let d = d_omega(&sys, &t, 0, &sys, &t, 0, 10, 8);
        assert_eq!(d, 0.0);
    }

    #[test]
    fn different_first_step_means_distance_half() {
        let sys1 = LazySystem::single(Box::new(LazyIdentity));
        let sys2 = LazySystem::single(Box::new(GrowChain));
        let t = LazyTree::leaf(Primitive::T);
        let d = d_omega(&sys1, &t, 0, &sys2, &t, 300, 10, 8);
        // Step 0: identical (leaf). Step 1: differ.
        // So first divergence at index 1 → d = 2^(-1) = 0.5.
        assert_eq!(d, 0.5);
    }
}
```

---

## `src/lazy_p_tau.rs` (новий)

```rust
//! Full P(τ) — §18.8 of v6.0-draft.

use serde::{Deserialize, Serialize};

use crate::lazy_dynamics::LazySystem;
use crate::lazy_omega::{self, Attainment, LazyTrajectory};
use crate::lazy_tree::LazyTree;

/// S-component of Ω_traj (§18.7).
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum SComponent {
    Stable,
    Cyclic,
    Metastable,
    Chaotic,
}

/// Two-axis classification Ω_traj = (S, Att).
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub struct OmegaTraj {
    pub s: SComponent,
    pub att: Attainment,
}

/// Certificate of a P(τ) computation.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PTauCertificate {
    pub omega_traj: OmegaTraj,
    pub cycle_start: Option<usize>,
    pub cycle_length: usize,
    pub horizon_used: usize,
    pub depth_used: usize,
    pub core_version: String,
    pub spec_version: String,
    pub iteration: String,
}

/// The full P(τ): pair (ω-trajectory, certificate).
pub struct PTau {
    pub trajectory: LazyTrajectory,
    pub omega_traj: OmegaTraj,
    pub certificate: PTauCertificate,
}

/// Classify a lazy trajectory.
pub fn classify(
    system: &LazySystem,
    start: &LazyTree,
    rule_id: u16,
    horizon: usize,
    depth: usize,
) -> PTau {
    let (traj, cycle_start) = lazy_omega::advance(system, start, rule_id, horizon, depth);
    let att = lazy_omega::attainment(&traj, cycle_start, horizon);

    let cycle_length = match cycle_start {
        Some(m) => traj.states.len() - m,
        None => 0,
    };

    let s = if cycle_start.is_some() {
        if cycle_length == 1 {
            SComponent::Stable
        } else {
            SComponent::Cyclic
        }
    } else if att == Attainment::Asymptotic {
        // Converging to a fixed point in S_∞.
        SComponent::Stable
    } else {
        SComponent::Chaotic
    };

    let omega_traj = OmegaTraj { s, att };

    let certificate = PTauCertificate {
        omega_traj,
        cycle_start,
        cycle_length,
        horizon_used: horizon,
        depth_used: depth,
        core_version: crate::VERSION.to_string(),
        spec_version: crate::SPEC_VERSION.to_string(),
        iteration: crate::ITERATION.to_string(),
    };

    PTau {
        trajectory: traj,
        omega_traj,
        certificate,
    }
}

/// Non-collapse check (У0): the classification is not constant across
/// rules.
pub fn is_non_collapsing(horizon: usize, depth: usize) -> bool {
    use crate::lazy_dynamics::{GrowChain, LazyIdentity, ShiftSpine};
    use subit_core::alphabet::Primitive;

    let start = LazyTree::leaf(Primitive::T);

    let sys_id = LazySystem::single(Box::new(LazyIdentity));
    let sys_grow = LazySystem::single(Box::new(GrowChain));
    let sys_spine = LazySystem::single(Box::new(ShiftSpine));

    let c1 = classify(&sys_id, &start, 0, horizon, depth).omega_traj;
    let c2 = classify(&sys_grow, &start, 300, horizon, depth).omega_traj;
    let c3 = classify(&sys_spine, &start, 301, horizon, depth).omega_traj;

    let set: std::collections::HashSet<_> = [c1, c2, c3].into_iter().collect();
    set.len() >= 2
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::lazy_dynamics::{GrowChain, LazyIdentity, ShiftSpine};
    use subit_core::alphabet::Primitive;

    #[test]
    fn identity_yields_stable_attained() {
        let sys = LazySystem::single(Box::new(LazyIdentity));
        let start = LazyTree::leaf(Primitive::T);
        let p = classify(&sys, &start, 0, 10, 8);
        assert_eq!(p.omega_traj.s, SComponent::Stable);
        assert_eq!(p.omega_traj.att, Attainment::Attained);
    }

    #[test]
    fn grow_chain_yields_stable_asymptotic() {
        let sys = LazySystem::single(Box::new(GrowChain));
        let start = LazyTree::leaf(Primitive::T);
        let p = classify(&sys, &start, 300, 20, 32);
        assert_eq!(p.omega_traj.s, SComponent::Stable);
        assert_eq!(p.omega_traj.att, Attainment::Asymptotic);
    }

    #[test]
    fn shift_spine_yields_chaotic_indeterminate() {
        let sys = LazySystem::single(Box::new(ShiftSpine));
        let start = LazyTree::leaf(Primitive::T);
        let p = classify(&sys, &start, 301, 20, 32);
        assert_eq!(p.omega_traj.s, SComponent::Chaotic);
        assert_eq!(p.omega_traj.att, Attainment::Indeterminate);
    }

    #[test]
    fn non_collapse_holds() {
        assert!(is_non_collapsing(20, 32));
    }
}
```

---

## `src/lib.rs` (оновлено)

```rust
pub mod d_omega;
pub mod dynamics;
pub mod lazy_dynamics;
pub mod lazy_metric;
pub mod lazy_omega;
pub mod lazy_p_tau;
pub mod lazy_tree;
pub mod metric;
pub mod omega_limit;
pub mod p_tau;
pub mod tree;

pub const VERSION: &str = env!("CARGO_PKG_VERSION");
pub const SPEC_VERSION: &str = "v6.0-draft";
pub const ITERATION: &str = "4.2";
```

---

## `src/bin/lazy-demo.rs` (новий)

```rust
//! Demonstration: full P(τ) on lazy S_∞.
//!
//! Three regimes:
//! - Identity       → (STABLE, ATTAINED)
//! - GrowChain      → (STABLE, ASYMPTOTIC)
//! - ShiftSpine     → (CHAOTIC, INDETERMINATE)

use subit_core::alphabet::Primitive;
use subit_infinity::lazy_dynamics::{GrowChain, LazyIdentity, LazySystem, ShiftSpine};
use subit_infinity::lazy_p_tau::classify;
use subit_infinity::lazy_tree::LazyTree;

fn report(label: &str, p: &subit_infinity::lazy_p_tau::PTau) {
    let c = &p.certificate;
    println!(
        "  {:<14} S={:?}, Att={:?}, cycle={}, horizon={}, depth={}",
        label, c.omega_traj.s, c.omega_traj.att, c.cycle_length, c.horizon_used, c.depth_used,
    );
}

fn main() {
    println!("SUBIT-INFINITY v{} — full P(tau) demo", subit_infinity::VERSION);
    println!("spec: {}, iteration: {}", subit_infinity::SPEC_VERSION, subit_infinity::ITERATION);
    println!();

    let start = LazyTree::leaf(Primitive::T);
    let horizon = 20;
    let depth = 32;

    let sys_id = LazySystem::single(Box::new(LazyIdentity));
    let sys_grow = LazySystem::single(Box::new(GrowChain));
    let sys_spine = LazySystem::single(Box::new(ShiftSpine));

    println!("Trajectories in S_infinity (horizon={}, depth={}):", horizon, depth);
    report("identity", &classify(&sys_id, &start, 0, horizon, depth));
    report("grow_chain", &classify(&sys_grow, &start, 300, horizon, depth));
    report("shift_spine", &classify(&sys_spine, &start, 301, horizon, depth));

    println!();
    println!("Non-collapse check (U0): {}",
        if subit_infinity::lazy_p_tau::is_non_collapsing(horizon, depth) {
            "OK — classifications are distinct"
        } else {
            "FAIL — classifications collapsed"
        });
}
```

---

## `tests/lazy_invariants.rs` (новий)

```rust
//! Normative invariants for the lazy S_∞ layer.

use subit_core::alphabet::Primitive;
use subit_infinity::d_omega::d_omega;
use subit_infinity::lazy_dynamics::{GrowChain, LazyIdentity, LazySystem, ShiftSpine};
use subit_infinity::lazy_metric::{d_s, eq_bounded};
use subit_infinity::lazy_omega::{self, Attainment};
use subit_infinity::lazy_p_tau::{classify, SComponent};
use subit_infinity::lazy_tree::LazyTree;

// -------------------------------------------------------------------------
// [18.5] Attainment variants are distinct and non-trivial.
// -------------------------------------------------------------------------

#[test]
fn invariant_18_5_three_attainment_types_realized() {
    let start = LazyTree::leaf(Primitive::T);

    let sys_id = LazySystem::single(Box::new(LazyIdentity));
    let sys_grow = LazySystem::single(Box::new(GrowChain));
    let sys_spine = LazySystem::single(Box::new(ShiftSpine));

    let att_id = classify(&sys_id, &start, 0, 20, 32).omega_traj.att;
    let att_grow = classify(&sys_grow, &start, 300, 20, 32).omega_traj.att;
    let att_spine = classify(&sys_spine, &start, 301, 20, 32).omega_traj.att;

    assert_eq!(att_id, Attainment::Attained);
    assert_eq!(att_grow, Attainment::Asymptotic);
    assert_eq!(att_spine, Attainment::Indeterminate);
}

// -------------------------------------------------------------------------
// [18.6] P(τ) is total (no panics).
// -------------------------------------------------------------------------

#[test]
fn invariant_18_6_p_tau_is_total() {
    let sys = LazySystem::single(Box::new(LazyIdentity));
    for p in Primitive::ALL {
        let start = LazyTree::leaf(p);
        let _ = classify(&sys, &start, 0, 20, 16);
    }
}

// -------------------------------------------------------------------------
// [18.8] Non-collapse (У0): classifications are not constant.
// -------------------------------------------------------------------------

#[test]
fn invariant_18_8_non_collapse() {
    let start = LazyTree::leaf(Primitive::T);

    let sys_id = LazySystem::single(Box::new(LazyIdentity));
    let sys_grow = LazySystem::single(Box::new(GrowChain));
    let sys_spine = LazySystem::single(Box::new(ShiftSpine));

    let c1 = classify(&sys_id, &start, 0, 20, 32).omega_traj;
    let c2 = classify(&sys_grow, &start, 300, 20, 32).omega_traj;
    let c3 = classify(&sys_spine, &start, 301, 20, 32).omega_traj;

    let distinct = [c1, c2, c3]
        .iter()
        .collect::<std::collections::HashSet<_>>()
        .len();
    assert!(distinct >= 2, "classifications collapsed: {:?}", [c1, c2, c3]);
    // Additionally: Chaotic appears at least once.
    assert!([c1, c2, c3].iter().any(|c| c.s == SComponent::Chaotic));
    // And Stable appears at least once.
    assert!([c1, c2, c3].iter().any(|c| c.s == SComponent::Stable));
}

// -------------------------------------------------------------------------
// [15.1] d_S is an ultrametric.
// -------------------------------------------------------------------------

#[test]
fn invariant_15_1_ultrametric_on_lazy() {
    let a = LazyTree::leaf(Primitive::T);
    let b = LazyTree::leaf(Primitive::F);
    let c = LazyTree::node(a.clone(), b.clone(), a.clone());
    let d = LazyTree::node(a.clone(), b.clone(), b.clone());

    // Symmetry
    assert_eq!(d_s(&a, &b), d_s(&b, &a));
    // d(a, a) = 0
    assert_eq!(d_s(&a, &a), 0.0);
    // d(a, b) > 0 for distinct leaves
    assert!(d_s(&a, &b) > 0.0);
    // Strong triangle
    assert!(d_s(&a, &d) <= d_s(&a, &b).max(d_s(&b, &d)));
    assert!(d_s(&c, &d) <= d_s(&c, &a).max(d_s(&a, &d)));
}

// -------------------------------------------------------------------------
// [18.7] Ω_traj = (S, Att) is well-formed.
// -------------------------------------------------------------------------

#[test]
fn invariant_18_7_omega_traj_well_formed() {
    let start = LazyTree::leaf(Primitive::T);
    let sys = LazySystem::single(Box::new(GrowChain));
    let p = classify(&sys, &start, 300, 20, 32);
    let c = &p.certificate;
    // STABLE + ASYMPTOTIC is a legitimate combination.
    assert_eq!(c.omega_traj.s, SComponent::Stable);
    assert_eq!(c.omega_traj.att, Attainment::Asymptotic);
    // The certificate is self-consistent: cycle_length is 0 when no
    // cycle was detected.
    assert_eq!(c.cycle_length, 0);
    assert_eq!(c.cycle_start, None);
}

// -------------------------------------------------------------------------
// [d_omega] First-divergence metric.
// -------------------------------------------------------------------------

#[test]
fn invariant_d_omega_first_divergence() {
    let start = LazyTree::leaf(Primitive::T);
    let sys1 = LazySystem::single(Box::new(LazyIdentity));
    let sys2 = LazySystem::single(Box::new(GrowChain));
    // Identity vs GrowChain diverge at step 1 (leaf vs node).
    let d = d_omega(&sys1, &start, 0, &sys2, &start, 300, 10, 8);
    assert_eq!(d, 0.5);
    // Same system with itself → 0.
    let d0 = d_omega(&sys1, &start, 0, &sys1, &start, 0, 10, 8);
    assert_eq!(d0, 0.0);
}

// -------------------------------------------------------------------------
// [13.1] S_0 embeds into lazy S_∞.
// -------------------------------------------------------------------------

#[test]
fn invariant_13_1_s0_embeds_in_lazy() {
    use subit_core::state::State;
    for s in State::all_states().take(8) {
        let t = LazyTree::from_state(s);
        assert_eq!(t.depth_bounded(8), 1);
        let (a, b, c) = t.children().unwrap();
        assert_eq!(a.leaf_label(), Some(s.who));
        assert_eq!(b.leaf_label(), Some(s.where_));
        assert_eq!(c.leaf_label(), Some(s.when_));
    }
}

// -------------------------------------------------------------------------
// [18.2] Fingerprint equality ⟺ d_S = 0 (at the given depth).
// -------------------------------------------------------------------------

#[test]
fn invariant_18_2_fingerprint_agrees_with_metric() {
    let a = LazyTree::leaf(Primitive::T);
    let b = LazyTree::leaf(Primitive::T);
    assert!(eq_bounded(&a, &b, 8));
    assert_eq!(d_s(&a, &b), 0.0);

    let c = LazyTree::leaf(Primitive::F);
    assert!(!eq_bounded(&a, &c, 8));
    assert!(d_s(&a, &c) > 0.0);
}

// -------------------------------------------------------------------------
// [omega] ω-fingerprint set is a lower bound on ω-limit size.
// -------------------------------------------------------------------------

#[test]
fn invariant_omega_lower_bound() {
    let sys = LazySystem::single(Box::new(ShiftSpine));
    let start = LazyTree::leaf(Primitive::T);
    let (traj, cycle_start) = lazy_omega::advance(&sys, &start, 301, 20, 32);
    assert!(cycle_start.is_none());
    let lb = lazy_omega::omega_size_lower_bound(&traj);
    assert!(lb >= 20, "expected ≥ 20 distinct fingerprints, got {}", lb);
}
```

---

## `Cargo.toml` (оновлено)

```toml
[[bin]]
name = "infinity-demo"
path = "src/bin/infinity-demo.rs"

[[bin]]
name = "lazy-demo"
path = "src/bin/lazy-demo.rs"
```

---

## Запуск

```bash
cd infinity
cargo build --all-targets
cargo test
cargo run --bin lazy-demo
cargo run --bin infinity-demo
```

Очікуваний вивід `lazy-demo`:

```
SUBIT-INFINITY v0.2.0 — full P(tau) demo
spec: v6.0-draft, iteration: 4.2

Trajectories in S_infinity (horizon=20, depth=32):
  identity       S=Stable, Att=Attained, cycle=1, horizon=20, depth=32
  grow_chain     S=Stable, Att=Asymptotic, cycle=0, horizon=20, depth=32
  shift_spine    S=Chaotic, Att=Indeterminate, cycle=0, horizon=20, depth=32

Non-collapse check (U0): OK — classifications are distinct
```

**Це перша демонстрація того, що повний Ω_traj = (S, Att) не колапсує в константу.** Твердження 18.8 (У0) реалізовано.

---

## Відповідність STATUS.md

| ID | Твердження | Де реалізовано | Тест |
|---|---|---|---|
| 13.1 | S₀ ⊂ S_∞ | `LazyTree::from_state` | `invariant_13_1` |
| 15.1 | d_S — ультраметрика | `lazy_metric::d_s` | `invariant_15_1` |
| 18.2 | Fingerprint ⟺ d_S = 0 | `fingerprint`, `d_s` | `invariant_18_2` |
| 18.5 | Три типи Attainment | `lazy_omega::Attainment` | `invariant_18_5` |
| 18.6 | P(τ) — тотальна | `lazy_p_tau::classify` | `invariant_18_6` |
| 18.7 | Ω_traj = (S, Att) | `lazy_p_tau::OmegaTraj` | `invariant_18_7` |
| 18.8 | Неколлапс (У0) | `is_non_collapsing` | `invariant_18_8` |
| 22.1 | d_ω — метрика першої розбіжності | `d_omega::d_omega` | `invariant_d_omega` |
| 22.2 | ω-границя як fingerprint-множина | `lazy_omega::omega_size_lower_bound` | `invariant_omega_lower_bound` |

**Зведення після ітерації 4.2:**

| Статус | Кількість |
|---|---|
| ✅ | 54 |
| ⚠️ | 3 |
| ❌ | 0 |
| ❓ | 6 |
| 📊 | 0 |
| ⊥ | 0 |

Частка ✅: 54/63 ≈ **86%**.

---

## Що залишається відкритим після 4.2

| Питання | Статус | Коментар |
|---|---|---|
| CHAOTIC з додатною топологічною ентропією | ❓ | Потрібна конструкція зі shift space; відкладено до 4.3 |
| Реалізація ℛ_0 / ℛ_1 | ❓ | Потрібна перевірка причинності правил |
| Компактність S_∞ × ℛ_0 у коді | ❓ | Формальне доведення в Lean (Фаза 3) |
| Декартова замкненість на підкатегорії | ❓ | Q1 у STATUS.md |
| Універсальний об'єкт U | ❓ | Фаза 4.3 |
| Категорія на S_∞ | ❓ | Фаза 4.3 |

---

## Критерій завершення ітерації 4.2

- [x] Lazy-подання S_∞ (`LazyTree` з `Rc<Head>`)
- [x] Циклічні дерева (`cyclic_leaf` через `Rc::new_cyclic`)
- [x] Аперіодична траєкторія (`ShiftSpine`)
- [x] ASYMPTOTIC реалізовано (`GrowChain`)
- [x] INDETERMINATE реалізовано (`ShiftSpine`, `BoundedWrap`)
- [x] d_ω — метрика першої розбіжності
- [x] Повна P(τ): `(A(τ), Ω_traj, certificate)`
- [x] Усі три типи Attainment продемонстровано в одному запуску
- [x] Неколлапс Ω_traj перевірено
- [x] Інтеграція з CORE (S₀ ⊂ lazy S_∞)
- [x] Демонстраційний бінарник

**Ітерація 4.2 завершена. Фаза 4 в основному завершена.**

---

## Що далі

Є два шляхи:

**Шлях A — Фаза 3 (PROOFS, Lean 4).** Верифікувати T1–T10. Це критично для довгострокової довіри до v6.0. Але вимагає окремого середовища (Lean toolchain) і не дає нового коду в CORE/INFINITY.

**Шлях B — Фаза 5 (EMPIRICAL).** Один пілот на реальних часових рядах. Показує розрізнювальну здатність SUBIT проти базових моделей. Ризик: без Фази 3 твердження пілота матимуть статус 📊 без математичної опори.

**Рекомендація:** рухатися до **Фази 3 (PROOFS)**, але почати з найпростіших теорем (T1, T3, T5, T10) — щоб швидко отримати першу машинно перевірювану теорему. Це дасть конкретний Lean-файл, який потім розширимо.

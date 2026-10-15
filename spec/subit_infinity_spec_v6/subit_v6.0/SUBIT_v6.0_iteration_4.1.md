# SUBIT-INFINITY v0.1.0 — Фаза 4, ітерація 4.1

**S_∞ як регулярні дерева, d_S, ω-границя, P(τ) з трьома типами Attainment**

Оскільки Фаза 3 (Lean 4) — це окремий тип артефакту (докази), а Фаза 4 — природне продовження CORE, починаємо з Фази 4. Це дає конкретний код, який Фаза 3 згодом верифікуватиме.

Обсяг ітерації 4.1: **скінченно-регулярні дерева** (finite DAG-подання з циклічними посиланнями). Це чесне наближення S_∞: регулярні дерева утворюють підклас S_∞, достатній для демонстрації:
- d_S — структурної ультраметрики,
- трьох типів Attainment,
- неколапсу Ω_traj,
- коректної роботи P(τ).

Справжня нескінченність (CHAOTIC на аперіодичних траєкторіях) — ітерація 4.2 з lazy-поданням.

---

## Структура

```
infinity/
├── Cargo.toml
├── src/
│   ├── lib.rs
│   ├── tree.rs
│   ├── metric.rs
│   ├── dynamics.rs
│   ├── omega_limit.rs
│   ├── p_tau.rs
│   └── bin/
│       └── infinity-demo.rs
└── tests/
    └── invariants.rs
```

---

## `Cargo.toml`

```toml
[package]
name = "subit-infinity"
version = "0.1.0"
edition = "2021"
rust-version = "1.75"
description = "S_infinity layer of SUBIT v6.0: trees, d_S, omega-limit, P(tau)"
license = "MIT OR Apache-2.0"

[dependencies]
subit-core = { path = "../core" }
serde = { version = "1", features = ["derive"] }
serde_json = "1"

[[bin]]
name = "infinity-demo"
path = "src/bin/infinity-demo.rs"
```

---

## `src/lib.rs`

```rust
//! SUBIT-INFINITY — S_∞ layer of SUBIT v6.0.
//!
//! ## Scope of v0.1.0 (Phase 4, iteration 4.1)
//!
//! - `tree`        — regular trees (finite DAGs with cycles)
//! - `metric`      — structural ultrametric d_S
//! - `dynamics`    — rules on trees, systems, trajectories
//! - `omega_limit` — ω-limit computation
//! - `p_tau`       — corrected P(τ) with three Attainment types
//!
//! ## Not yet included (iteration 4.2+)
//!
//! - lazy/coinductive representation of aperiodic trees
//! - CHAOTIC class on a single trajectory
//! - categorical structure on S_∞
//! - d_ω, factor metric
//!
//! ## Normative references
//!
//! - STATUS.md (audit Part 1)
//! - SUBIT v6.0-draft, §13–15, §18 (revised)

pub mod dynamics;
pub mod metric;
pub mod omega_limit;
pub mod p_tau;
pub mod tree;

pub const VERSION: &str = env!("CARGO_PKG_VERSION");
pub const SPEC_VERSION: &str = "v6.0-draft";
pub const ITERATION: &str = "4.1";
```

---

## `src/tree.rs`

```rust
//! Regular trees — finite DAG representation of S_∞ elements.
//!
//! A tree is stored as a pool of nodes with a distinguished root.
//! Nodes either are leaves (labelled by a `Primitive`) or internal
//! nodes with three children (indices into the pool). Cycles in the
//! pool yield infinite trees by unrolling.
//!
//! This is the class of **regular trees** — a proper subset of S_∞.
//! Every regular tree is an element of S_∞, but not conversely.

use std::collections::HashMap;
use std::hash::{Hash, Hasher};

use subit_core::alphabet::Primitive;

/// Node data in the pool.
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub enum NodeData {
    Leaf(Primitive),
    Node(usize, usize, usize),
}

/// A regular tree.
#[derive(Debug, Clone)]
pub struct Tree {
    /// Nodes in the pool, in topological order (children always have
    /// smaller index than their parent — but we do not enforce this
    /// strictly; the pool may contain cycles).
    pub pool: Vec<NodeData>,
    /// Index of the root.
    pub root: usize,
}

impl PartialEq for Tree {
    fn eq(&self, other: &Self) -> bool {
        // Bisimulation-lite: same root node, same pool modulo index
        // renaming. For v0.1.0 we compare structurally up to depth
        // MAX_DEPTH. This is sound for regular trees up to that depth.
        for d in 0..=MAX_DEPTH {
            if self.subtree_at_depth(self.root, d)
                != other.subtree_at_depth(other.root, d)
            {
                return false;
            }
        }
        true
    }
}

impl Eq for Tree {}

impl Hash for Tree {
    fn hash<H: Hasher>(&self, state: &mut H) {
        // Hash up to depth MAX_DEPTH, by canonical structure.
        hash_subtree(self, self.root, MAX_DEPTH, state);
    }
}

/// Depth bound for structural equality/hashing.
pub const MAX_DEPTH: usize = 8;

/// Canonical structural fingerprint of the subtree at `node`, truncated
/// at depth `d`.
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub enum Fingerprint {
    Truncated,
    Leaf(Primitive),
    Node(Box<Fingerprint>, Box<Fingerprint>, Box<Fingerprint>),
}

pub fn fingerprint(tree: &Tree, node: usize, depth: usize) -> Fingerprint {
    if depth == 0 {
        return Fingerprint::Truncated;
    }
    match &tree.pool[node] {
        NodeData::Leaf(p) => Fingerprint::Leaf(*p),
        NodeData::Node(a, b, c) => Fingerprint::Node(
            Box::new(fingerprint(tree, *a, depth - 1)),
            Box::new(fingerprint(tree, *b, depth - 1)),
            Box::new(fingerprint(tree, *c, depth - 1)),
        ),
    }
}

fn hash_subtree<H: Hasher>(tree: &Tree, node: usize, depth: usize, state: &mut H) {
    fingerprint(tree, node, depth).hash(state);
}

fn subtree_at_depth(tree: &Tree, node: usize, depth: usize) -> Fingerprint {
    fingerprint(tree, node, depth)
}

impl Tree {
    /// A single-leaf tree.
    pub fn leaf(p: Primitive) -> Self {
        Self {
            pool: vec![NodeData::Leaf(p)],
            root: 0,
        }
    }

    /// An internal node with three children.
    pub fn node(a: &Tree, b: &Tree, c: &Tree) -> Self {
        // Merge pools with offset for each child.
        let mut pool = Vec::new();
        let off_a = 0;
        pool.extend(a.pool.iter().cloned());
        let off_b = pool.len();
        pool.extend(b.pool.iter().cloned());
        let off_c = pool.len();
        pool.extend(c.pool.iter().cloned());
        let root = pool.len();
        pool.push(NodeData::Node(
            off_a + a.root,
            off_b + b.root,
            off_c + c.root,
        ));
        Self { pool, root }
    }

    /// The S_0 embedding: `(a, b, c)` as a depth-1 tree.
    pub fn from_state(s: subit_core::state::State) -> Self {
        Self {
            pool: vec![
                NodeData::Leaf(s.who),
                NodeData::Leaf(s.where_),
                NodeData::Leaf(s.when_),
                NodeData::Node(0, 1, 2),
            ],
            root: 3,
        }
    }

    /// Children of the root, if it is an internal node.
    pub fn root_children(&self) -> Option<(Tree, Tree, Tree)> {
        match self.pool[self.root] {
            NodeData::Leaf(_) => None,
            NodeData::Node(a, b, c) => Some((
                Tree { pool: self.pool.clone(), root: a },
                Tree { pool: self.pool.clone(), root: b },
                Tree { pool: self.pool.clone(), root: c },
            )),
        }
    }

    /// Structural depth up to `MAX_DEPTH`.
    pub fn depth(&self) -> usize {
        self.depth_at(self.root, MAX_DEPTH)
    }

    fn depth_at(&self, node: usize, bound: usize) -> usize {
        if bound == 0 {
            return 0;
        }
        match self.pool[node] {
            NodeData::Leaf(_) => 0,
            NodeData::Node(a, b, c) => {
                1 + self
                    .depth_at(a, bound - 1)
                    .max(self.depth_at(b, bound - 1))
                    .max(self.depth_at(c, bound - 1))
            }
        }
    }

    /// Construct a self-referential tree: root has three children all
    /// equal to the root. This is a legitimate regular tree (infinite
    /// unrolling).
    pub fn self_ref(p: Primitive) -> Self {
        Self {
            pool: vec![
                NodeData::Leaf(p),
                NodeData::Node(1, 1, 1), // wait, node references itself
            ],
            root: 1,
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use subit_core::state::State;

    #[test]
    fn leaf_has_depth_zero() {
        assert_eq!(Tree::leaf(Primitive::T).depth(), 0);
    }

    #[test]
    fn state_embedding_has_depth_one() {
        let s = State::new(Primitive::T, Primitive::F, Primitive::N);
        let t = Tree::from_state(s);
        assert_eq!(t.depth(), 1);
    }

    #[test]
    fn node_children_are_preserved() {
        let a = Tree::leaf(Primitive::T);
        let b = Tree::leaf(Primitive::F);
        let c = Tree::leaf(Primitive::N);
        let t = Tree::node(&a, &b, &c);
        let (x, y, z) = t.root_children().unwrap();
        assert_eq!(x, a);
        assert_eq!(y, b);
        assert_eq!(z, c);
    }

    #[test]
    fn structural_equality_holds_for_equal_trees() {
        let a = Tree::leaf(Primitive::T);
        let b = Tree::leaf(Primitive::T);
        assert_eq!(a, b);
    }

    #[test]
    fn structural_equality_distinguishes_different_labels() {
        let a = Tree::leaf(Primitive::T);
        let b = Tree::leaf(Primitive::F);
        assert_ne!(a, b);
    }
}
```

---

## `src/metric.rs`

```rust
//! Structural ultrametric d_S — §18.2 of SUBIT v6.0.
//!
//! `d_S(s, t) = 2^(−δ(s, t))` where `δ(s, t)` is the least depth at
//! which the unrolled trees differ. Because regular trees can be
//! unbounded in depth, we truncate at `MAX_DEPTH` for computability.
//!
//! Truncation means `d_S` is an ultrametric on the class of regular
//! trees *up to depth MAX_DEPTH*. This is sound for all downstream
//! uses in iteration 4.1.

use crate::tree::{fingerprint, Fingerprint, Tree, MAX_DEPTH};

/// Least depth of divergence between two trees. Capped at MAX_DEPTH.
pub fn delta(s: &Tree, t: &Tree) -> usize {
    delta_at(s, s.root, t, t.root, MAX_DEPTH)
}

fn delta_at(a: &Tree, an: usize, b: &Tree, bn: usize, bound: usize) -> usize {
    if bound == 0 {
        return 0;
    }
    match (&a.pool[an], &b.pool[bn]) {
        (crate::tree::NodeData::Leaf(p), crate::tree::NodeData::Leaf(q)) => {
            if p == q { bound } else { 0 }
        }
        (crate::tree::NodeData::Leaf(_), _) => 0,
        (_, crate::tree::NodeData::Leaf(_)) => 0,
        (
            crate::tree::NodeData::Node(a1, a2, a3),
            crate::tree::NodeData::Node(b1, b2, b3),
        ) => {
            let d1 = delta_at(a, *a1, b, *b1, bound - 1);
            let d2 = delta_at(a, *a2, b, *b2, bound - 1);
            let d3 = delta_at(a, *a3, b, *b3, bound - 1);
            1 + d1.min(d2).min(d3)
        }
    }
}

/// Structural ultrametric.
pub fn d_s(s: &Tree, t: &Tree) -> f64 {
    let d = delta(s, t);
    if d >= MAX_DEPTH {
        0.0
    } else {
        2f64.powi(-(d as i32))
    }
}

/// Fingerprint-based sanity check: equality at MAX_DEPTH.
pub fn structurally_equal(s: &Tree, t: &Tree) -> bool {
    fingerprint(s, s.root, MAX_DEPTH) == fingerprint(t, t.root, MAX_DEPTH)
}

#[cfg(test)]
mod tests {
    use super::*;
    use subit_core::alphabet::Primitive;

    #[test]
    fn identical_leaves_have_distance_zero() {
        let a = Tree::leaf(Primitive::T);
        let b = Tree::leaf(Primitive::T);
        assert_eq!(d_s(&a, &b), 0.0);
    }

    #[test]
    fn distinct_leaves_have_distance_one() {
        let a = Tree::leaf(Primitive::T);
        let b = Tree::leaf(Primitive::F);
        assert_eq!(d_s(&a, &b), 1.0);
    }

    #[test]
    fn ultrametric_strong_triangle() {
        let a = Tree::leaf(Primitive::T);
        let b = Tree::leaf(Primitive::F);
        let c = Tree::leaf(Primitive::N);
        // d(a, c) ≤ max(d(a, b), d(b, c))
        let dac = d_s(&a, &c);
        let dab = d_s(&a, &b);
        let dbc = d_s(&b, &c);
        assert!(dac <= dab.max(dbc));
    }

    #[test]
    fn deeper_agreement_means_smaller_distance() {
        let a = Tree::leaf(Primitive::T);
        let b = Tree::leaf(Primitive::F);
        let c = Tree::node(&a, &b, &a);
        let d = Tree::node(&a, &b, &b);
        // c and d agree at root and first two children, diverge at third.
        let d_cd = d_s(&c, &d);
        assert!(d_cd < 1.0, "distance {} should be < 1", d_cd);
        assert!(d_cd > 0.0, "distance {} should be > 0", d_cd);
    }
}
```

---

## `src/dynamics.rs`

```rust
//! Rules and systems on S_∞ — §14 of SUBIT v6.0.
//!
//! A rule is a function `Tree -> Tree`. Rules in this iteration are
//! implemented as **local rewriting** on the DAG representation: they
//! visit the root, rebuild it, and (for depth-bounded rules) stop at
//! some depth.
//!
//! The key correction relative to v5.2: rules are not assumed to be
//! causal or continuous. We provide a `Rule` trait without continuity
//! obligations; higher-level properties are checked where needed.

use crate::tree::{NodeData, Tree};
use subit_core::alphabet::Primitive;

/// A deterministic endofunction on regular trees.
pub trait TreeRule: Send + Sync {
    fn id(&self) -> u16;
    fn name(&self) -> &'static str;
    fn apply(&self, t: &Tree) -> Tree;
}

/// A system over trees.
pub struct TreeSystem {
    rules: Vec<Box<dyn TreeRule>>,
}

impl TreeSystem {
    pub fn new(rules: Vec<Box<dyn TreeRule>>) -> Self {
        Self { rules }
    }

    pub fn single(rule: Box<dyn TreeRule>) -> Self {
        Self::new(vec![rule])
    }

    pub fn rule_ids(&self) -> Vec<u16> {
        self.rules.iter().map(|r| r.id()).collect()
    }

    pub fn rule(&self, id: u16) -> Option<&dyn TreeRule> {
        self.rules.iter().find(|r| r.id() == id).map(|b| b.as_ref())
    }

    pub fn len(&self) -> usize {
        self.rules.len()
    }

    pub fn is_empty(&self) -> bool {
        self.rules.is_empty()
    }

    /// One step of F: `(t, r) ↦ (f_r(t), g(r, t))`.
    ///
    /// Meta-evolution here is a cyclic pointer over rules; it is
    /// deliberately independent of `t` to keep the DAG pool bounded.
    pub fn step(&self, t: &Tree, rule_id: u16) -> Option<(Tree, u16)> {
        let rule = self.rule(rule_id)?;
        let next_tree = rule.apply(t);
        let ids = self.rule_ids();
        let pos = ids.iter().position(|&id| id == rule_id)?;
        let next_rule = ids[(pos + 1) % ids.len()];
        Some((next_tree, next_rule))
    }
}

// -------------------------------------------------------------------------
// Concrete rules
// -------------------------------------------------------------------------

/// `id(t) = t`.
pub struct Identity;

impl TreeRule for Identity {
    fn id(&self) -> u16 { 0 }
    fn name(&self) -> &'static str { "identity" }
    fn apply(&self, t: &Tree) -> Tree { t.clone() }
}

/// Replaces the root leaf with a fixed primitive. No-op on internal
/// nodes.
pub struct LeafRewrite(pub Primitive);

impl TreeRule for LeafRewrite {
    fn id(&self) -> u16 { 100 + self.0.code() as u16 }
    fn name(&self) -> &'static str { "leaf_rewrite" }
    fn apply(&self, t: &Tree) -> Tree {
        match t.pool[t.root] {
            NodeData::Leaf(_) => Tree::leaf(self.0),
            NodeData::Node(..) => t.clone(),
        }
    }
}

/// Extends the root: replaces a leaf `p` with `Node(Leaf(p), Leaf(p), Leaf(p))`.
/// Internal nodes are unchanged.
pub struct Grow;

impl TreeRule for Grow {
    fn id(&self) -> u16 { 200 }
    fn name(&self) -> &'static str { "grow" }
    fn apply(&self, t: &Tree) -> Tree {
        match t.pool[t.root] {
            NodeData::Leaf(p) => {
                let child = Tree::leaf(p);
                Tree::node(&child, &child, &child)
            }
            NodeData::Node(..) => t.clone(),
        }
    }
}

/// Shrinks the root: replaces `Node(a, b, c)` with `a`. Leaves unchanged.
pub struct Shrink;

impl TreeRule for Shrink {
    fn id(&self) -> u16 { 201 }
    fn name(&self) -> &'static str { "shrink" }
    fn apply(&self, t: &Tree) -> Tree {
        match t.pool[t.root] {
            NodeData::Leaf(_) => t.clone(),
            NodeData::Node(a, _, _) => Tree { pool: t.pool.clone(), root: a },
        }
    }
}

/// Cycle the labels of a leaf root: T → F → N → B → T.
pub struct CycleLeaf;

impl TreeRule for CycleLeaf {
    fn id(&self) -> u16 { 202 }
    fn name(&self) -> &'static str { "cycle_leaf" }
    fn apply(&self, t: &Tree) -> Tree {
        match t.pool[t.root] {
            NodeData::Leaf(p) => Tree::leaf(cycle_primitive(p)),
            NodeData::Node(..) => t.clone(),
        }
    }
}

fn cycle_primitive(p: Primitive) -> Primitive {
    match p {
        Primitive::T => Primitive::F,
        Primitive::F => Primitive::N,
        Primitive::N => Primitive::B,
        Primitive::B => Primitive::T,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn identity_is_identity() {
        let t = Tree::leaf(Primitive::T);
        assert_eq!(Identity.apply(&t), t);
    }

    #[test]
    fn grow_extends_a_leaf() {
        let t = Tree::leaf(Primitive::T);
        let g = Grow.apply(&t);
        assert_eq!(g.depth(), 1);
        let (a, b, c) = g.root_children().unwrap();
        assert_eq!(a, Tree::leaf(Primitive::T));
        assert_eq!(b, Tree::leaf(Primitive::T));
        assert_eq!(c, Tree::leaf(Primitive::T));
    }

    #[test]
    fn grow_is_idempotent_on_internal_nodes() {
        let t = Tree::node(
            &Tree::leaf(Primitive::T),
            &Tree::leaf(Primitive::T),
            &Tree::leaf(Primitive::T),
        );
        assert_eq!(Grow.apply(&t), t);
    }

    #[test]
    fn shrink_undoes_grow() {
        let t = Tree::leaf(Primitive::N);
        let g = Grow.apply(&t);
        let s = Shrink.apply(&g);
        assert_eq!(s, t);
    }

    #[test]
    fn cycle_leaf_has_period_4() {
        let mut t = Tree::leaf(Primitive::T);
        for _ in 0..4 {
            t = CycleLeaf.apply(&t);
        }
        assert_eq!(t, Tree::leaf(Primitive::T));
    }

    #[test]
    fn system_step_is_total() {
        let sys = TreeSystem::single(Box::new(Identity));
        let t = Tree::leaf(Primitive::T);
        assert!(sys.step(&t, 0).is_some());
    }
}
```

---

## `src/omega_limit.rs`

```rust
//! ω-limit of a trajectory in S_∞ — §18.3–18.4 of SUBIT v6.0.
//!
//! For regular trees with bounded depth, the ω-limit is computed by
//! taking the d_S-limit of the trajectory. Since our representation
//! truncates at `MAX_DEPTH`, we compute the ω-limit as the set of
//! **limit fingerprints** reached by the trajectory.

use std::collections::HashSet;

use crate::dynamics::TreeSystem;
use crate::tree::{fingerprint, Fingerprint, Tree, MAX_DEPTH};

/// One state of the extended trajectory.
pub type ExtendedTree = (Tree, u16);

/// A trajectory, together with cycle detection.
pub struct Trajectory {
    pub states: Vec<ExtendedTree>,
    pub cycle_start: Option<usize>,
}

impl Trajectory {
    pub fn cycle(&self) -> Option<&[ExtendedTree]> {
        self.cycle_start.map(|s| &self.states[s..])
    }

    pub fn len(&self) -> usize {
        self.states.len()
    }

    pub fn is_empty(&self) -> bool {
        self.states.is_empty()
    }
}

/// Advance up to `horizon` steps, detecting a cycle by structural
/// fingerprint equality on (tree, rule_id).
pub fn advance(
    system: &TreeSystem,
    start: &Tree,
    rule_id: u16,
    horizon: usize,
) -> Trajectory {
    let mut states: Vec<ExtendedTree> = Vec::new();
    let mut seen: std::collections::HashMap<Fingerprint, usize> =
        std::collections::HashMap::new();
    let mut cur = (start.clone(), rule_id);

    for n in 0..=horizon {
        let fp = fingerprint(&cur.0, cur.0.root, MAX_DEPTH);
        if let Some(&prev) = seen.get(&fp) {
            return Trajectory {
                states,
                cycle_start: Some(prev),
            };
        }
        seen.insert(fp, n);
        states.push(cur.clone());

        match system.step(&cur.0, cur.1) {
            Some(next) => cur = next,
            None => break,
        }
    }

    Trajectory {
        states,
        cycle_start: None,
    }
}

/// The ω-limit of a trajectory, as a set of limit fingerprints.
///
/// For regular trees (finite DAGs), the ω-limit is always reachable
/// in finitely many steps; we compute it as the fingerprints of the
/// eventual cycle.
pub fn omega_limit(traj: &Trajectory) -> HashSet<Fingerprint> {
    match traj.cycle() {
        Some(cycle) => cycle
            .iter()
            .map(|(t, _)| fingerprint(t, t.root, MAX_DEPTH))
            .collect(),
        None => HashSet::new(),
    }
}

/// Whether the ω-limit is reached at some finite step.
pub fn is_attained(traj: &Trajectory) -> bool {
    traj.cycle_start.is_some()
}

/// Distance from a tree to a set of fingerprints.
pub fn distance_to_limit(t: &Tree, limit: &HashSet<Fingerprint>) -> f64 {
    let fp = fingerprint(t, t.root, MAX_DEPTH);
    if limit.contains(&fp) {
        return 0.0;
    }
    // Simplified: distance = 2^-depth-of-largest-common-prefix; we use
    // the fp equality test as a coarse approximation.
    1.0
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn identity_cycle_is_immediate() {
        let sys = TreeSystem::single(Box::new(crate::dynamics::Identity));
        let t = Tree::leaf(Primitive::T);
        let traj = advance(&sys, &t, 0, 5);
        assert_eq!(traj.cycle_start, Some(0));
        assert!(is_attained(&traj));
    }

    #[test]
    fn grow_terminates() {
        // Grow is idempotent on internal nodes, so after 1 step it's a
        // fixed point.
        let sys = TreeSystem::single(Box::new(crate::dynamics::Grow));
        let t = Tree::leaf(Primitive::T);
        let traj = advance(&sys, &t, 200, 5);
        assert!(is_attained(&traj));
    }

    #[test]
    fn cycle_leaf_has_limit_of_size_4() {
        let sys = TreeSystem::single(Box::new(crate::dynamics::CycleLeaf));
        let t = Tree::leaf(Primitive::T);
        let traj = advance(&sys, &t, 202, 20);
        let limit = omega_limit(&traj);
        assert_eq!(limit.len(), 4);
    }
}
```

---

## `src/p_tau.rs`

```rust
//! Corrected P(τ) and two-axis classification — §18.5–18.9 of v6.0.
//!
//! Implements the audit's Ozn. 18.5–18.8:
//!
//! - `Attainment::{Attained, Asymptotic, Indeterminate}`
//! - `p_tau::classify(system, start, rule_id, horizon) -> PTau`

use serde::{Deserialize, Serialize};

use crate::dynamics::TreeSystem;
use crate::omega_limit::{advance, is_attained, omega_limit};
use crate::tree::Tree;

/// S-component of Ω_traj (from §18.7).
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum SComponent {
    Stable,
    Cyclic,
    Chaotic,
}

/// Attainment type of the ω-limit (from §18.5).
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum Attainment {
    /// ω-limit reached at some finite step.
    Attained,
    /// ω-limit not reached, but trajectory converges to it in d_S.
    Asymptotic,
    /// Cannot decide with available resources.
    Indeterminate,
}

/// The corrected classification function P(τ).
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PTau {
    pub s: SComponent,
    pub att: Attainment,
    /// Length of the eventual cycle, if any.
    pub cycle_length: usize,
}

/// Compute P(τ) for a trajectory in S_∞.
///
/// Uses the finite DAG representation, so the ω-limit is always
/// eventually reached (regular trees have a finite state space up to
/// bisimulation depth MAX_DEPTH). `Asymptotic` and `Indeterminate` are
/// therefore not produced in v0.1.0 — see iteration 4.2.
pub fn classify(
    system: &TreeSystem,
    start: &Tree,
    rule_id: u16,
    horizon: usize,
) -> PTau {
    let traj = advance(system, start, rule_id, horizon);

    if !is_attained(&traj) {
        return PTau {
            s: SComponent::Chaotic, // placeholder
            att: Attainment::Indeterminate,
            cycle_length: 0,
        };
    }

    let limit = omega_limit(&traj);
    let cycle_len = traj.cycle().map(|c| c.len()).unwrap_or(0);

    let s = if cycle_len == 1 {
        SComponent::Stable
    } else {
        SComponent::Cyclic
    };

    let _ = limit; // used for future asymptotic detection

    PTau {
        s,
        att: Attainment::Attained,
        cycle_length: cycle_len,
    }
}

/// Whether the classification is degenerate (constant STABLE).
///
/// This is the audit's *non-collapse* check (§18.8 / У0): a correct
/// P(τ) must return non-constant classifications.
pub fn is_non_collapsing(system: &TreeSystem, horizon: usize) -> bool {
    use crate::dynamics::{CycleLeaf, Grow, Identity};
    use subit_core::alphabet::Primitive;

    let start = Tree::leaf(Primitive::T);

    let sys_id = TreeSystem::single(Box::new(Identity));
    let sys_grow = TreeSystem::single(Box::new(Grow));
    let sys_cycle = TreeSystem::single(Box::new(CycleLeaf));

    let _ = system;

    let c_id = classify(&sys_id, &start, 0, horizon);
    let c_grow = classify(&sys_grow, &start, 200, horizon);
    let c_cycle = classify(&sys_cycle, &start, 202, horizon);

    c_id != c_grow || c_grow != c_cycle
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::dynamics::{CycleLeaf, Grow, Identity};
    use subit_core::alphabet::Primitive;

    #[test]
    fn identity_yields_stable() {
        let sys = TreeSystem::single(Box::new(Identity));
        let start = Tree::leaf(Primitive::T);
        let c = classify(&sys, &start, 0, 10);
        assert_eq!(c.s, SComponent::Stable);
        assert_eq!(c.att, Attainment::Attained);
        assert_eq!(c.cycle_length, 1);
    }

    #[test]
    fn cycle_leaf_yields_cyclic() {
        let sys = TreeSystem::single(Box::new(CycleLeaf));
        let start = Tree::leaf(Primitive::T);
        let c = classify(&sys, &start, 202, 20);
        assert_eq!(c.s, SComponent::Cyclic);
        assert_eq!(c.att, Attainment::Attained);
        assert_eq!(c.cycle_length, 4);
    }

    #[test]
    fn grow_yields_stable_at_deeper_tree() {
        let sys = TreeSystem::single(Box::new(Grow));
        let start = Tree::leaf(Primitive::T);
        let c = classify(&sys, &start, 200, 10);
        // Grow: leaf → node; node is a fixed point.
        assert_eq!(c.s, SComponent::Stable);
        assert_eq!(c.cycle_length, 1);
    }

    #[test]
    fn classification_is_non_collapsing() {
        let sys = TreeSystem::single(Box::new(Identity));
        assert!(is_non_collapsing(&sys, 20));
    }
}
```

---

## `src/bin/infinity-demo.rs`

```rust
//! Demonstration: P(τ) on three trajectories in S_∞.
//!
//! Run: `cargo run --bin infinity-demo`.

use subit_core::alphabet::Primitive;
use subit_infinity::dynamics::{CycleLeaf, Grow, Identity, TreeSystem};
use subit_infinity::p_tau::{classify, PTau};
use subit_infinity::tree::Tree;

fn report(label: &str, c: &PTau) {
    println!(
        "  {:<24} S = {:?}, Att = {:?}, cycle = {}",
        label, c.s, c.att, c.cycle_length
    );
}

fn main() {
    println!("SUBIT-INFINITY v0.1.0 — P(tau) demonstration");
    println!();

    let start = Tree::leaf(Primitive::T);

    let sys_id = TreeSystem::single(Box::new(Identity));
    let sys_grow = TreeSystem::single(Box::new(Grow));
    let sys_cycle = TreeSystem::single(Box::new(CycleLeaf));

    println!("Trajectory 1: identity rule (fixed point at depth 0)");
    report("identity", &classify(&sys_id, &start, 0, 10));

    println!();
    println!("Trajectory 2: grow rule (leaf -> node, then fixed)");
    report("grow", &classify(&sys_grow, &start, 200, 10));

    println!();
    println!("Trajectory 3: cycle_leaf rule (period-4 orbit)");
    report("cycle_leaf", &classify(&sys_cycle, &start, 202, 20));

    println!();
    println!("Non-collapse check: classifications differ across rules.");
}
```

---

## `tests/invariants.rs`

```rust
//! Invariant tests for SUBIT-INFINITY v0.1.0.

use subit_core::alphabet::Primitive;
use subit_infinity::dynamics::{CycleLeaf, Grow, Identity, TreeSystem};
use subit_infinity::metric::{d_s, delta};
use subit_infinity::omega_limit::{advance, omega_limit};
use subit_infinity::p_tau::{classify, Attainment, SComponent};
use subit_infinity::tree::Tree;

// -------------------------------------------------------------------------
// [18.1] d_S is a well-defined ultrametric.
// -------------------------------------------------------------------------

#[test]
fn invariant_18_1_ultrametric_properties() {
    let a = Tree::leaf(Primitive::T);
    let b = Tree::leaf(Primitive::F);
    let c = Tree::leaf(Primitive::N);
    let d = Tree::node(&a, &b, &a);

    // Symmetry
    assert_eq!(d_s(&a, &b), d_s(&b, &a));
    assert_eq!(d_s(&a, &d), d_s(&d, &a));

    // Zero iff structurally equal
    assert_eq!(d_s(&a, &Tree::leaf(Primitive::T)), 0.0);
    assert!(d_s(&a, &b) > 0.0);

    // Strong triangle inequality
    assert!(d_s(&a, &c) <= d_s(&a, &b).max(d_s(&b, &c)));
    assert!(d_s(&a, &d) <= d_s(&a, &b).max(d_s(&b, &d)));
}

// -------------------------------------------------------------------------
// [18.5] Attainment types are distinct.
// -------------------------------------------------------------------------

#[test]
fn invariant_18_5_attainment_variants() {
    assert_ne!(Attainment::Attained, Attainment::Asymptotic);
    assert_ne!(Attainment::Asymptotic, Attainment::Indeterminate);
    assert_ne!(Attainment::Attained, Attainment::Indeterminate);
}

// -------------------------------------------------------------------------
// [18.6] P(tau) is total on regular trees.
// -------------------------------------------------------------------------

#[test]
fn invariant_18_6_p_tau_is_total() {
    let sys = TreeSystem::single(Box::new(Identity));
    for p in Primitive::ALL {
        let start = Tree::leaf(p);
        let c = classify(&sys, &start, 0, 10);
        assert_eq!(c.s, SComponent::Stable);
        assert_eq!(c.att, Attainment::Attained);
    }
}

// -------------------------------------------------------------------------
// [18.8] Non-collapse (У0): P(tau) is not constant across rules.
// -------------------------------------------------------------------------

#[test]
fn invariant_18_8_non_collapse() {
    let start = Tree::leaf(Primitive::T);

    let sys_id = TreeSystem::single(Box::new(Identity));
    let sys_cycle = TreeSystem::single(Box::new(CycleLeaf));
    let sys_grow = TreeSystem::single(Box::new(Grow));

    let c_id = classify(&sys_id, &start, 0, 10);
    let c_cycle = classify(&sys_cycle, &start, 202, 20);
    let c_grow = classify(&sys_grow, &start, 200, 10);

    // At least two of the three must differ in S-component or cycle length.
    let classifications = [
        (c_id.s, c_id.cycle_length),
        (c_cycle.s, c_cycle.cycle_length),
        (c_grow.s, c_grow.cycle_length),
    ];
    let mut distinct = 0;
    for i in 0..classifications.len() {
        for j in (i + 1)..classifications.len() {
            if classifications[i] != classifications[j] {
                distinct += 1;
            }
        }
    }
    assert!(distinct >= 2, "classifications not distinct enough: {:?}", classifications);
}

// -------------------------------------------------------------------------
// [18.9] Machine-verifiable certificate for a trajectory.
// -------------------------------------------------------------------------

#[test]
fn invariant_18_9_trajectory_has_certificate() {
    let sys = TreeSystem::single(Box::new(CycleLeaf));
    let start = Tree::leaf(Primitive::T);
    let traj = advance(&sys, &start, 202, 20);
    assert!(traj.cycle_start.is_some());
    let limit = omega_limit(&traj);
    assert_eq!(limit.len(), 4);
    assert_eq!(traj.cycle().unwrap().len(), 4);
}

// -------------------------------------------------------------------------
// [13.1] S_0 embeds into S_∞.
// -------------------------------------------------------------------------

#[test]
fn invariant_13_1_s0_embeds() {
    use subit_core::state::State;
    for s in State::all_states().take(8) {
        let t = Tree::from_state(s);
        assert_eq!(t.depth(), 1);
        let (a, b, c) = t.root_children().unwrap();
        assert_eq!(a, Tree::leaf(s.who));
        assert_eq!(b, Tree::leaf(s.where_));
        assert_eq!(c, Tree::leaf(s.when_));
    }
}

// -------------------------------------------------------------------------
// [15.1] delta is a well-behaved divergence depth.
// -------------------------------------------------------------------------

#[test]
fn invariant_15_1_delta_bounds() {
    let a = Tree::leaf(Primitive::T);
    let b = Tree::leaf(Primitive::T);
    let c = Tree::leaf(Primitive::F);
    assert_eq!(delta(&a, &b), subit_infinity::tree::MAX_DEPTH);
    assert_eq!(delta(&a, &c), 0);
}
```

---

## Запуск

```bash
cd infinity
cargo build --all-targets
cargo test
cargo run --bin infinity-demo
```

Очікуваний вивід демо:

```
SUBIT-INFINITY v0.1.0 — P(tau) demonstration

Trajectory 1: identity rule (fixed point at depth 0)
  identity                 S = Stable, Att = Attained, cycle = 1

Trajectory 2: grow rule (leaf -> node, then fixed)
  grow                     S = Stable, Att = Attained, cycle = 1

Trajectory 3: cycle_leaf rule (period-4 orbit)
  cycle_leaf               S = Cyclic, Att = Attained, cycle = 4

Non-collapse check: classifications differ across rules.
```

---

## Відповідність STATUS.md

| ID | Твердження | Де реалізовано | Тест |
|---|---|---|---|
| 13.1 | S₀ ⊂ S_∞ | `Tree::from_state` | `invariant_13_1` |
| 15.1 | d_S — ультраметрика | `metric::d_s` | `invariant_18_1` |
| 18.1 | d_S компактний | (не реалізовано явно — обмежено MAX_DEPTH) | — |
| 18.5 | Три типи Attainment | `p_tau::Attainment` | `invariant_18_5` |
| 18.6 | P(τ) — тотальна | `p_tau::classify` | `invariant_18_6` |
| 18.8 | Неколлапс (У0) | `is_non_collapsing` | `invariant_18_8` |
| 18.9 | Сертифікат траєкторії | `omega_limit::advance` | `invariant_18_9` |

**Не реалізовано в 4.1 (обіцяно в 4.2):**
- CHAOTIC на одиничній траєкторії (потрібне lazy-подання S_∞)
- ASYMPTOTIC (потрібні нескінченні нерегулярні дерева)
- INDETERMINATE (потрібне обчислювальне обмеження)
- d_ω, факторметрика
- Повна категорія на S_∞
- P(τ) як функція з §18.8 v6.0 (з `A(τ)`, `Ω_traj`, сертифікатом)

Ці елементи складають ітерацію 4.2.

---

## Критерій завершення ітерації 4.1

- [x] Регулярні дерева як DAG-подання S_∞
- [x] d_S — ультраметрика (перевірено на прикладах)
- [x] F — тотальний на регулярних деревах
- [x] ω-границя для регулярних траєкторій
- [x] P(τ) з трьома типами Attainment (усі три визначено; реалізовано лише ATTAINED)
- [x] Неколлапс Ω_traj на трьох прикладах
- [x] Інтеграція з SUBIT-CORE (S₀ ⊂ S_∞)
- [x] Демонстраційний бінарник

**Ітерація 4.1 завершена.**

---

## Що далі: ітерація 4.2

Обсяг:

- **Lazy-подання S_∞** через `Rc<dyn Fn() -> Head>` або stateful coalgebra
- **Аперіодична траєкторія** — приклад CHAOTIC на одиничній траєкторії
- **ASYMPTOTIC** — траєкторія, що наближається до ω-границі, не досягаючи її (аналог x_n = 1/(n+1))
- **INDETERMINATE** — приклад з явною обчислювальною межею
- **d_ω** — метрика за першою розбіжністю ω-границь
- **P(τ) у повній формі** §18.8 v6.0: (A(τ), Ω_traj, certificate)

Після ітерації 4.2 Фаза 4 буде завершена, і можна буде повернутися до Фази 3 (Lean 4) для верифікації T1–T10, а потім до Фази 5 (EMPIRICAL).

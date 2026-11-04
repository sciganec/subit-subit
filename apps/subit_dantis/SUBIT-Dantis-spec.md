# SUBIT-TOPOS · Dantis Cosmologia — Specification v1.1

> **Status:** DRAFT · Partial Reconstruction  
> **Date:** 2026-11-03  
> **Atlas:** Cosmologia Dantis v1.1 · SUBIT-TOPOS  

---

## 1. Formal Core

### 1.1 State Space S₀

```
S₀ = A³   where  A = {0,1,2,3}
|S₀| = 4³ = 64 states
```

Three independent coordinate axes, each 2-bit:

| Axis  | Bits | Values                                              |
|-------|------|-----------------------------------------------------|
| WHO   | 2    | THEY(00=0) · YOU(01=1) · ME(10=2) · WE(11=3)       |
| WHERE | 2    | NORTH(00=0) · WEST(01=1) · EAST(10=2) · SOUTH(11=3)|
| WHEN  | 2    | WINTER(00=0) · AUTUMN(01=1) · SPRING(10=2) · SUMMER(11=3) |

### 1.2 Encoding Function

```
code6(WHO, WHERE, WHEN) = 16·WHO + 4·WHERE + WHEN
range: [0 .. 63]
```

**Canonical states:**

| code6 | Binary  | WHO  | WHERE | WHEN   | Dante locus        |
|-------|---------|------|-------|--------|--------------------|
| 0     | 000000₂ | THEY | NORTH | WINTER | Lucifer / minimal  |
| 42    | 101010₂ | ME   | EAST  | SPRING | Selva Oscura (start)|
| 63    | 111111₂ | WE   | SOUTH | SUMMER | Empyrean / maximal |

### 1.3 Ω Classifier (Experimental)

The Ω function assigns a dynamical class to each state. **No formal operator or transition rule is yet defined.** All labels are heuristic and subject to revision.

```javascript
function getOmega(c) {
  if (c === 0)  return "Ω?·0";    // minimal element
  if (c === 63) return "Ω?·63";   // maximal element
  if (c === 42) return "Ω?·42";   // Dante start (heuristic)
  if ((c & (c-1)) === 0 || c === 62) return "Ω?·pow2";
  return "Ω?·gen";
}
```

Ω requires formal definition of:
- transition operator T: S₀ → S₀
- fixed-point criteria
- orbit structure
- invariant subsets

Until these are defined, all Ω values carry the `?` prefix.

### 1.4 Principle: DO NOT COLLAPSE — CONTEXTUALIZE

Multiple Dante loci may share the same code6. This is not an error. The coordinate state is a *context key*, not a unique identifier. Resolution requires:

```
{
  regionId:   string,          // specific locus (e.g. "cocito")
  code6:      0..63,           // SUBIT coordinate
  contextId:  string,          // narrative context (e.g. "inferno.circle-9")
  provenance: {
    source:      string,       // e.g. "Inferno XXXI–XXXIV"
    status:      string,       // "authorial" | "interpolated" | "experimental"
    ruleVersion: "SUBIT-TOPOS-1.1"
  }
}
```

**Current collision map (code6 → region count):**

| code6  | Regions sharing it |
|--------|--------------------|
| 0      | 9                  |
| 4      | 2                  |
| 25     | 2                  |
| 26     | 2                  |
| 27     | 1                  |
| 58     | 2                  |
| 62     | 2                  |
| 63     | 6                  |

Disambiguation UI: when multiple regions share a state, all names are shown in the **context** row of the info panel.

---

## 2. Logical Layer: Belnap FOUR

Belnap FOUR is a **separate logical module**, independent of the SUBIT coordinate axes.

| Symbol | Bits | Meaning        |
|--------|------|----------------|
| N      | 00   | Neither (no information) |
| F      | 01   | False only     |
| T      | 10   | True only      |
| B      | 11   | Both (contradictory) |

**Critical distinction:** the 2-bit encoding of Belnap values (00–11) coincidentally matches the 2-bit range of each SUBIT axis, but the two structures are **not interchangeable**. WHO/WHERE/WHEN axes carry spatio-temporal coordinates; N/F/T/B carry logical truth values. They operate on different domains and must not be conflated.

---

## 3. Dante Cosmological Model

### 3.1 Paradiso — Nine Moving Heavens

Correctly ordered, geocentric, nested spheres:

| #  | Heaven        | Cantica    | Virtue / Theme  |
|----|---------------|------------|-----------------|
| I  | Luna          | Par. II    | Incostanza      |
| II | Mercurio      | Par. V     | Ambizione       |
| III| Venere        | Par. VIII  | Amore           |
| IV | Sole          | Par. X     | Sapienza        |
| V  | Marte         | Par. XIV   | Fortezza        |
| VI | Giove         | Par. XVIII | Giustizia       |
| VII| Saturno       | Par. XXI   | Contemplazione  |
| VIII| Stelle Fisse | Par. XXVII | —               |
| IX | Primo Mobile  | Par. XXVIII| Prima Causa     |

**Empyrean** = immaterial luminous field beyond all spheres. It has no physical radius; it is not a tenth sphere. Its SUBIT assignment (code6=63, WE⊗SOUTH⊗SUMMER) is an interpretive correspondence, not a geometric coordinate.

### 3.2 Inferno — Structure

```
Surface (Jerusalem) → Vestibolo / Ante-Inferno
                     ↓
         Cerchio I  — Limbo
         Cerchio II — Lussuria
         Cerchio III — Gola
         Cerchio IV  — Avarizia / Prodigalità
         Cerchio V   — Ira / Accidia
         Cerchio VI  — Eresìa
         Cerchio VII — Violenza (tre gironi)
         Cerchio VIII — Malebolge (dieci bolge)
         Cerchio IX  — Cocito
                         ├── Caina
                         ├── Antenora
                         ├── Tolomea
                         └── Giudecca
                              └── Lucifer (centre of Earth)
```

**Note:** Ante-Inferno (Vestibolo) is architecturally separate from the nine circles. The current atlas model includes it as a layer alongside the circles — this is visually functional but not strictly canonical.

**Cocito** requires four distinct geometric sectors with individual hit areas. Currently implemented as text labels only.

### 3.3 Purgatorio — Structure

```
Southern hemisphere (antipodal to Jerusalem)
  └── Island base
       ├── Ante-Purgatorio (excommunicates, negligent)
       ├── Cornicia I  — Superbia
       ├── Cornicia II — Invidia
       ├── Cornicia III — Ira
       ├── Cornicia IV — Accidia
       ├── Cornicia V  — Avarizia
       ├── Cornicia VI — Gola
       ├── Cornicia VII — Lussuria
       └── Earthly Paradise (Eden) — summit
```

Currently the atlas represents all seven terraces as a single `corniche` region. Each cornice should be an independent interactive object with its own ID. SUBIT coordinate assignment for individual terraces has not been formally defined and must be treated as interpretive.

---

## 4. Rendering Engine — Current State

### 4.1 Projection

Custom Canvas 2D perspective with yaw/pitch camera:

```javascript
const FOV = 20;
function proj(x, y, z, o) {
  // yaw rotation
  const x1 = x*cos(yaw) + z*sin(yaw);
  const z1 = -x*sin(yaw) + z*cos(yaw);
  // pitch rotation
  const y1 = y*cos(pitch) - z1*sin(pitch);
  const z2 = y*sin(pitch) + z1*cos(pitch);
  if (z2 >= FOV - 0.01) { o.k = 0; return o; }  // near-plane clip
  const k = FOV / (FOV - z2);
  o.x = W/2 + x1 * min(W,H) * 0.1 * zoom * k;
  o.y = H/2 - y1 * min(W,H) * 0.1 * zoom * k;
  return o;
}
```

**FOV=20** prevents near-plane blow-up for scene radii up to ~8 units.

### 4.2 Rendering Loop

Demand-driven via `invalidate()`:

```javascript
function invalidate() {
  if (!rafId) { rafId = requestAnimationFrame(frame); }
}
// New frames scheduled only on: state change, resize, drag, key, auto-rotate
```

### 4.3 Known Limitations

| Issue | Status |
|-------|--------|
| Far clipping | Not implemented |
| Line clipping at near plane | Line dropped entirely if either endpoint clips |
| Hit-testing | Nearest-point only; no area or line testing |
| Pointer state machine | No formal IDLE/DRAG/PINCH/INERTIA states |
| Drag inertia | Based on event count, not Δposition/Δtime |

---

## 5. Scene Inventory

| Scene   | Description                                 | Camera default     |
|---------|---------------------------------------------|--------------------|
| COSMOS  | Full model, all layers                      | side view          |
| INFERNO | Inverted cone, 10 layers, Cocito            | angled             |
| PARADISO| Nine spheres + Empyrean rays                | side               |
| MANDALA | Top-down view reusing COSMOS geometry       | top (pitch≈−π/2)   |
| SUBIT   | 3D axis display for WHO/WHERE/WHEN          | angled             |

---

## 6. Verification Status

| Check | Status |
|-------|--------|
| SUBIT axis encoding (code6 formula) | ✅ |
| Initial state = ME/EAST/SPRING = 42 | ✅ |
| Lullian wheel binary labels (00/01/10/11) | ✅ |
| Belnap FOUR as separate logical layer | ✅ |
| getRegion() returns null for unknown IDs | ✅ |
| Demand-driven rendering | ✅ |
| Multi-match disambiguation in UI | ✅ |
| Ω marked experimental | ✅ |
| contextId / provenance structure | ❌ not yet |
| Formal Ω operator | ❌ not yet |
| 7 independent terrace objects | ❌ not yet |
| 4 geometric Cocito sectors | ❌ not yet |
| Near/far line clipping | ❌ not yet |
| Object-level hit-testing | ❌ not yet |
| 64-state exhaustive tests | ❌ not yet |
| Region mapping regression tests | ❌ not yet |

---

## 7. Version History

| Version | Date       | Key changes |
|---------|------------|-------------|
| v1.0    | 2025       | Initial 2D+3D unified interface |
| v1.1    | 2026-10    | Purgatory geometry, SUBIT axis clicks, MANDALA scene, line depth sorting |
| v1.1 V7 | 2026-10   | Double HTML wrapper fix, getRegion() null safety, binary wheel labels |
| v1.1 V9 | 2026-11-03| Demand-driven rendering, Belnap note fix, Ω experimental, multi-match disambiguation, mobile schema toggle |
| v1.1 V10| 2026-11-03| Stale Ω labels removed from region notes, BEL comment corrected |

---

## 8. Next Release: v1.2 — Contextual Reconstruction

Recommended architecture:

```
SUBIT-TOPOS v1.2
│
├── FORMAL CORE
│   ├── SUBIT-64  (WHO × WHERE × WHEN)
│   ├── CONTEXT   (regionId + contextId)
│   ├── PROVENANCE (source + status + ruleVersion)
│   └── Ω         (only if formally defined)
│
├── LOGIC
│   └── BELNAP FOUR (independent module)
│
├── DANTE MODEL
│   ├── INFERNO
│   │   ├── ANTE-INFERNO (Vestibolo)
│   │   ├── NINE CIRCLES (I–IX)
│   │   └── COCITO — four sectors (Caina/Antenora/Tolomea/Giudecca)
│   ├── PURGATORIO
│   │   ├── ANTE-PURGATORY
│   │   ├── SEVEN TERRACES (I–VII, individual IDs)
│   │   └── EDEN (summit)
│   └── PARADISO
│       ├── NINE MOVING HEAVENS (I–IX)
│       └── IMMATERIAL EMPYREAN
│
├── VISUAL ENGINE
│   ├── Near + far line clipping
│   ├── Object-level hit-testing
│   ├── Pointer state machine (IDLE/DRAG/PINCH/INERTIA)
│   └── Demand-driven rendering ✅ (done in v1.1 V9)
│
└── VERIFICATION
    ├── 64-state exhaustive tests
    ├── Region mapping regression tests
    └── Browser smoke tests (5 scenes)
```

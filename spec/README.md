# spec/ — специфікації SUBIT-∞

Хронологічний архів специфікацій. Усі версії зберігаються без вилучень.

---

## Поточний стабільний реліз

**[subit_infinity_spec_v6/subit_v6.13.37-39/](subit_infinity_spec_v6/subit_v6.13.37-39/)**

| Файл | Призначення |
| :-- | :-- |
| [`subit_v6.13.39_stable.md`](subit_infinity_spec_v6/subit_v6.13.37-39/subit_v6.13.39_stable.md) | Специфікація (заморожений текст) |
| [`subit_v6.13.37_lean_mathlib.tar.gz`](subit_infinity_spec_v6/subit_v6.13.37-39/subit_v6.13.37_lean_mathlib.tar.gz) | Lean 4.32.0 / Mathlib v4.32.0 (2472 задачі, 0 попереджень) |
| [`subit_v6.13.39_manifest.md`](subit_infinity_spec_v6/subit_v6.13.37-39/subit_v6.13.39_manifest.md) | Хеші SHA-256 і відтворюваність |
| [`subit_v6.13.39_release_notes.md`](subit_infinity_spec_v6/subit_v6.13.37-39/subit_v6.13.39_release_notes.md) | Що змінено |
| [`subit_v6.13.39_review.md`](subit_infinity_spec_v6/subit_v6.13.37-39/subit_v6.13.39_review.md) | Журнал рецензування |

**Lean-перевірено:** W6 (W6Word, W6Tree), W7 (W7Abstract, W7Word, W7Tree), W8 (W8GTree), твердження Дод. Е.
Аксіоми: лише `propext`, `Classical.choice`, `Quot.sound`.

---

## Дослідницький модуль (підготовка до v6.14)

**[subit_warp/](subit_warp/)**

SUBIT-WARP v0.4 — формальна модель деревоподібних структур, граничної геометрії та ієрархічної спектральної динаміки (W0–W24). Статус: DRAFT · CANONICAL CONSOLIDATION · NOT STABLE.

Залежність: SUBIT-∞ v6.13.39 Stable (не змінює її означень).

| Файл | Зміст |
| :-- | :-- |
| [`subit_warp_00_randall_sundrum.md`](subit_warp/subit_warp_00_randall_sundrum.md) | Вихідне есе: походження WARP-концепції |
| [`subit_warp_v0.1.md`](subit_warp/subit_warp_v0.1.md) | Перша специфікація |
| [`subit_warp_v0.2.0.md`](subit_warp/subit_warp_v0.2.0.md) | v0.2.0 |
| [`subit_warp_v0.3.md`](subit_warp/subit_warp_v0.3.md) | v0.3 Proof-Refined |
| [`subit_warp_v0.4.0.md`](subit_warp/subit_warp_v0.4.0.md) | **v0.4.0: W21 Canonical Specification** |
| [`subit_warp_v0.4_draft_11_canonical.md`](subit_warp/subit_warp_v0.4_draft_11_canonical.md) | **W23: Canonical Corrections & Unified Specification** |
| [`subit_warp_v0.4_draft_12_audit_2.md`](subit_warp/subit_warp_v0.4_draft_12_audit_2.md) | **W24: Primary Source Audit (W0–W6 foundations)** |

Ключовий результат W9: ядро взаємодії є степеневою функцією метрики межі ($K_q = d_v^\beta$), де $\beta = \alpha_w/\alpha_v$ — похідний геометричний інваріант. v0.4 кодифікує структурну й спектральну системи (W0–W24). Деталі та повний список аудитів див. у [`subit_warp/README.md`](subit_warp/README.md).

---

## Альтернативні надбудови

**[subit_alternative/](subit_alternative/)**

Альтернативні теоретичні надбудови над `subit_spec_v0.1.md` — не залежать від SUBIT-∞.

| Файл | Зміст |
| :-- | :-- |
| [`01_intention.md`](subit_alternative/01_intention.md) | Аналіз природності розвитку v0.1 → v6; альтернативні шляхи |
| [`02_intention_2.md`](subit_alternative/02_intention_2.md) | Продовження аналізу |
| [`subit_alt1_v0.1/subit_alt1_spec_v0.1.md`](subit_alternative/subit_alt1_v0.1/subit_alt1_spec_v0.1.md) | **SUBIT-ALT1**: ℤ₄³, 86016 оборотних матриць, ядерна гексаграма |
| [`subit_alt1_v0.1/verify_alt1.py`](subit_alternative/subit_alt1_v0.1/verify_alt1.py) | Перевірка ALT1 (Python + numpy) |
| [`subit_alt2_v0.1/subit_alt2_spec_v0.1.md`](subit_alternative/subit_alt2_v0.1/subit_alt2_spec_v0.1.md) | **SUBIT-ALT2 v0.1**: контексти, S5×S5×S5, циклічний час |
| [`subit_alt2_v0.1/subit_alt2_spec_v0.2.md`](subit_alternative/subit_alt2_v0.1/subit_alt2_spec_v0.2.md) | **ALT2 v0.2**: гексаграма як відношення доступності |
| [`subit_alt2_v0.1/verify_alt2.py`](subit_alternative/subit_alt2_v0.1/verify_alt2.py) | Перевірка ALT2 v0.1 |
| [`subit_alt2_v0.1/verify_alt2b.py`](subit_alternative/subit_alt2_v0.1/verify_alt2b.py) | Перевірка ALT2 v0.2 |

---

## Архів версій

| Папка / Файл | Версія | Дата |
| :-- | :-- | :-- |
| `subit_spec_v0.1.md` | v0.1 (прототип) | — |
| `subit_infinity_spec_v3.md` | v3 | Jul 2026 |
| `subit_infinity_spec_v4.md` | v4 | Jul 2026 |
| `subit_infinity_spec_v5.md` | v5 | Jul 2026 |
| `subit_infinity_spec_v5_2.md` | v5.2 | Aug 2026 |
| `subit_infinity_spec_v5_1_EXT/` | v5.1 EXT: монографія та коментарі | Oct 2026 |
| `subit_infinity_spec_v6/subit_v6.0/` | v6.0 | — |
| `subit_infinity_spec_v6/subit_v6.1-7/` | v6.1–6.7 | — |
| `subit_infinity_spec_v6/subit_v6.8/` | v6.8 | — |
| `subit_infinity_spec_v6/subit_v6.9/` | v6.9 | — |
| `subit_infinity_spec_v6/subit_v6.10/` | v6.10 | — |
| `subit_infinity_spec_v6/subit_v6.11/` | v6.11 | — |
| `subit_infinity_spec_v6/subit_v6.12/` | v6.12 | — |
| `subit_infinity_spec_v6/subit_v6.13.0-9/` | v6.13.0–9 | — |
| `subit_infinity_spec_v6/subit_v6.13.10-19/` | v6.13.10–19 | — |
| `subit_infinity_spec_v6/subit_v6.13.20-29/` | v6.13.20–29 | — |
| `subit_infinity_spec_v6/subit_v6.13.30-36/` | v6.13.30–36 | — |
| `subit_infinity_spec_v6/subit_v6.13.37-39/` | **v6.13.37–39 (STABLE)** | Nov 2026 |

Принцип: **незворотність**. Жодна версія не вилучається.

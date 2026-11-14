# SUBIT-∞ v6.14.0

**Версія:** v6.14.0  
**Тип:** Інтегрована архітектурна специфікація (RC Candidate Preparation)  
**Дата:** 7 листопада 2026 року  
**Статус:** INTEGRATED SPECIFICATION DRAFT · NOT STABLE

---

## Файли цього релізу

| Файл | Призначення |
| :-- | :-- |
| [`subit_v6.14.0.md`](subit_v6.14.0.md) | **Головна специфікація** — повний текст (429 рядків, 16 секцій) |
| [`subit_v6.14.0_release_notes.md`](subit_v6.14.0_release_notes.md) | Що нового відносно v6.13.39 |
| [`subit_v6.14.0_readme.md`](subit_v6.14.0_readme.md) | Цей файл |

---

## Що інтегровано

v6.14.0 вперше об'єднує три напрями в єдину специфікацію:

```text
(SUBIT-64 ⊗ ALT) ≼ₐ SUBIT⁺ ≼ₐ SUBIT-CAT ≼ₐ SUBIT-∞ ≼ₐ (SUBIT-∞ ⋉ WARP)
```

| Компонент | Що включено |
| :-- | :-- |
| **SUBIT-∞ v6.13.39** | Заморожене ядро: аксіоматика, динаміка, ентропія, Lean W6–W8 (2472 задачі, 0 попереджень) |
| **SUBIT-ALT v0.3** | $\mathbb{Z}_4^3$-алгебра, 86016 оборотних матриць, $N$-оператор, $S5^3$-логіка, 36 класів бісимуляції |
| **SUBIT-WARP v0.4** | Межа $\Sigma_b$, $\dim_H = \ln(b)/\alpha_v$, 2-ліпшицевий $\partial$, оператор $T_q$, реконструкція T-020′/T-021′ |

---

## Прапорці системи

| Прапорець | Стан |
| :-- | :-- |
| DEFINED | ✅ |
| PROVED ON PAPER | ✅ (ALT-1–ALT-6, T-001–T-021) |
| AUDITED BY EXECUTION | 🟡 ЧАСТКОВО |
| RUST-TESTED | 🟡 ЧАСТКОВО (57 тестів, крейт `subit`) |
| LEAN-CHECKED | 🟡 ЧАСТКОВО (базове ядро: W6, W7, W8, Дод. Е) |
| BUILD-PASSED-FROM-ARCHIVE | 🟡 ЧАСТКОВО |
| CLEAN-REPRODUCIBLE-BUILD | ⛔ НІ |
| IMPLEMENTED (conformant) | ⛔ НІ |
| EMPIRICALLY SUPPORTED | ⛔ НІ |

---

## Quick Start

**Читання специфікації:**
1. Відкрийте [`subit_v6.14.0.md`](subit_v6.14.0.md) — секція §0 описує статуси, принципи та архітектуру.
2. §1–§5: базовий простір, ALT-алгебра, тор $\mathbb{Z}_4^3$, бісимуляція.
3. §6–§9: коалгебраїчна динаміка, дерева, нескінченні гілки, ентропія.
4. §10–§12: WARP-геометрія: межа $\Sigma_b$, метрики, оператор $T_q$, спектр.
5. §13–§14: реєстри теорем ALT та WARP із статусами доведення.
6. §15: верифікація та відкриті питання.
7. §16: журнал переходу v6.13.39 → v6.14.0.

**Пов'язані специфікації:**
- **Базове ядро:** [`../subit_v6.13.37-39/subit_v6.13.39_stable.md`](../subit_v6.13.37-39/subit_v6.13.39_stable.md)
- **WARP канон (C2):** [`../../subit_warp/subit_warp_v0.4/subit_warp_v0.4.md`](../../subit_warp/subit_warp_v0.4/subit_warp_v0.4.md)
- **ALT v0.3:** [`../../subit_alt/subit_alt_v0.3/`](../../subit_alt/subit_alt_v0.3/)

---

## Ворота релізу

Статус STABLE буде надано після закриття:
- **G-12:** повний регресійний пакет W20 (нескінченні дерева WARP) ⛔
- **G-13:** Lean kernel verification Blueprint W45 ⛔
- **G-14:** Rust implementation audit (WARP + ALT) ⛔
- **G-15:** CLEAN-REPRODUCIBLE-BUILD для повної системи ⛔

---

## Залежні файли (не у цій папці)

| Файл | Розташування |
| :-- | :-- |
| `subit_v6.13.39_stable.md` | `spec/subit_infinity_spec_v6/subit_v6.13.37-39/` |
| `subit_warp_v0.4.md` | `spec/subit_warp/subit_warp_v0.4/` |
| `verify_alt1.py` та ін. | `spec/subit_alt/subit_alt_v0.3/` |

---

*SUBIT-∞ v6.14.0 · DRAFT · NOT STABLE · 7 листопада 2026*

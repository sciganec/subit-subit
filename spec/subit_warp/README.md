# SUBIT-WARP

**Статус:** DRAFT · NOT STABLE  
**Версія:** v0.4 (W23′ + W34.1.3–W34.1.9 integration/release-preparation series; RC не оголошено)  
**Дата:** 5 листопада 2026 року  
**Базова система:** SUBIT-∞ v6.13.39 Stable  
**Принцип:** DO NOT COLLAPSE — CONTEXTUALIZE  

---

## Мета

SUBIT-WARP — дослідницький модуль над SUBIT-∞ (підготовка до v6.14), що вивчає взаємозв'язок між:

1. структурою скінченних та нескінченних дерев;
2. простором причинних перетворень;
3. геометрією нескінченних граничних гілок;
4. операторами взаємодії на просторі меж;
5. спектральними властивостями ієрархічних операторів та реконструкцією.

**Дослідницька гіпотеза:** структурна ієрархія Tree∞ індукує геометрію межі, а геометрія межі дозволяє побудувати оператори, спектр яких відображає ієрархічну організацію початкової структури.

WARP не змінює означень базової системи і не є частиною стабільної специфікації.

---

## Архітектурний розподіл (W0–W32)

Модуль розділяє дві фундаментальні системи:

- **STRUCTURAL SYSTEM**: простір адрес, вузли, листки, глибини, відношення батьківства та інваріанти.
- **SPECTRAL SYSTEM**: міри, ядра взаємодії, інтегральні оператори, спектри та операторні збурення.

### Еволюція розділів:
- **W0–W6**: Первинні конструкції (дерева, межа, метрика $d_v$, міра, спадне та обернене ядра).
- **W7–W10**: Спектральний оператор $T_q$, скінченна апроксимація, розмежування параметрів (W9: $\beta = \alpha_w/\alpha_v$, $K_q = d_v^\beta$), верифікація (W10).
- **W11–W20**: Неоднорідні моделі, межі спектральної та структурної реконструкції.
- **W21 / v0.4.0**: Канонічна консолідація (`subit_warp_v0.4.0.md`).
- **W23**: Канонічні виправлення та уніфікована математична специфікація (`subit_warp_v0.4_draft_11_canonical.md`).
- **W24**: Первинний аудит математичних основ W0–W6 (`subit_warp_v0.4_draft_12_audit_2.md`, частковий).
- **W24.16**: Завершений первинний аудит W0–W6 за оригінальним текстом v0.3 (`subit_warp_v0.4_draft_14_audit_3.md`).
- **W23′**: Канонічна редакція W23, виправлена після W24.16: d_F / d_Σ / d_T / d_H, PartialTree як нове розширення, Tω⁺ і теорема W5.4′, K_Vl(ξ,ξ)=0 (`subit_warp_v0.4_draft_13_canonical.md`).
- **W25**: Executable Verification — аналітично й чисельно перевірено; Lean/Rust не виконано (`subit_warp_v0.4_draft_15_audit_4.md`).
- **W26**: Canonical Integration & Release Audit — INTEGRATION CANDIDATE (`subit_warp_v0.4_draft_16_audit_5.md`).
- **W27**: Proof Closure — ANALYTICAL PROOF CLOSURE COMPLETED (`subit_warp_v0.4_draft_17.md`).
- **W28**: Global Consistency & Regression Spec — специфікацію завершено, W20 suite не виконано (`subit_warp_v0.4_draft_18.md`).
- **W29**: Independent Mathematical Audit — **CORRECTIONS REQUIRED** (C-11…C-15) (`subit_warp_v0.4_draft_19.md`).
- **W30**: Theorem Registry & Proof Dependency — MATHEMATICALLY CONSOLIDATED DRAFT (`subit_warp_v0.4_draft_20.md`).
- **W31**: Formalization Boundary & Lean Blueprint — архітектуру задано, реалізації немає (`subit_warp_v0.4_draft_21.md`).

**Поточний канон:** Канонічна консолідована специфікація [`subit_warp_v0.4.md`](subit_warp_v0.4.md) інтегрує W23′, W30, W31, W34.1.3–W34.1.9 та W39–W47 (Enc/Dec correspondence, повне розмежування метрик d_F / d_Σ / d_T / d_H, домен Tω⁺, повні теореми T-001–T-021, чисельну перевірку W25 та Lean 4 Blueprint W45). За критеріями реліз-контролю статус залишається **DRAFT · NOT STABLE · NOT RELEASE CANDIDATE (RC NOT DECLARED)**, оскільки повний регресійний пакет W20, Lean kernel verification та implementation audit (Rust) очікують завершення (ворота G-12, G-13, G-14).

---

## Файли специфікації та аудиту

| Файл | Зміст |
| :-- | :-- |
| [`subit_warp_00_randall_sundrum.md`](subit_warp_00_randall_sundrum.md) | Вихідне есе: аналогія з моделлю Randall–Sundrum |
| [`subit_warp_v0.1.md`](subit_warp_v0.1.md) | Специфікація v0.1 |
| [`subit_warp_v0.2.0.md`](subit_warp_v0.2.0.md) | Специфікація v0.2.0 |
| [`subit_warp_v0.2.1.md`](subit_warp_v0.2.1.md) | Редакція v0.2.1 |
| [`subit_warp_v0.2_audit.md`](subit_warp_v0.2_audit.md) | Аудит v0.2 |
| [`subit_warp_v0.3.md`](subit_warp_v0.3.md) | Специфікація v0.3 (Proof-Refined) |
| [`subit_warp_v0.3_audit_1.md`](subit_warp_v0.3_audit_1.md) | Аудит v0.3: W6–W8 |
| [`subit_warp_v0.3_audit_2.md`](subit_warp_v0.3_audit_2.md) | Аудит v0.3: W9 (перший прохід) |
| [`subit_warp_v0.3_audit_3.md`](subit_warp_v0.3_audit_3.md) | Аудит v0.3: W9 Parameter Separation (фінальний) |
| [`subit_warp_v0.3_audit_4.md`](subit_warp_v0.3_audit_4.md) | Аудит v0.3 (частина 4) |
| [`subit_warp_v0.3_audit_5.md`](subit_warp_v0.3_audit_5.md) | Аудит v0.3 (частина 5) |
| [`subit_warp_v0.4.0.md`](subit_warp_v0.4.0.md) | **v0.4.0: W21 Canonical Specification** |
| [`subit_warp_v0.4_draft_1.md`](subit_warp_v0.4_draft_1.md) – [`_10_audit.md`](subit_warp_v0.4_draft_10_audit.md) | Чернетки та аудити еволюції v0.4 |
| [`subit_warp_v0.4_draft_11_canonical.md`](subit_warp_v0.4_draft_11_canonical.md) | **W23: Canonical Corrections & Unified Specification** |
| [`subit_warp_v0.4_draft_12_audit_2.md`](subit_warp_v0.4_draft_12_audit_2.md) | **W24: Primary Source Audit (W0–W6 foundations)** — частковий, доповнено W24.16 |
| [`subit_warp_v0.4_draft_14_audit_3.md`](subit_warp_v0.4_draft_14_audit_3.md) | **W24.16: Primary Source Audit W0–W6 — COMPLETED WITH CORRECTIONS** (раніше згадувався як `draft_12_audit_3`) |
| [`subit_warp_v0.4_draft_13_canonical.md`](subit_warp_v0.4_draft_13_canonical.md) | **W23′: Canonical Corrections after W24.16 (поточна канонічна редакція)** |
| [`subit_warp_v0.4_draft_15_audit_4.md`](subit_warp_v0.4_draft_15_audit_4.md) | **W25: Executable Verification** |
| [`subit_warp_v0.4_draft_16_audit_5.md`](subit_warp_v0.4_draft_16_audit_5.md) | **W26: Canonical Integration & Release Audit** |
| [`subit_warp_v0.4_draft_17.md`](subit_warp_v0.4_draft_17.md) | **W27: Proof Closure** |
| [`subit_warp_v0.4_draft_18.md`](subit_warp_v0.4_draft_18.md) | **W28: Global Consistency & Regression Spec** |
| [`subit_warp_v0.4_draft_19.md`](subit_warp_v0.4_draft_19.md) | **W29: Independent Mathematical Audit — CORRECTIONS REQUIRED** |
| [`subit_warp_v0.4_draft_20.md`](subit_warp_v0.4_draft_20.md) | **W30: Theorem Registry & Proof Dependency** |
| [`subit_warp_v0.4_draft_21.md`](subit_warp_v0.4_draft_21.md) | **W31: Formalization Boundary & Lean Blueprint** |
| [`subit_warp_v0.4_draft_39_architecture.md`](subit_warp_v0.4_draft_39_architecture.md) | **W39: Consolidation Architecture** |
| [`subit_warp_v0.4_draft_40.md`](subit_warp_v0.4_draft_40.md) | **W40: Mathematical Consistency Audit** |
| [`subit_warp_v0.4_draft_41.md`](subit_warp_v0.4_draft_41.md) | **W39.1: Metric and Type Consistency Correction** |
| [`subit_warp_v0.4_draft_42.md`](subit_warp_v0.4_draft_42.md) | **W41: T-007 Boundary Map Proof Closure** |
| [`subit_warp_v0.4_draft_43.md`](subit_warp_v0.4_draft_43.md) | **W42: Spectral Theory Audit** |
| [`subit_warp_v0.4_draft_44.md`](subit_warp_v0.4_draft_44.md) | **W43: Encoding/Decoding Correctness Audit** |
| [`subit_warp_v0.4_draft_45.md`](subit_warp_v0.4_draft_45.md) | **W44: W20 Regression Audit** |
| [`subit_warp_v0.4_draft_46.md`](subit_warp_v0.4_draft_46.md) | **W45: Lean 4 Formalization Blueprint** |
| [`subit_warp_v0.4_draft_47.md`](subit_warp_v0.4_draft_47.md) | **W46: Independent Release Audit** |
| [`subit_warp_v0.4_draft_48.md`](subit_warp_v0.4_draft_48.md) | **W47: Source Recovery & Dependency Closure** |
| [`subit_warp_v0.4_draft_49_consolodated.md`](subit_warp_v0.4_draft_49_consolodated.md) | **Consolidated Draft — C1** |
| [`subit_warp_v0.4.md`](subit_warp_v0.4.md) | **Канонічна специфікація SUBIT-WARP v0.4 (Consolidated Canonical C2)** |

---

## Обмеження та статус

- Специфікація має статус **DRAFT · NOT STABLE**; поточний канон — W23′ (`draft_13`); RC не оголошено (W32); наступний крок — I-3, далі W33.
- Lean 4 формалізація та чисельна сертифікація матриць $3^n \times 3^n$ залишаються відкритими (W10).
- Фізична інтерпретація гравітаційних аналогій — суто дослідницька гіпотеза зі статусом `PHYSICAL-CORRESPONDENCE-OPEN`.


## W34.1 — поточна інтеграція та підготовка релізу

| Файл | Зміст | Статус |
|---|---|---|
| `subit_warp_v0.4_draft_32.md` | W34.1.3 Corrected Canonical Integration Patch | ANALYTICALLY CHECKED |
| `subit_warp_v0.4_draft_33.md` | W34.1.4 Independent Mathematical Audit | CONDITIONAL PASS |
| `subit_warp_v0.4_draft_34.md` | W34.1.5 Enc/Dec Correspondence Patch | TYPE-CORRECTED; NOT LEAN-VERIFIED |
| `subit_warp_v0.4_draft_35.md` | W34.1.6 Independent Enc/Dec Review | CONDITIONAL PASS |
| `subit_warp_v0.4_draft_36.md` | W34.1.7 W23′ / W30 Integration Proposal | PROPOSAL ONLY; NOT APPLIED |
| `subit_warp_v0.4_draft_37.md` | W34.1.8 Stable Release Readiness Gate | BLOCKED; NOT STABLE |
| `subit_warp_v0.4_draft_38.md` | W34.1.9 Independent Review of W23′ / W30 Integration Proposal | CONDITIONAL PASS; FULL DIFF REVIEW REQUIRED |

**Важливо:** W34.1.7 не змінює W23′ або W30. W20 full regression, Lean kernel verification та implementation audit не можна вважати пройденими без фактичного виконання й відтворюваних артефактів.

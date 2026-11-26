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

**Поточний канон:** Канонічна консолідована специфікація [`subit_warp_v0.4.md`](subit_warp_v0.4/subit_warp_v0.4.md) інтегрує W23′, W30, W31, W34.1.3–W34.1.9 та W39–W47 (Enc/Dec correspondence, повне розмежування метрик d_F / d_Σ / d_T / d_H, домен Tω⁺, повні теореми T-001–T-021, чисельну перевірку W25 та Lean 4 Blueprint W45). За критеріями реліз-контролю статус залишається **DRAFT · NOT STABLE · NOT RELEASE CANDIDATE (RC NOT DECLARED)**, оскільки повний регресійний пакет W20, Lean kernel verification та implementation audit (Rust) очікують завершення (ворота G-12, G-13, G-14).

---

## Файли специфікації та аудиту

| Файл | Зміст |
| :-- | :-- |
| [`subit_warp_v0.0_randall_sundrum.md`](subit_warp_v0.0/subit_warp_v0.0_randall_sundrum.md) | Вихідне есе: аналогія з моделлю Randall–Sundrum |
| [`subit_warp_v0.1.md`](subit_warp_v0.1/subit_warp_v0.1.md) | Специфікація v0.1 |
| [`subit_warp_v0.2.0.md`](subit_warp_v0.2/subit_warp_v0.2.0.md) | Специфікація v0.2.0 |
| [`subit_warp_v0.2.1.md`](subit_warp_v0.2/subit_warp_v0.2.1.md) | Редакція v0.2.1 |
| [`subit_warp_v0.2_audit.md`](subit_warp_v0.2/subit_warp_v0.2_audit.md) | Аудит v0.2 |
| [`subit_warp_v0.3.md`](subit_warp_v0.3/subit_warp_v0.3.md) | Специфікація v0.3 (Proof-Refined) |
| [`subit_warp_v0.3_audit_1.md`](subit_warp_v0.3/drafts/subit_warp_v0.3_audit_1.md) – [`_audit_5.md`](subit_warp_v0.3/drafts/subit_warp_v0.3_audit_5.md) | Аудити v0.3 (W6–W9, Parameter Separation) |
| `subit_warp_v0.4.0` | **v0.4.0: W21 Canonical Specification** (консолідовано в [`subit_warp_v0.4.md`](subit_warp_v0.4/subit_warp_v0.4.md)) |
| [`subit_warp_v0.4_draft_11_canonical.md`](subit_warp_v0.4/drafts/subit_warp_v0.4_draft_00-49/subit_warp_v0.4_draft_11_canonical.md) | **W23: Canonical Corrections & Unified Specification** |
| [`subit_warp_v0.4_draft_12_audit_2.md`](subit_warp_v0.4/drafts/subit_warp_v0.4_draft_00-49/subit_warp_v0.4_draft_12_audit_2.md) | **W24: Primary Source Audit (W0–W6 foundations)** |
| [`subit_warp_v0.4_draft_13_canonical.md`](subit_warp_v0.4/drafts/subit_warp_v0.4_draft_00-49/subit_warp_v0.4_draft_13_canonical.md) | **W23′: Canonical Corrections after W24.16 (канонічна редакція)** |
| [`subit_warp_v0.4_draft_14_audit_3.md`](subit_warp_v0.4/drafts/subit_warp_v0.4_draft_00-49/subit_warp_v0.4_draft_14_audit_3.md) – [`_16_audit_5.md`](subit_warp_v0.4/drafts/subit_warp_v0.4_draft_00-49/subit_warp_v0.4_draft_16_audit_5.md) | W24.16–W26: Primary Source, Executable Verification (W25), Release Audit |
| [`subit_warp_v0.4_draft_17.md`](subit_warp_v0.4/drafts/subit_warp_v0.4_draft_00-49/subit_warp_v0.4_draft_17.md) – [`_21.md`](subit_warp_v0.4/drafts/subit_warp_v0.4_draft_00-49/subit_warp_v0.4_draft_21.md) | W27–W31: Proof Closure, Regression Spec, Independent Audit, Lean Blueprint |
| [`subit_warp_v0.4_draft_32.md`](subit_warp_v0.4/drafts/subit_warp_v0.4_draft_00-49/subit_warp_v0.4_draft_32.md) – [`_38.md`](subit_warp_v0.4/drafts/subit_warp_v0.4_draft_00-49/subit_warp_v0.4_draft_38.md) | W34.1.3–W34.1.9: Integration Patches, Enc/Dec Correspondence, Readiness Gates |
| [`subit_warp_v0.4_draft_39_architecture.md`](subit_warp_v0.4/drafts/subit_warp_v0.4_draft_00-49/subit_warp_v0.4_draft_39_architecture.md) – [`_48.md`](subit_warp_v0.4/drafts/subit_warp_v0.4_draft_00-49/subit_warp_v0.4_draft_48.md) | W39–W47: Consolidation Architecture, Metric Consistency, Spectral Theory Audit |
| [`subit_warp_v0.4_draft_49_consolidated.md`](subit_warp_v0.4/drafts/subit_warp_v0.4_draft_00-49/subit_warp_v0.4_draft_49_consolidated.md) | **Consolidated Draft — C1** |
| [`subit_warp_v0.4.md`](subit_warp_v0.4/subit_warp_v0.4.md) | **Канонічна специфікація SUBIT-WARP v0.4 (Consolidated Canonical C2)** |
| [`subit_warp_v0.4_draft_50.md`](subit_warp_v0.4/drafts/subit_warp_v0.4_draft_50-99/subit_warp_v0.4_draft_50.md) – [`_53.md`](subit_warp_v0.4/drafts/subit_warp_v0.4_draft_50-99/subit_warp_v0.4_draft_53.md) | **W48–W49.1**: C2 Integration Audit, Corrective Patch, Fingerprint Reconstruction |
| [`subit_warp_v0.4_draft_54.md`](subit_warp_v0.4/drafts/subit_warp_v0.4_draft_50-99/subit_warp_v0.4_draft_54.md) – [`_57.md`](subit_warp_v0.4/drafts/subit_warp_v0.4_draft_50-99/subit_warp_v0.4_draft_57.md) | **W50–W53**: Reconstruction Axioms, Minimal Axioms, Tree-Class Selection, Boundary Quotients |
| [`subit_warp_v0.4_draft_58.md`](subit_warp_v0.4/drafts/subit_warp_v0.4_draft_50-99/subit_warp_v0.4_draft_58.md) – [`_60.md`](subit_warp_v0.4/drafts/subit_warp_v0.4_draft_50-99/subit_warp_v0.4_draft_60.md) | **W54–W55**: Enriched Boundary, Information Geometry and Audit |
| [`subit_warp_v0.4_draft_61.md`](subit_warp_v0.4/drafts/subit_warp_v0.4_draft_50-99/subit_warp_v0.4_draft_61.md) – [`_65.md`](subit_warp_v0.4/drafts/subit_warp_v0.4_draft_50-99/subit_warp_v0.4_draft_65.md) | **W56–W60**: Boundary Dynamics, Grafting Semigroup, Symbolic Geometry, Transfer Dynamics, Verification |
| [`subit_warp_v0.4_draft_66.md`](subit_warp_v0.4/drafts/subit_warp_v0.4_draft_50-99/subit_warp_v0.4_draft_66.md) – [`_68.md`](subit_warp_v0.4/drafts/subit_warp_v0.4_draft_50-99/subit_warp_v0.4_draft_68.md) | **W61–W63**: Operator Limits, Spectral Measures, Observational Equivalence & Information Quotients |

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
